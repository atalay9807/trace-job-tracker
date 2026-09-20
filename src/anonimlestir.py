#!/usr/bin/env python3
"""Gerçek başvuru verisini açık depoya konabilecek demo veriye çevirir.

Gerçek veri özel depoda durur, demo veri açık depoda yayınlanır. Bu script
ikisi arasındaki tek köprüdür: şirket adlarını takma adlarla değiştirir,
kişisel bilgiyi temizler ve **çıktıda gerçek bir ad kalmadığını doğrular.**

Eşleme tablosu (`anonimlestirme/eslesme.json`) özel depodadır ve oraya
kalır — o tablo gerçek adla takma adı yan yana tutar, yani yeniden
kimliklendirme anahtarıdır. Bu script tablonun içeriğini taşımaz, okur.

Tasarımın tek kritik özelliği: **eşlemesi olmayan şirket görülürse script
durur.** Bilinmeyen adı olduğu gibi geçirmek, sessizce gerçek veri sızdırmak
demektir; bu yüzden geçirmek yerine durmak seçildi. Yeni bir şirkete
başvurulduğunda script hata verir, tabloya takma ad eklenir, tekrar çalışır.

Kullanım:
    TRACE_DATA=/yol/trace-data/data python3 src/anonimlestir.py --yaz

    --yaz verilmezse hiçbir dosyaya dokunmaz, ne olacağını yazdırır.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import sys
import unicodedata
import urllib.parse

KOK = pathlib.Path(__file__).resolve().parent.parent

# Demo tarafında elle bakımı yapılan, bu script'in ÜRETMEDİĞİ dosyalar.
# profile.json özellikle burada: CV özeti serbest metindir ve otomatik
# dönüştürmenin kaçırdığı bir ayrıntı doğrudan kişiyi ele verir. CV yılda
# birkaç kez değişir; o değişiklik insan gözünden geçmeyi hak ediyor.
ELLE_BAKILAN = {"profile.json", "skills_catalog.json", "journey.json",
                "engagement.json", "role_targets.json", "last_scan.json"}

URETILEN = ["applications.json", "saved_jobs.json"]


def kimliksizle(s: str) -> str:
    """Türkçe karakterleri sadeleştirip id'ye uygun hale getirir."""
    s = unicodedata.normalize("NFKD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    for a, b in (("ı", "i"), ("ş", "s"), ("ğ", "g"), ("ü", "u"), ("ö", "o"), ("ç", "c")):
        s = s.replace(a, b)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"-{2,}", "-", s)


class Anonimlestirici:
    def __init__(self, esleme: dict):
        self.sirketler: dict = esleme["sirketler"]
        self.profil: dict = esleme["profil"]
        self.gorulmeyen: set = set()

        # Değiştirme sırası UZUNDAN KISAYA. "Getir Perakende Lojistik A.Ş."
        # önce gitmezse "Getir" onu parçalar ve geride "Perakende Lojistik
        # A.Ş." kalır — yani gerçek bilgi sızar.
        birlesik = {**self.sirketler, **self.profil}
        self.kurallar = sorted(
            ((k, v) for k, v in birlesik.items() if k and k != "—"),
            key=lambda kv: -len(kv[0]),
        )
        # Doğrulamada aranacak yasaklı diziler: her gerçek ad.
        self.yasakli = [k for k, _ in self.kurallar if len(k) >= 3]

    # ---------- dönüştürme ----------

    def takma(self, sirket: str | None) -> str:
        if sirket in (None, "", "—"):
            return "—"
        if sirket not in self.sirketler:
            self.gorulmeyen.add(sirket)
            return sirket          # çağıran durduracak; burada sessizce geçme
        return self.sirketler[sirket]

    def takma_kisi(self) -> str:
        return self.profil.get("Atalay Denizer", "—")

    def metin(self, s):
        """Serbest metindeki her gerçek adı takma adıyla değiştirir."""
        if not isinstance(s, str):
            return s
        for gercek, sahte in self.kurallar:
            if gercek in s:
                s = s.replace(gercek, sahte)
        # İlan/talep numaraları şirketi aratılabilir kılıyor — sabit bir
        # türevle değiştirilir ki kayıt tutarlı kalsın ama izlenebilir olmasın.
        s = re.sub(r"\b[A-Z]{0,3}\d{5,}\b",
                   lambda m: "R" + hashlib.sha256(m.group().encode()).hexdigest()[:6].upper(), s)
        return s

    def gmail_baglantisi(self, sirket: str) -> dict:
        return {"label": "Maili aç", "kind": "gmail",
                "url": "https://mail.google.com/mail/u/0/#search/"
                       + urllib.parse.quote(f"from:{sirket}", safe="")}

    def kayit(self, a: dict) -> dict:
        sirket = self.takma(a.get("company"))
        rol = self.metin(a.get("role"))
        y = dict(a)
        y["company"] = sirket
        y["role"] = rol
        # id şirket adı taşıyor — takma addan yeniden üretilir
        parca = kimliksizle(sirket) or "kayit"
        if rol and rol != "—":
            parca += "-" + "-".join(kimliksizle(rol).split("-")[:3])
        y["id"] = parca
        for alan in ("notes", "next_step", "track", "location", "contact", "rationale"):
            if alan in y:
                y[alan] = self.metin(y[alan])
        if isinstance(y.get("match"), dict) and y["match"].get("rationale"):
            y["match"] = {**y["match"], "rationale": self.metin(y["match"]["rationale"])}
        # Bağlantılar yeniden üretilir: URL içinde url-encoded gerçek ad
        # kalmasın diye metin değiştirmeye güvenilmez.
        if y.get("links_actions"):
            y["links_actions"] = [self.gmail_baglantisi(sirket)]
        y.pop("links", None)
        return y


