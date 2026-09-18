"""Demo dışındaki gerçek sınır durumları ve veri güvenliği için regresyonlar."""
import copy
import csv
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import eslesme_kontrol
import build_dashboard as pano
import insights
import match
import pipeline
import veri


def basvuru(**changes):
    app = {"id": "ornek-analist", "company": "Örnek", "role": "Analist", "channel": "ats",
           "stage": "under_review", "status": "awaiting_response", "applied": "2026-09-01",
           "last_contact": "2026-09-01", "deadline": None, "fit": 3, "track": "Analiz",
           "next_step": None, "notes": None, "match": None, "gap_skills": [], "links_actions": []}
    app.update(changes)
    return app


def belge(*apps):
    return {"meta": {"owner": "Örnek", "email": "ornek@example.com", "last_scan": "2026-09-17",
                     "scan_window": {"from": "2026-09-01", "to": "2026-09-17"}},
            "applications": list(apps)}


def puan(**changes):
    values = {"role_family": 35, "seniority": 25, "skills": 25, "domain": 15,
              "location_mod": 0, "rationale": "Örnek ilan/profil karşılaştırması."}
    values.update(changes)
    return values


class VeriTestleri(unittest.TestCase):
    def test_demo_semasi(self):
        with patch.dict(os.environ, {"TRACE_DATA": str(ROOT / "data")}):
            self.assertEqual(veri.basvuru_hatalari(veri.oku("applications.json"), veri.oku("skills_catalog.json")), [])

    def test_bilinmeyen_asama_yanlis_puana_donusmez(self):
        with self.assertRaisesRegex(ValueError, "stage"):
            pipeline.enrich(belge(basvuru(stage="interwiev")), date(2026, 9, 17))

    def test_null_tarih_ve_puan_bilinmeyen_kalir(self):
        result = pipeline.enrich(belge(basvuru(applied=None, last_contact=None, fit=None)), date(2026, 9, 17))[0]
        self.assertIsNone(result["match_score"])
        self.assertIsNone(result["days_silent"])
        self.assertEqual(result["score"], 35)

    def test_boyut_sinirlari_ve_sayi_tipi(self):
        for invalid in [puan(role_family=36), puan(skills=-1), puan(domain=True),
                        puan(seniority=float("nan")), puan(location_mod=1), {}]:
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                match.score_match({"match": invalid})

    def test_yinelenen_kimlik_tarih_ve_beceri(self):
        data = belge(basvuru(), basvuru(applied="2026-02-30", gap_skills=["bilinmeyen"]))
        errors = veri.basvuru_hatalari(data, {"skills": {}})
        for term in ["yinelenen", "applied", "gap_skills"]:
            self.assertTrue(any(term in e for e in errors))

    def test_unsafe_url_reddedilir(self):
        for url in ["javascript:alert(1)", "data:text/html,abc", "https://user:password@example.com", "https://example.com\n"]:
            with self.subTest(url=url):
                self.assertFalse(veri.guvenli_url(url))
        self.assertFalse(veri.guvenli_url("https://example.com", "gmail"))
        self.assertTrue(veri.guvenli_url("https://mail.google.com/mail/u/0/#search/ornek", "gmail"))

    def test_eslestirme_kaynak_veriyi_degistirmez(self):
        data = belge(basvuru(match=puan()))
        original = copy.deepcopy(data)
        pipeline.enrich(data, date(2026, 9, 17))
        self.assertEqual(data, original)

    def test_ayni_surecte_veri_klasoru_degisebilir(self):
        with tempfile.TemporaryDirectory() as one, tempfile.TemporaryDirectory() as two:
            for folder, name in [(one, "Birinci"), (two, "İkinci")]:
                Path(folder, "profile.json").write_text(json.dumps({"name": name}))
            with patch.dict(os.environ, {"TRACE_DATA": one}):
                self.assertEqual(match.load_profile()["name"], "Birinci")
            with patch.dict(os.environ, {"TRACE_DATA": two}):
                self.assertEqual(match.load_profile()["name"], "İkinci")
            with patch.dict(os.environ, {"TRACE_DATA": two}):
                with self.assertRaisesRegex(ValueError, "applications.json"):
                    veri.oku("applications.json")


