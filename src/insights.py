#!/usr/bin/env python3
"""
Rapor ve eğitim verisi üreticisi.

Raporlar
--------
funnel()            Kaydedilen → başvurulan → yanıt → ileri aşama → sonuç hunisi
skill_gaps()        Çıkarımsal eksik yetkinlik analizi (red gerekçesi DEĞİL — aşağıdaki nota bak)
trend()             Haftalık başvuru hacmi ve sonuç dağılımı
track_success()     Rol/sektör bazlı ilerleme ve red oranı
channel_success()   Başvuru kanalı bazlı etkinlik
response_speed()    Şirketlerin yanıt süresi dağılımı
missed()            Kaydedilip başvurulmayan / süresi dolan fırsatlar
engagement()        Kullanım sıklığı, streak ve yaşam döngüsü aşaması
learning_plan()     Eksiklerden türeyen öncelikli eğitim planı

Eksik yetkinlik verisi hakkında
-------------------------------
Taranan 15 red e-postasının HİÇBİRİ gerekçe belirtmiyor; hepsi standart
kalıp metin. Bu yüzden "eksik yetkinlik", şirketlerin söylediği bir şey
değil, ilanın rol ailesi ile CV arasındaki farktan ÇIKARILAN bir tahmindir.
Arayüzde de bu şekilde etiketlenir.
"""

from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from statistics import median

from veri import (ADVANCED_STAGES, oku, parse_date as _d, kapali, yanit_var,
                  haftalik_gruplar, basvurulari_dogrula)

INTERVIEW_STAGES = ("interviewed", "interview_scheduling")
_load = oku


# ---------------------------------------------------------------- huni

def funnel(apps, saved):
    jobs = saved["jobs"]
    responded = [a for a in apps if yanit_var(a)]
    advanced = [a for a in apps if a.get("stage") in ADVANCED_STAGES]
    interviewed = [a for a in apps if a.get("stage") in INTERVIEW_STAGES]
    rejected = [a for a in apps if a["status"] == "rejected"]
    offers = [a for a in apps if a.get("stage") == "offer"]

    total = len(apps)
    steps = [
        {"key": "saved", "label": "Kaydedilen ilan", "value": len(jobs),
         "note": "LinkedIn hatırlatması gelenler — alt sınır, tamamı değil", "partial": True},
        {"key": "applied", "label": "Başvurulan", "value": total,
         "note": "Kaydedilenlerin dışındaki doğrudan başvurular dahil"},
        {"key": "responded", "label": "Yanıt alınan", "value": len(responded),
         "note": "Yanıt tarihi veya yanıt içeren aşama/sonuç kaydı bulunanlar — alt sınır"},
        {"key": "advanced", "label": "İleri aşamaya geçen", "value": len(advanced),
         "note": "Güncel aşaması test, sonraki aşama, mülakat veya teklif olanlar"},
        {"key": "interviewed", "label": "Mülakat aşamasında", "value": len(interviewed),
         "note": "Görüşme yapılan veya planlanan"},
        {"key": "offer", "label": "Teklif", "value": len(offers), "note": "Güncel teklif kayıtları"},
    ]
    for i, s in enumerate(steps):
        s["pct_of_applied"] = round(100 * s["value"] / total, 1) if i >= 1 and total else None
        # Kaydedilen ilan sayısı yalnızca alt sınır olduğu için ondan sonraki
        # adıma dönüşüm oranı hesaplanmaz — yanıltıcı olurdu.
        # Aşamalar geçmiş olaylar değil anlık durumdur; ardışık dönüşüm
        # gibi sunmak teklif/mülakat kayıtlarında yanıltıcı oran üretir.
        s["conv_from_prev"] = (round(100 * s["value"] / total, 1)
                               if s["key"] == "responded" and total else None)

    return {
        "steps": steps,
        "rejected": len(rejected),
        "reject_rate": round(100 * len(rejected) / total, 1) if total else 0,
        "pending": sum(not kapali(a) and a.get("stage") != "offer" for a in apps),
        "caveat": "'Görüntülenen ilan' verisi yok — LinkedIn bunu e-postayla bildirmiyor. "
                  "Kaydedilenler alt sınırdır. Aşamalar anlık durumdur; aşamalar arası "
                  "geçiş ve geçmiş mülakat sayısı olay geçmişi olmadan ölçülemez.",
    }


