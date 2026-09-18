#!/usr/bin/env python3
"""Şablondan pano üret. --site yalnızca açık depodaki demo verisini yayıma hazırlar."""
import argparse
import json
import os
import tempfile
from datetime import date
from pathlib import Path

from pipeline import enrich, funnel, STALE_DAYS
from match import segment_summary, load_profile
from veri import ROOT, oku, veri_dizini, parse_date, haftalik_gruplar, kapali
import insights

TEMPLATE = ROOT / "src" / "dashboard.template.html"


def weekly_volume(apps):
    return [{"label": group["label"], "value": len(group["items"])}
            for group in haftalik_gruplar(apps)]


def pipeline_states(apps):
    closed = [a for a in apps if kapali(a)]
    action = [a for a in apps if not kapali(a) and a["status"] == "action_required"]
    stale = [a for a in apps if not kapali(a) and a["status"] != "action_required"
             and (a.get("days_silent") or 0) >= STALE_DAYS]
    active = len(apps) - len(closed) - len(action) - len(stale)
    return [
        {"label": "Aksiyon gerekli", "value": len(action), "tone": "critical", "icon": "!"},
        {"label": "Aktif / yanıt bekleniyor", "value": active, "tone": "good", "icon": "→"},
        {"label": "Sessizleşen (12+ gün)", "value": len(stale), "tone": "warning", "icon": "~"},
        {"label": "Kapanan", "value": len(closed), "tone": "archive", "icon": "×"},
    ]


def html_uret(payload):
    # JSON'daki </script> HTML ayrıştırıcısını kapatabilir. JSON geçerli kalır,
    # fakat kullanıcı metni yeni bir script/etiket oluşturamaz.
    encoded = json.dumps(payload, ensure_ascii=False, allow_nan=False)
    for char, escaped in (("<", "\\u003c"), (">", "\\u003e"), ("&", "\\u0026"),
                          ("\u2028", "\\u2028"), ("\u2029", "\\u2029")):
        encoded = encoded.replace(char, escaped)
    template = TEMPLATE.read_text(encoding="utf-8")
    marker = "/*__DATA__*/null"
    if template.count(marker) != 1:
        raise ValueError("Şablonda tam bir veri işareti olmalı.")
    return template.replace(marker, encoded)


def payload_uret(today, public_demo=False):
    data = oku("applications.json")
    if public_demo:
        if veri_dizini() != (ROOT / "data").resolve():
            raise ValueError("--site özel TRACE_DATA klasörüyle kullanılamaz.")
        if "DEMO" not in data.get("meta", {}).get("_uyari", ""):
            raise ValueError("--site için açıkça etiketlenmiş demo verisi gerekli.")
    apps = enrich(data, today)
    fields = ("id", "company", "role", "stage", "status", "band", "score", "closed",
              "channel", "track", "location", "applied", "last_contact", "deadline",
              "days_silent", "days_to_deadline", "next_step", "reminders", "match_score",
              "match_segment", "match_segment_key", "match_rationale", "match_weakest",
              "gap_skills", "contact", "notes")
    payload = {
        "generated": today.isoformat(), "demo": public_demo,
        "meta": data["meta"], "stats": funnel(apps),
        "weekly": weekly_volume(apps), "states": pipeline_states(apps),
        "profile": load_profile(), "insights": insights.build_all(today),
        "catalog": oku("skills_catalog.json"), "role_targets": oku("role_targets.json"),
        "segments": segment_summary(apps),
        "applications": [dict({key: a.get(key) for key in fields},
                              links_actions=[] if public_demo else a.get("links_actions", []),
                              match_breakdown=(a.get("match_result") or {}).get("breakdown", []))
                         for a in apps],
        "outreach": [] if public_demo else data.get("recruiter_outreach", []),
    }
    if public_demo:
        for app in payload["applications"]:
            app["contact"] = None
    return payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("today", nargs="?", help="YYYY-MM-DD; özel pano için varsayılan bugün")
    parser.add_argument("--site", action="store_true", help="Demo verisinden site/app.html üret")
    parser.add_argument("--out", type=Path, help="Özel pano çıktı yolu; --site ile kullanılmaz")
    args = parser.parse_args()
    if args.site and (args.out or args.today):
        parser.error("--site tarihi demo taramasından alır; tarih/--out ile birleştirilmez.")
    if args.site and veri_dizini() != (ROOT / "data").resolve():
        parser.error("--site özel TRACE_DATA ile kullanılamaz; önce demo veri klasörünü seç.")
    out = (ROOT / "site" / "app.html") if args.site else (args.out or ROOT / "reports" / "pano.html")
    out = out.resolve()
    if not args.site and out.is_relative_to(ROOT) and out != (ROOT / "reports" / "pano.html"):
        parser.error("Repo içinde özel pano yalnızca reports/pano.html olabilir; site için --site kullan.")
    try:
        today = (parse_date(oku("applications.json")["meta"]["last_scan"]) if args.site
                 else parse_date(args.today) if args.today else date.today())
        if today is None:
            raise ValueError("Pano için referans tarihi gerekli.")
        html = html_uret(payload_uret(today, public_demo=args.site))
    except (ValueError, KeyError) as exc:
        parser.error(str(exc))
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=out.parent, delete=False) as tmp:
        tmp.write(html)
        temp_path = Path(tmp.name)
    try:
        os.replace(temp_path, out)
    finally:
        temp_path.unlink(missing_ok=True)
    print(f"Yazıldı: {out}")


if __name__ == "__main__":
    main()