class HesaplamaTestleri(unittest.TestCase):
    def test_eslesme_esikleri(self):
        for score, segment in [(0,"weak"),(44,"weak"),(45,"fair"),(61,"fair"),(62,"good"),(77,"good"),(78,"strong"),(100,"strong")]:
            with self.subTest(score=score):
                result = match.score_match({"match": puan(location_mod=score - 100)})
                self.assertEqual((result["score"], result["segment_key"]), (score, segment))

    def test_deadline_esikleri(self):
        for days, expected in [(None,0),(-1,40),(0,35),(1,35),(2,25),(3,25),(4,15),(7,15),(8,8),(14,8),(15,0)]:
            with self.subTest(days=days):
                self.assertEqual(pipeline.deadline_bonus(days), expected)

    def test_sessizlik_tam_esikte_cezalandirilir(self):
        app = basvuru()
        self.assertEqual(pipeline.score(app, date(2026, 9, 12)), 47)
        self.assertEqual(pipeline.score(app, date(2026, 9, 13)), 39)
        self.assertEqual(pipeline.score(app, date(2026, 9, 22)), 27)

    def test_kapanmis_kayit_aksiyon_uretmez(self):
        for status in ["rejected", "in_progress"]:
            app = basvuru(stage="closed", status=status, deadline="2026-09-01")
            self.assertEqual(pipeline.reminders_for(app, date(2026, 9, 17)), [])
            self.assertEqual(pipeline.score(app, date(2026, 9, 17)), 0)
            self.assertEqual(pipeline.band(app, date(2026, 9, 17), 100), "archive")

    def test_bugunku_yanit_iki_raporda_ayni(self):
        apps = pipeline.enrich(belge(basvuru(stage="interviewed", last_contact="2026-09-17")), date(2026, 9, 17))
        self.assertEqual(pipeline.funnel(apps)["response_rate"], 100)
        self.assertEqual(insights.funnel(apps, {"jobs": []})["steps"][2]["value"], 1)

    def test_otomatik_onay_yanit_sayilmaz(self):
        app = basvuru(last_contact="2026-09-02")
        self.assertFalse(veri.yanit_var(app))
        self.assertIsNone(insights.response_speed([app])["median_days"])

    def test_sure_ilk_yanittan_olculur(self):
        apps = [basvuru(first_response="2026-09-02", last_contact="2026-09-17"),
                basvuru(first_response="2026-09-11", last_contact="2026-09-17")]
        self.assertEqual(insights.response_speed(apps)["median_days"], 5.5)
        self.assertEqual(insights.response_speed([basvuru(first_response="2026-09-01")])["median_days"], 0)

    def test_haftalar_sabit_aydan_bagimsiz(self):
        apps = [basvuru(applied="2025-12-31"), basvuru(applied="2026-01-01"),
                basvuru(applied="2026-09-17"), basvuru(applied=None)]
        groups = insights.trend(apps)
        self.assertEqual([g["applied"] for g in groups], [2, 1])
        self.assertEqual(groups[1]["start"], "2026-09-14")
        self.assertEqual([g["value"] for g in pano.weekly_volume(apps)], [2, 1])
        self.assertIn("2025", groups[0]["label"])

    def test_bos_basvuru_ve_bos_kullanim(self):
        self.assertEqual(insights.funnel([], {"jobs": []})["reject_rate"], 0)
        self.assertEqual(pipeline.funnel([])["response_rate"], 0)
        result = insights.engagement({"report_days": []}, [], date(2026, 9, 17))
        self.assertEqual(result["calendar"], [])
        self.assertEqual(result["coverage"], 0)

    def test_kullanim_gelecek_ve_tekrar_gunleri_saymaz(self):
        eng = {"tracking_started":"2026-09-10", "report_days":["2026-09-09", "2026-09-16", "2026-09-16", "2026-09-17", "2026-09-18"]}
        result = insights.engagement(eng, [], date(2026, 9, 17))
        self.assertEqual(result["reports_sent"], 2)
        self.assertEqual(result["reports_last_7d"], 2)
        self.assertEqual(result["current_streak"], 2)
        self.assertLessEqual(result["coverage"], 100)
        self.assertEqual(insights.engagement(eng, [], date(2026, 9, 1))["days_tracked"], 0)

    def test_huni_asama_gecisini_uydurmaz(self):
        data = insights.funnel([basvuru(stage="offer")], {"jobs": []})
        self.assertTrue(all(step["conv_from_prev"] is None for step in data["steps"][3:]))
        self.assertEqual(data["steps"][-1]["value"], 1)