# ---------------------------------------------------------------- eksik yetkinlik

def skill_gaps(apps, catalog):
    total_c = Counter()
    reject_c = Counter()
    open_c = Counter()
    by_skill_apps = defaultdict(list)

    for a in apps:
        for s in dict.fromkeys(a.get("gap_skills", [])):
            total_c[s] += 1
            by_skill_apps[s].append({"id": a["id"], "company": a["company"], "role": a["role"],
                                     "status": a["status"], "match_score": a.get("match_score")})
            if a["status"] == "rejected":
                reject_c[s] += 1
            elif not kapali(a):
                open_c[s] += 1

    rows = []
    for skill, n in total_c.most_common():
        meta = catalog["skills"].get(skill, {})
        # Öncelik: redlerde görülmesi, açık süreçleri etkilemesi ve kapanması gereken seviye farkı
        level_gap = max(0, meta.get("target_level", 0) - meta.get("cv_level", 0))
        priority = reject_c[skill] * 3 + open_c[skill] * 1 + level_gap * 2
        rows.append({
            "skill": skill,
            "name": meta.get("name", skill),
            "why": meta.get("why", ""),
            "effort": meta.get("effort"),
            "caveat": meta.get("caveat"),
            "cv_level": meta.get("cv_level"),
            "target_level": meta.get("target_level"),
            "total": n, "rejected": reject_c[skill], "open": open_c[skill],
            "priority": priority,
            "resources": meta.get("resources", []),
            "applications": sorted(by_skill_apps[skill],
                                   key=lambda x: -(x["match_score"] or 0))[:6],
        })
    rows.sort(key=lambda r: (-r["priority"], -r["total"], r["skill"]))
    return {
        "rows": rows,
        "basis": "ÇIKARIM — eksikler kayıtlı ilan/profil değerlendirmelerinden gelir; "
                 "işverenin red gerekçesi veya nedensellik kanıtı değildir.",
    }


# ---------------------------------------------------------------- trend

def trend(apps):
    return [{"label": group["label"], "start": group["start"], "end": group["end"],
             "applied": len(group["items"]),
             "rejected": sum(a["status"] == "rejected" for a in group["items"]),
             "advanced": sum(a.get("stage") in ADVANCED_STAGES for a in group["items"])}
            for group in haftalik_gruplar(apps)]


# ---------------------------------------------------------------- rol / kanal başarısı

def _group_success(apps, key, min_n=2):
    g = defaultdict(list)
    for a in apps:
        g[a.get(key) or "—"].append(a)
    rows = []
    for name, items in g.items():
        if len(items) < min_n:
            continue
        adv = [x for x in items if x.get("stage") in ADVANCED_STAGES]
        rej = [x for x in items if x["status"] == "rejected"]
        ms = [x["match_score"] for x in items if x.get("match_score") is not None]
        rows.append({
            "name": name, "count": len(items),
            "advanced": len(adv), "rejected": len(rej),
            "advance_rate": round(100 * len(adv) / len(items), 1),
            "reject_rate": round(100 * len(rej) / len(items), 1),
            "avg_match": round(sum(ms) / len(ms)) if ms else None,
        })
    rows.sort(key=lambda r: (-r["advance_rate"], -r["count"]))
    return rows


def track_success(apps):
    return _group_success(apps, "track", min_n=2)


def channel_success(apps):
    return _group_success(apps, "channel", min_n=1)


# ---------------------------------------------------------------- yanıt hızı

