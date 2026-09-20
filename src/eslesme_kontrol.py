#!/usr/bin/env python3
"""Ajanın JSON çıktısını stdin'den doğrula; hiçbir veri dosyasına yazma."""
import json
import sys

from match import score_match
from veri import oku


def dogrula(proposal, catalog):
    if not isinstance(proposal, dict) or "match" not in proposal:
        raise ValueError("match alanı içeren JSON nesnesi gerekli.")
    result = score_match({"match": proposal["match"]})
    gaps = proposal.get("gap_skills")
    if not isinstance(gaps, list) or any(not isinstance(g, str) or g not in catalog["skills"] for g in gaps):
        raise ValueError("gap_skills kataloğun anahtarlarından oluşmalı.")
    if result is None:
        if proposal.get("hesaplanan_toplam") is not None or proposal.get("segment") is not None:
            raise ValueError("Puanlanamayan ilan için toplam ve segment null olmalı.")
    elif proposal.get("hesaplanan_toplam") != result["score"] or proposal.get("segment") != result["segment_key"]:
        raise ValueError("Ajanın toplamı veya segmenti hesaplamayla uyuşmuyor.")
    if proposal.get("guven") not in ("yuksek", "orta", "dusuk"):
        raise ValueError("guven: yuksek, orta veya dusuk olmalı.")
    return {"gecerli": True, "match_result": result}


def main():
    try:
        result = dogrula(json.load(sys.stdin), oku("skills_catalog.json"))
    except (ValueError, KeyError) as exc:
        sys.exit(f"Eşleşme doğrulanamadı: {exc}")
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    main()