class CiktiTestleri(unittest.TestCase):
    def test_json_html_script_kapatamaz(self):
        value = '</script><script>alert("test")</script>\u2028'
        html = pano.html_uret({"probe": value})
        self.assertNotIn(value, html)
        line = next(x for x in html.splitlines() if x.startswith("const D = "))
        self.assertEqual(json.loads(line[len("const D = "):-1])["probe"], value)

    def test_markdown_hatirlatma_govdesi_gorunur(self):
        data = belge(basvuru(stage="assessment", status="action_required", deadline="2026-09-17"))
        apps = pipeline.enrich(data, date(2026, 9, 17))
        report = pipeline.render_markdown(apps, pipeline.funnel(apps), data, date(2026, 9, 17))
        self.assertIn("Deadline BUGÜN", report)
        self.assertNotIn("hatırlatma yok", report)

    def test_site_farkli_sureclerde_ayni_uretilir(self):
        code = "import sys,hashlib;sys.path.insert(0,'src');import build_dashboard as b;from datetime import date;print(hashlib.sha256(b.html_uret(b.payload_uret(date(2026,9,1),True)).encode()).hexdigest())"
        results = []
        for seed in ["1", "17"]:
            env = {**os.environ, "TRACE_DATA": str(ROOT / "data"), "PYTHONHASHSEED": seed}
            result = subprocess.run([sys.executable, "-c", code], cwd=ROOT, env=env, capture_output=True, text=True, check=True)
            results.append(result.stdout)
        self.assertEqual(results[0], results[1])

    def test_csv_metni_formul_calistiramaz(self):
        app = pipeline.enrich(belge(basvuru(company=' =HYPERLINK("https://example.com")')), date(2026, 9, 17))[0]
        rows = list(csv.reader(io.StringIO(pipeline.render_csv([app]))))
        self.assertTrue(rows[1][4].startswith("'"))

    def test_demo_aksiyon_ve_iletisim_verisi_tasimasin(self):
        with patch.dict(os.environ, {"TRACE_DATA": str(ROOT / "data")}):
            payload = pano.payload_uret(date(2026, 9, 1), public_demo=True)
        self.assertTrue(payload["demo"])
        self.assertEqual(payload["outreach"], [])
        self.assertTrue(all(not a["links_actions"] and a["contact"] is None for a in payload["applications"]))

    def test_ozel_veri_siteye_yazilmaz(self):
        with tempfile.TemporaryDirectory() as private:
            env = {**os.environ, "TRACE_DATA": private}
            for args in [["--site"], ["--out", str(ROOT / "site" / "app.html")]]:
                result = subprocess.run([sys.executable, str(ROOT / "src" / "build_dashboard.py"), *args], env=env, capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("site", result.stderr)

    def test_bos_veriyle_tum_komutlar(self):
        with tempfile.TemporaryDirectory() as private:
            folder = Path(private)
            for source in (ROOT / "data").glob("*.json"):
                folder.joinpath(source.name).write_bytes(source.read_bytes())
            folder.joinpath("applications.json").write_text(json.dumps(belge()))
            folder.joinpath("profile.json").write_text("null")
            folder.joinpath("engagement.json").write_text('{"report_days": []}')
            folder.joinpath("saved_jobs.json").write_text('{"jobs": []}')
            folder.joinpath("role_targets.json").write_text('{"meta": {}, "hedefler": []}')
            env = {**os.environ, "TRACE_DATA": private}
            for script, args in [("pipeline.py", ["--format", "json"]), ("match.py", []),
                                 ("insights.py", []), ("build_dashboard.py", ["--out", str(folder / "pano.html")])]:
                result = subprocess.run([sys.executable, str(ROOT / "src" / script), *args], env=env, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(folder.joinpath("pano.html").exists())


class AjanKontrolTestleri(unittest.TestCase):
    def test_gecerli_oneri_dosya_yazmadan_dogrulanir(self):
        proposal = {"match": puan(), "gap_skills": [], "hesaplanan_toplam": 100,
                    "segment": "strong", "guven": "yuksek"}
        original = copy.deepcopy(proposal)
        self.assertTrue(eslesme_kontrol.dogrula(proposal, {"skills": {}})["gecerli"])
        self.assertEqual(proposal, original)

    def test_ajanin_yanlis_aritmetigi_reddedilir(self):
        proposal = {"match": puan(location_mod=-23), "gap_skills": [],
                    "hesaplanan_toplam": 78, "segment": "strong", "guven": "orta"}
        with self.assertRaisesRegex(ValueError, "uyuşmuyor"):
            eslesme_kontrol.dogrula(proposal, {"skills": {}})

    def test_bilinmeyen_ilan_sifir_puan_olmaz(self):
        proposal = {"match": None, "gap_skills": [], "hesaplanan_toplam": None,
                    "segment": None, "guven": "dusuk"}
        self.assertIsNone(eslesme_kontrol.dogrula(proposal, {"skills": {}})["match_result"])
        proposal["hesaplanan_toplam"] = 0
        with self.assertRaises(ValueError):
            eslesme_kontrol.dogrula(proposal, {"skills": {}})


if __name__ == "__main__":
    unittest.main()