def response_speed(apps):
    buckets = [("0-3 gün", 0, 3), ("4-7 gün", 4, 7), ("8-14 gün", 8, 14),
               ("15-21 gün", 15, 21), ("22+ gün", 22, float("inf"))]
    out = [{"label": b[0], "value": 0} for b in buckets]
    days = []
    for app in apps:
        applied = _d(app.get("applied"))
        first = _d(app.get("first_response"))
        if not applied or not first or first < applied:
            continue
        n = (first - applied).days
        days.append(n)
        for index, (_, low, high) in enumerate(buckets):
            if low <= n <= high:
                out[index]["value"] += 1
                break
    responded = sum(yanit_var(a) for a in apps)
    return {"buckets": out, "median_days": median(days) if days else None,
            "measured": len(days), "responded": responded,
            "silent": len(apps) - responded,
            "basis": "Yalnızca first_response tarihi bilinen kayıtlar ölçülür; "
                     "son temas, ilk yanıt tarihi yerine kullanılamaz."}


# ---------------------------------------------------------------- kaçırılanlar

def missed(saved):
    jobs = saved["jobs"]
    not_applied = [j for j in jobs if not j["applied"]]
    expired = [j for j in not_applied if j["expired"]]
    strong = [j for j in not_applied if j.get("match_estimate") is not None and j["match_estimate"] >= 75]
    return {
        "saved_total": len(jobs),
        "applied": sum(1 for j in jobs if j["applied"]),
        "not_applied": len(not_applied),
        "expired": expired,
        "strong_missed": sorted(strong, key=lambda j: -(j.get("match_estimate") if j.get("match_estimate") is not None else -1)),
        "all_open": sorted([j for j in not_applied if not j["expired"]],
                           key=lambda j: -(j.get("match_estimate") if j.get("match_estimate") is not None else -1)),
    }


# ---------------------------------------------------------------- kullanım / streak

def engagement(eng, apps, today):
    raw_days = {_d(x) for x in eng.get("report_days", []) if x}
    start = _d(eng.get("tracking_started"))
    if start is None and raw_days:
        start = min(raw_days)
    days = sorted(d for d in raw_days if d <= today and (start is None or d >= start))
    cur = 0
    cursor = today if today in days else today - timedelta(days=1)
    day_set = set(days)
    while cursor in day_set:
        cur += 1
        cursor -= timedelta(days=1)
    longest = run = 0
    for index, day in enumerate(days):
        run = run + 1 if index and (day - days[index - 1]).days == 1 else 1
        longest = max(longest, run)
    span = max(0, (today - start).days + 1) if start else 0
    calendar = [{"date": (start + timedelta(days=i)).isoformat(),
                 "active": (start + timedelta(days=i)) in day_set} for i in range(span)]
    return {"tracking_started": start.isoformat() if start else None,
            "days_tracked": span, "reports_sent": len(days),
            "coverage": round(100 * len(days) / span, 1) if span else 0,
            "current_streak": cur, "longest_streak": longest,
            "missed_days": [c["date"] for c in calendar if not c["active"]],
            "reports_last_7d": sum(0 <= (today - d).days < 7 for d in days),
            "feedback_replies": eng.get("feedback_replies", 0), "calendar": calendar}


def lifecycle_stage(journey, eng_stats, apps, profile_exists):
    n = len(apps)
    streak = eng_stats.get("current_streak", 0)
    fb = eng_stats.get("feedback_replies", 0)
    last7 = eng_stats.get("reports_last_7d", 0)
    reports = eng_stats.get("reports_sent", 0)

    if not profile_exists:
        key = "newcomer"
    elif n == 0:
        key = "activated"
    elif n < 10:
        key = "applying"
    elif streak >= 7 and fb >= 1:
        key = "habit"
    elif last7 >= 4:
        key = "engaged"
    elif reports >= 1:
        key = "tracking"
    else:
        key = "applying"

    stages = journey["stages"]
    cur = next(s for s in stages if s["key"] == key)
    nxt = next((s for s in stages if s["order"] == cur["order"] + 1), None)

    blockers = []
    if key == "engaged":
        if streak < 7:
            blockers.append(f"Kesintisiz streak {streak}/7 gün")
        if fb < 1:
            blockers.append("Henüz hiçbir rapora geri bildirim yazılmadı (0/1)")
    return {"current": cur, "next": nxt, "blockers": blockers,
            "all": [{"key": s["key"], "label": s["label"], "order": s["order"]} for s in stages],
            "nudges": journey["page_nudges"]}