def _son_tarih(kayitlar: list) -> str:
    """Veride geçen en ileri tarih. Panonun 'bugün'ü buradan gelir."""
    return max((k.get(a) or "" for k in kayitlar
                for a in ("last_contact", "applied", "first_response")), default="")


def _ilk_tarih(kayitlar: list) -> str:
    return min((k.get("applied") or "9999-99-99" for k in kayitlar), default="")


def benzersizlestir(kayitlar: list) -> list:
    """Aynı id'ye düşen kayıtlara sayaç ekler (aynı şirkete ikinci rol)."""
    sayac: dict = {}
    for k in kayitlar:
        n = sayac.get(k["id"], 0) + 1
        sayac[k["id"]] = n
        if n > 1:
            k["id"] = f"{k['id']}-{n}"
    return kayitlar


def dogrula(dizin: pathlib.Path, yasakli: list) -> list:
    """Yayınlanacak KLASÖRÜN TAMAMINI tarar. Tek bir gerçek ad bulursa hata.

    Yalnızca üretilen dosyaya değil, tüm klasöre bakılır: elle bakılan bir
    dosyaya kazara gerçek bir ad girdiyse onu da burada yakalamak gerekir.
    """
    bulgular = []
    for p in sorted(dizin.glob("*.json")):
        metin = p.read_text(encoding="utf-8")
        # JSON kaçışlı Unicode de aranabilsin diye çözülmüş hali de taranır
        try:
            duz = json.dumps(json.loads(metin), ensure_ascii=False)
        except json.JSONDecodeError:
            duz = metin
        # mailto/gmail baglantilari icindeki ad ve e-posta URL-encoded durur;
        # 'atalay%40gmail' duz aramada gorunmez, bu yuzden cozulmus hali de taranir.
        govdeler = (metin, duz, urllib.parse.unquote(metin), urllib.parse.unquote(duz))
        for kotu in yasakli:
            for govde in govdeler:
                if re.search(r"(?<![0-9A-Za-zÇĞİÖŞÜçğıöşü])" + re.escape(kotu)
                             + r"(?![0-9A-Za-zÇĞİÖŞÜçğıöşü])", govde):
                    bulgular.append((p.name, kotu))
                    break
    return sorted(set(bulgular))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--yaz", action="store_true", help="dosyalara yaz (yoksa kuru çalışma)")
    ap.add_argument("--kaynak", default=os.environ.get("TRACE_DATA"),
                    help="gerçek veri klasörü (varsayılan: TRACE_DATA)")
    ap.add_argument("--esleme", help="eşleme tablosu (varsayılan: <kaynak>/../anonimlestirme/eslesme.json)")
    ap.add_argument("--hedef", default=str(KOK / "data"), help="demo veri klasörü")
    a = ap.parse_args()

    if not a.kaynak:
        print("HATA: gerçek veri klasörü verilmedi (TRACE_DATA ya da --kaynak).", file=sys.stderr)
        return 2
    kaynak = pathlib.Path(a.kaynak)
    esleme_yolu = pathlib.Path(a.esleme) if a.esleme else kaynak.parent / "anonimlestirme" / "eslesme.json"
    hedef = pathlib.Path(a.hedef)

    for yol, ad in ((kaynak, "kaynak"), (esleme_yolu, "eşleme tablosu"), (hedef, "hedef")):
        if not yol.exists():
            print(f"HATA: {ad} bulunamadı: {yol}", file=sys.stderr)
            return 2

    an = Anonimlestirici(json.load(esleme_yolu.open(encoding="utf-8")))
    cikti: dict = {}

    for ad in URETILEN:
        kyol = kaynak / ad
        if not kyol.exists():
            print(f"  atlandı (kaynakta yok): {ad}")
            continue
        veri = json.load(kyol.open(encoding="utf-8"))
        if ad == "applications.json":
            veri["applications"] = benzersizlestir([an.kayit(x) for x in veri["applications"]])
            # recruiter_outreach serbest metin ve kişi adı taşıyabiliyor —
            # anonimleştirmek yerine tamamen düşürülür.
            veri.pop("recruiter_outreach", None)
            # meta gercek ad, e-posta ve uyari metni tasiyor. Devralinmaz —
            # yalnizca zararsiz alanlar beyaz listeyle tasinir, gerisi dusurulur.
            eski_meta = veri.get("meta") if isinstance(veri.get("meta"), dict) else {}
            veri["meta"] = {
                "owner": an.takma_kisi(),
                "email": an.profil.get("atalay.denizer0@gmail.com", "ornek@ornek.example"),
                "schema_version": eski_meta.get("schema_version", 1),
                # Tarihler veriden türetilir. Devralınan eski bir last_scan,
                # panoyu verinin gerisinde bir "bugün"le üretir ve sessizlik
                # günleri negatife düşer — ürün bozuk görünür.
                "scan_window": {"from": _ilk_tarih(veri["applications"]),
                                "to": _son_tarih(veri["applications"])},
                "last_scan": _son_tarih(veri["applications"]),
                "anonim": True,
                "_uyari": "DEMO VERİ — şirket adları kurgusaldır. Gerçek sürüm özel "
                          "depodadır. Yapı, tarih, aşama ve puanlar korunmuştur.",
            }
        elif isinstance(veri, dict):
            # Liste anahtari dosyadan dosyaya degisiyor; hangisi varsa o kullanilir.
            anahtar = next((k for k in ("jobs", "saved_jobs")
                            if isinstance(veri.get(k), list)), None)
            if anahtar is None:
                print(f"HATA: {ad} icinde liste anahtari bulunamadi.", file=sys.stderr)
                return 1
            veri = {**veri, anahtar: [an.kayit(x) if isinstance(x, dict) and "company" in x
                                      else an.metin(x) for x in veri[anahtar]]}
            veri = {k: (an.metin(v) if isinstance(v, str) else v) for k, v in veri.items()}
        else:
            veri = [an.kayit(x) if isinstance(x, dict) and "company" in x else x for x in veri]
        cikti[ad] = veri

    if an.gorulmeyen:
        print("\nDURDU — eşlemesi olmayan şirket var. Hiçbir dosyaya yazılmadı.\n", file=sys.stderr)
        for s in sorted(an.gorulmeyen):
            print(f"  {s}", file=sys.stderr)
        print(f"\n{esleme_yolu} içindeki 'sirketler' tablosuna takma ad ekle, "
              "sonra tekrar çalıştır.", file=sys.stderr)
        return 1

    toplam = len(cikti.get("applications.json", {}).get("applications", []))
    print(f"{toplam} başvuru anonimleştirildi · {len(an.sirketler)} şirket eşlemesi kullanıldı")

    if not a.yaz:
        print("\n(kuru çalışma — dosyaya dokunulmadı; yazmak için --yaz)")
        return 0

    for ad, veri in cikti.items():
        (hedef / ad).write_text(json.dumps(veri, ensure_ascii=False, indent=2) + "\n",
                                encoding="utf-8")
        print(f"  yazıldı: {hedef/ad}")

    bulgular = dogrula(hedef, an.yasakli)
    if bulgular:
        print("\nDOĞRULAMA BAŞARISIZ — çıktıda gerçek ad kaldı:\n", file=sys.stderr)
        for dosya, kotu in bulgular:
            print(f"  {dosya}: {kotu!r}", file=sys.stderr)
        print("\nBU VERİYİ COMMIT ETME.", file=sys.stderr)
        return 1

    print(f"\nDoğrulandı: {hedef} içinde gerçek ad yok "
          f"({len(an.yasakli)} yasaklı dizi tarandı, elle bakılan dosyalar dahil).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
