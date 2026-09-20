"""Veri okuma, şema denetimi ve ortak tarih/durum tanımları.

TRACE_DATA her çağrıda okunur; aynı süreçte profil değiştirmek eski veriyi
önbellekten getirmez. Özel veri eksikse demo veriye sessizce dönülmez.
"""
import json
import math
import os
import re
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
STAGE_WEIGHT = {
    "offer": 100, "interview_scheduling": 88, "assessment": 85,
    "next_stage": 82, "interviewed": 78, "application_incomplete": 70,
    "in_process": 60, "under_review": 35, "talent_pool": 20, "closed": 0,
}
STATUSES = {"action_required", "in_progress", "awaiting_response", "stale", "rejected"}
CHANNELS = {"ats", "linkedin", "direct", "aggregator", "indeed"}
MAX = {"role_family": 35, "seniority": 25, "skills": 25, "domain": 15}
ADVANCED_STAGES = {"interviewed", "interview_scheduling", "next_stage", "assessment", "offer"}
AYLAR = ("Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara")


def veri_dizini():
    return Path(os.environ.get("TRACE_DATA") or ROOT / "data").resolve()


def oku(name):
    path = veri_dizini() / name
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Veri dosyası bulunamadı: {name}. TRACE_DATA klasörünü kontrol et.") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Geçersiz JSON: {name}, satır {exc.lineno}.") from exc


def parse_date(value):
    if value is None or value == "":
        return None
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError("Tarih YYYY-MM-DD biçiminde olmalı.")
    return date.fromisoformat(value)


def kapali(app):
    return app.get("status") == "rejected" or app.get("stage") == "closed"


def yanit_var(app):
    """Açık kanıtı kullan; yalnızca son temas tarihinden yanıt tahmin etme."""
    if app.get("first_response"):
        return True
    if isinstance(app.get("response_received"), bool):
        return app["response_received"]
    return app.get("stage") in ADVANCED_STAGES or app.get("status") == "rejected"


def guvenli_url(value, kind=None):
    if not isinstance(value, str) or any(ord(c) < 32 for c in value):
        return False
    try:
        parsed = urlsplit(value)
        if parsed.username or parsed.password:
            return False
        if kind == "mailto":
            return parsed.scheme == "mailto" and bool(parsed.path)
        if kind == "gmail":
            return parsed.scheme == "https" and parsed.hostname == "mail.google.com"
        return parsed.scheme == "https" and bool(parsed.hostname)
    except ValueError:
        return False


def sayi(value):
    return type(value) in (int, float) and math.isfinite(value)


def match_hatalari(m, yer="match"):
    if m is None:
        return []
    if not isinstance(m, dict):
        return [f"{yer}: nesne veya null olmalı."]
    errors = []
    for key, maximum in MAX.items():
        if not sayi(m.get(key)) or not 0 <= m[key] <= maximum:
            errors.append(f"{yer}.{key}: 0–{maximum} arası sayı olmalı.")
    if not sayi(m.get("location_mod")) or m["location_mod"] > 0:
        errors.append(f"{yer}.location_mod: sıfır veya negatif sayı olmalı.")
    if not isinstance(m.get("rationale"), str) or not m["rationale"].strip():
        errors.append(f"{yer}.rationale: boş olmayan gerekçe gerekli.")
    return errors