# ---------------------------------------------------------------- eğitim planı

def learning_plan(gaps, catalog):
    """Eksiklerden türeyen, öncelik sıralı eğitim planı. Eğitim sayfası ve
    başvuru detayındaki kurs kartı aynı bu çıktıyı kullanır."""
    plan = []
    for i, row in enumerate(gaps["rows"]):
        plan.append({
            "rank": i + 1,
            "skill": row["skill"], "name": row["name"], "why": row["why"],
            "effort": row["effort"], "caveat": row["caveat"],
            "cv_level": row["cv_level"], "target_level": row["target_level"],
            "affects_total": row["total"], "affects_open": row["open"],
            "seen_in_rejections": row["rejected"],
            "priority": row["priority"],
            "resources": row["resources"],
            "applications": row["applications"],
        })
    return plan


def build_all(today=None):
    today = today or date.today()
    apps_raw = _load("applications.json")
    catalog = _load("skills_catalog.json")
    basvurulari_dogrula(apps_raw, catalog)
    saved = _load("saved_jobs.json")
    eng = _load("engagement.json")
    journey = _load("journey.json")
    profile = _load("profile.json")

    from match import enrich_with_match
    apps = enrich_with_match(apps_raw["applications"])
    for a in apps:
        mr = a.get("match_result") or {}
        a["match_score"] = mr.get("score")
        a["match_segment_key"] = mr.get("segment_key")

    gaps = skill_gaps(apps, catalog)
    eng_stats = engagement(eng, apps, today)
    return {
        "funnel": funnel(apps, saved),
        "skill_gaps": gaps,
        "trend": trend(apps),
        "track_success": track_success(apps),
        "channel_success": channel_success(apps),
        "response_speed": response_speed(apps),
        "missed": missed(saved),
        "engagement": eng_stats,
        "lifecycle": lifecycle_stage(journey, eng_stats, apps, bool(profile)),
        "learning_plan": learning_plan(gaps, catalog),
    }


if __name__ == "__main__":
    import sys
    t = datetime.strptime(sys.argv[1], "%Y-%m-%d").date() if len(sys.argv) > 1 else date.today()
    r = build_all(t)

    print("HUNİ")
    for s in r["funnel"]["steps"]:
        c = f" · önceki adımdan %{s['conv_from_prev']}" if s["conv_from_prev"] is not None else ""
        print(f"  {s['label']:<22} {s['value']:>3}{c}")
    print(f"  ! {r['funnel']['caveat']}")

    print("\nEKSİK YETKİNLİKLER (öncelik sırası)")
    for g in r["learning_plan"][:6]:
        print(f"  {g['rank']}. {g['name']:<28} {g['affects_total']:>2} başvuru "
              f"({g['seen_in_rejections']} red) · öncelik {g['priority']}")

    print("\nKULLANIM")
    e = r["engagement"]
    print(f"  {e['reports_sent']}/{e['days_tracked']} gün (%{e['coverage']}) · "
          f"streak {e['current_streak']} (en uzun {e['longest_streak']}) · "
          f"geri bildirim {e['feedback_replies']}")

    next_stage = r['lifecycle']['next']
    print(f"\nAŞAMA: {r['lifecycle']['current']['label']} → {next_stage['label'] if next_stage else 'Son aşama'}")
    for b in r["lifecycle"]["blockers"]:
        print(f"  eksik: {b}")

    print("\nROL BAZLI BAŞARI (ilk 5)")
    for t_ in r["track_success"][:5]:
        print(f"  {t_['name']:<22} {t_['count']:>2} başvuru · ilerleme %{t_['advance_rate']}")

    print("\nKAÇIRILANLAR")
    m = r["missed"]
    print(f"  {m['not_applied']}/{m['saved_total']} kaydedilen ilana başvurulmamış, "
          f"{len(m['expired'])} tanesinin süresi dolmuş")
    for j in m["strong_missed"]:
        print(f"    [{j['match_estimate']}] {j['company']} — {j['role'][:48]}"
              f"{' (SÜRESİ DOLDU)' if j['expired'] else ''}")
