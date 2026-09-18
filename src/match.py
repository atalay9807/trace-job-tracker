#!/usr/bin/env python3
"""
CV ↔ ilan eşleşme motoru.

Her başvurunun önceden değerlendirilmiş `match` boyutlarını doğrular,
toplayıp 0–100 eşleşme puanı ve segment üretir. Profil yalnızca CLI özetinde
okunur; bu modül CV veya ilan metni yorumlamaz.

Boyutlar
--------
rol_ailesi   0-35  Rolün, profilin çekirdek iş ailelerine yakınlığı
                   (growth analitiği, FP&A, ticari strateji, iş/veri analizi)
kıdem        0-25  İlanın kıdem bandı ile 2 yıllık Specialist seviyesinin uyumu
beceri       0-25  İlanın beklediği araç/teknik setin CV ile örtüşmesi
sektör       0-15  Sektörün q-commerce/e-ticaret deneyimine yakınlığı
lokasyon     ≤0    Taşınma, uzaktan çalışma izni veya dil engeli cezası

Segmentler
----------
🟢 Güçlü   78-100  Öncelikli kovala, takip maili at
🔵 İyi     62-77   Sağlam aday, süreci canlı tut
🟡 Orta    45-61   Kısmi uyum — sadece boş zaman kalırsa
🔴 Zayıf    0-44   Düşük getiri, kapatmayı düşün
"""

from veri import MAX, ADVANCED_STAGES, oku, match_hatalari, basvurulari_dogrula

SEGMENTS = [
    (78, "strong", "🟢 Güçlü eşleşme",  "Öncelikli kovala — takip maili at, hazırlık yap."),
    (62, "good",   "🔵 İyi eşleşme",    "Sağlam aday; süreci canlı tut."),
    (45, "fair",   "🟡 Orta eşleşme",   "Kısmi uyum — zaman kalırsa ilerlet."),
    (0,  "weak",   "🔴 Zayıf eşleşme",  "Düşük getiri; kapatmayı değerlendir."),
]

DIM_TR = {"role_family": "Rol ailesi", "seniority": "Kıdem",
          "skills": "Beceri örtüşmesi", "domain": "Sektör yakınlığı"}


def load_profile():
    return oku("profile.json")


def score_match(app):
    """Bir başvurunun eşleşme skorunu ve dökümünü döndürür."""
    m = app.get("match")
    errors = match_hatalari(m)
    if errors:
        raise ValueError("\n".join(errors))
    if m is None:
        return None
    raw = sum(m.get(k, 0) for k in MAX)
    total = max(0, min(100, raw + m.get("location_mod", 0)))

    for threshold, key, label, advice in SEGMENTS:
        if total >= threshold:
            segment, seg_key, seg_advice = label, key, advice
            break

    # En zayıf boyut — neyin eksik olduğunu tek bakışta göstermek için
    ratios = {k: m.get(k, 0) / MAX[k] for k in MAX}
    weakest = min(ratios, key=ratios.get)

    return {
        "score": total,
        "raw": raw,
        "segment": segment,
        "segment_key": seg_key,
        "advice": seg_advice,
        "location_mod": m.get("location_mod", 0),
        "breakdown": [
            {"dim": k, "label": DIM_TR[k], "value": m.get(k, 0),
             "max": MAX[k], "pct": round(100 * ratios[k])}
            for k in ("role_family", "seniority", "skills", "domain")
        ],
        "weakest": DIM_TR[weakest],
        "rationale": m.get("rationale", ""),
    }


def enrich_with_match(apps):
    """Kaynak kayıtları değiştirmeden türetilmiş sonuç ekle."""
    return [dict(app, match_result=score_match(app)) for app in apps]


def segment_summary(apps):
    """Segment bazlı dağılım + her segmentin ortalama başvuru sonucu."""
    out = {}
    for key, label in [("strong", "🟢 Güçlü"), ("good", "🔵 İyi"),
                       ("fair", "🟡 Orta"), ("weak", "🔴 Zayıf")]:
        group = [a for a in apps if (a.get("match_result") or {}).get("segment_key") == key]
        rejected = [a for a in group if a["status"] == "rejected"]
        advanced = [a for a in group if a.get("stage") in ADVANCED_STAGES]
        out[key] = {
            "label": label,
            "count": len(group),
            "rejected": len(rejected),
            "advanced": len(advanced),
            "advance_rate": round(100 * len(advanced) / len(group), 1) if group else 0.0,
            "reject_rate": round(100 * len(rejected) / len(group), 1) if group else 0.0,
        }
    return out


if __name__ == "__main__":
    data = basvurulari_dogrula(oku("applications.json"))
    apps = enrich_with_match(data["applications"])
    # İlan metni olmayan kayıtlarda match=null; puanlananları ayrı tut,
    # puanlanmayanı sıfır sayıp listeye karıştırma.
    puanli = [a for a in apps if a.get("match_result")]
    puansiz = [a for a in apps if not a.get("match_result")]
    puanli.sort(key=lambda a: -a["match_result"]["score"])
    prof = load_profile() or {}

    print(f"Profil: {prof.get('name', '—')} — {prof.get('headline', 'Profil eklenmedi')}")
    seniority = prof.get('seniority') or {}
    print(f"Kıdem: {seniority.get('current_title', '—')} · "
          f"{seniority.get('years_professional', '—')} yıl\n")

    for key, s in segment_summary(puanli).items():
        print(f"{s['label']:<12} {s['count']:>2} başvuru · "
              f"ileri aşamaya geçen %{s['advance_rate']:<5} · red %{s['reject_rate']}")

    print("\nEn iyi 12 eşleşme:")
    for a in puanli[:12]:
        r = a["match_result"]
        print(f"  {r['score']:>3}  {r['segment'][:2]}  {a['company']:<26} {a['role'][:44]}")

    print("\nEn zayıf 6 eşleşme:")
    for a in puanli[-6:]:
        r = a["match_result"]
        print(f"  {r['score']:>3}  {r['segment'][:2]}  {a['company']:<26} {a['role'][:44]}")

    if puansiz:
        print(f"\nPuanlanmadı ({len(puansiz)}) — ilan metni yok, dört boyut hesaplanamıyor:")
        for a in puansiz:
            print(f"       —   {a['company']:<26} {a['role'][:44]}")