def basvuru_hatalari(data, catalog=None):
    if not isinstance(data, dict) or not isinstance(data.get("applications"), list):
        return ["applications: başvuru listesi gerekli."]
    errors, ids = [], set()
    meta = data.get("meta")
    if not isinstance(meta, dict):
        errors.append("meta: kaynak ve tarama bilgisi gerekli.")
    else:
        for key in ("owner", "email"):
            if not isinstance(meta.get(key), str):
                errors.append(f"meta.{key}: metin gerekli.")
        window = meta.get("scan_window")
        if not isinstance(window, dict) or not {"from", "to"} <= window.keys():
            errors.append("meta.scan_window: from/to alanları gerekli.")
        else:
            for key, value in (("last_scan", meta.get("last_scan")), ("scan_window.from", window["from"]), ("scan_window.to", window["to"])):
                try:
                    parse_date(value)
                except ValueError:
                    errors.append(f"meta.{key}: geçerli tarih veya null gerekli.")
    required = {"id", "company", "role", "channel", "applied", "last_contact", "stage",
                "status", "track", "fit", "deadline", "next_step", "notes", "match",
                "gap_skills", "links_actions"}
    for index, app in enumerate(data["applications"]):
        yer = f"applications[{index}]"
        if not isinstance(app, dict):
            errors.append(f"{yer}: nesne olmalı.")
            continue
        for key in sorted(required - app.keys()):
            errors.append(f"{yer}.{key}: alan eksik; bilinmeyen değer için null kullan.")
        ident = app.get("id")
        if not isinstance(ident, str) or not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", ident):
            errors.append(f"{yer}.id: küçük harf, rakam, tire veya alt çizgi kullan.")
        elif ident in ids:
            errors.append(f"{yer}.id: yinelenen kayıt kimliği.")
        else:
            ids.add(ident)
        for key in ("company", "role"):
            if not isinstance(app.get(key), str) or not app[key].strip():
                errors.append(f"{yer}.{key}: boş olmayan metin gerekli.")
        for key in ("track", "next_step", "notes", "location", "contact"):
            if app.get(key) is not None and not isinstance(app[key], str):
                errors.append(f"{yer}.{key}: metin veya null olmalı.")
        for key, allowed in (("stage", STAGE_WEIGHT), ("status", STATUSES), ("channel", CHANNELS)):
            if not isinstance(app.get(key), str) or app[key] not in allowed:
                errors.append(f"{yer}.{key}: tanınmayan değer.")
        fit = app.get("fit")
        if fit is not None and (type(fit) is not int or not 1 <= fit <= 5):
            errors.append(f"{yer}.fit: 1–5 arası tam sayı veya null olmalı.")
        dates = {}
        for key in ("applied", "last_contact", "deadline", "first_response"):
            try:
                dates[key] = parse_date(app.get(key))
            except ValueError:
                errors.append(f"{yer}.{key}: geçerli YYYY-MM-DD veya null gerekli.")
        for key in ("last_contact", "first_response"):
            if dates.get(key) and dates.get("applied") and dates[key] < dates["applied"]:
                errors.append(f"{yer}.{key}: başvuru tarihinden önce olamaz.")
        if dates.get("first_response") and dates.get("last_contact") and dates["first_response"] > dates["last_contact"]:
            errors.append(f"{yer}.first_response: son temastan sonra olamaz.")
        if app.get("response_received") is not None and type(app["response_received"]) is not bool:
            errors.append(f"{yer}.response_received: true, false veya null olmalı.")
        if app.get("response_received") is False and (dates.get("first_response") or (isinstance(app.get("stage"), str) and app["stage"] in ADVANCED_STAGES) or app.get("status") == "rejected"):
            errors.append(f"{yer}.response_received: kayıtlı yanıt/aşama ile çelişiyor.")
        errors.extend(match_hatalari(app.get("match"), yer + ".match"))
        gaps = app.get("gap_skills")
        if not isinstance(gaps, list) or any(not isinstance(g, str) for g in gaps):
            errors.append(f"{yer}.gap_skills: metin listesi gerekli; eksik yoksa [].")
        elif catalog is not None:
            for gap in gaps:
                if gap not in catalog.get("skills", {}):
                    errors.append(f"{yer}.gap_skills: katalogda olmayan beceri.")
        links = app.get("links_actions")
        if not isinstance(links, list):
            errors.append(f"{yer}.links_actions: liste gerekli; bağlantı yoksa [].")
        else:
            for n, link in enumerate(links):
                if not isinstance(link, dict) or not isinstance(link.get("label"), str) or not link["label"].strip() or not isinstance(link.get("kind"), str) or link.get("kind") not in ("mailto", "gmail", "ext") or not guvenli_url(link.get("url"), link.get("kind")):
                    errors.append(f"{yer}.links_actions[{n}]: geçerli label/kind/url gerekli.")
    return errors


def basvurulari_dogrula(data, catalog=None):
    errors = basvuru_hatalari(data, catalog)
    if errors:
        raise ValueError("Veri doğrulanamadı:\n" + "\n".join(errors))
    return data


def haftalik_gruplar(apps):
    """ISO hafta başlangıcına göre gruplar; bilinmeyen tarihler sayılmaz."""
    groups = {}
    for app in apps:
        day = parse_date(app.get("applied"))
        if day is None:
            continue
        start = day - timedelta(days=day.weekday())
        groups.setdefault(start, []).append(app)
    out = []
    for start, items in sorted(groups.items()):
        end = start + timedelta(days=6)
        label = f"{start.day} {AYLAR[start.month-1]} {start.year} – {end.day} {AYLAR[end.month-1]} {end.year}"
        out.append({"label": label, "start": start.isoformat(), "end": end.isoformat(), "items": items})
    return out


if __name__ == "__main__":
    import sys
    try:
        data = basvurulari_dogrula(oku("applications.json"), oku("skills_catalog.json"))
    except ValueError as exc:
        sys.exit(str(exc))
    print(f"Doğrulandı: {len(data['applications'])} başvuru.")
