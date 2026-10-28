#!/usr/bin/env python3
"""PreToolUse hook'u: açık depoya gerçek şirket ya da kişi adı yazılmasını engeller.

Claude Code bu dosyayı bir dosya yazılmadan ya da düzenlenmeden ÖNCE çalıştırır.
Yazılacak metinde eşleme tablosundaki gerçek bir ad varsa yazma reddedilir —
dosya hiç değişmez. Açık depoya giren gerçek veri geri alınamaz (git geçmişinde
kalır, klonlanmış olabilir), bu yüzden kontrol sonradan değil önceden yapılır.

Yasaklı adlar burada YAZILMAZ: bu dosya açık depoda duruyor, gerçek adları
içerirse kendisi sızıntı olur. Liste özel depodaki eşleme tablosundan, aynı
`Anonimlestirici` sınıfıyla üretilir — anonimleştiricinin doğrulayıcısıyla bu
kalkan hep aynı listeye bakar, ikisi ayrışamaz.

Sınırları:
- Yalnızca Write/Edit araçlarını görür. Bir kabuk komutuyla yapılan kopyalama
  (cp, python betiği) buradan geçmez; onu anonimleştiricinin kendi doğrulaması
  ve commit öncesi tarama yakalar.
- Eşleme tablosu bulunamazsa (özel depo bu oturuma bağlı değilse) denetim
  yapamaz. O durumda yazmayı engellemez ama bunu açıkça bildirir — sessizce
  "temiz" demez.
- Proje sahibinin adı yazar künyesi olarak açık depoda kasıtlı yer alır
  (README, tanıtım sayfası); o ad yasaklı listeden çıkarılır.
"""
import json
import os
import pathlib
import re
import sys
import urllib.parse

PROJE = pathlib.Path(os.environ.get("CLAUDE_PROJECT_DIR")
                     or pathlib.Path(__file__).resolve().parents[2]).resolve()
sys.path.insert(0, str(PROJE / "src"))
from anonimlestir import Anonimlestirici  # noqa: E402

KUNYE = {"Atalay Denizer", "Atalay", "Denizer", "DENİZER"}
HARF = "0-9A-Za-zÇĞİÖŞÜçğıöşü"


def esleme_yolu() -> pathlib.Path | None:
    adaylar = []
    if os.environ.get("TRACE_ESLESME"):
        adaylar.append(pathlib.Path(os.environ["TRACE_ESLESME"]))
    if os.environ.get("TRACE_DATA"):
        adaylar.append(pathlib.Path(os.environ["TRACE_DATA"]).parent
                       / "anonimlestirme" / "eslesme.json")
    adaylar += [PROJE.parent / "trace-data" / "anonimlestirme" / "eslesme.json",
                pathlib.Path("/tmp/trace-data/anonimlestirme/eslesme.json")]
    return next((a for a in adaylar if a.is_file()), None)


def yazilacak_metin(girdi: dict) -> str:
    ti = girdi.get("tool_input") or {}
    parcalar = [ti.get("content"), ti.get("new_string")]
    parcalar += [e.get("new_string") for e in ti.get("edits") or [] if isinstance(e, dict)]
    return "\n".join(p for p in parcalar if isinstance(p, str))


def cikti(veri: dict) -> int:
    print(json.dumps(veri, ensure_ascii=False))
    return 0


def main() -> int:
    try:
        girdi = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    yol = (girdi.get("tool_input") or {}).get("file_path") or ""
    if not yol:
        return 0
    hedef = pathlib.Path(yol).resolve()
    # Yalnızca açık depoya yazılanlar denetlenir. Özel depo zaten gerçek veri yeridir.
    if PROJE not in hedef.parents:
        return 0

    esleme = esleme_yolu()
    if esleme is None:
        return cikti({"systemMessage":
            "Gerçek veri kalkanı: eşleme tablosu bulunamadı, bu yazma DENETLENMEDİ. "
            "Özel depo (trace-data) oturuma bağlı değilse kalkan çalışamaz."})

    an = Anonimlestirici(json.load(esleme.open(encoding="utf-8")))
    yasakli = [k for k in an.yasakli if k not in KUNYE]
    metin = yazilacak_metin(girdi)
    # mailto/gmail bağlantılarında ad URL-encoded durur; çözülmüş hâli de taranır.
    govdeler = (metin, urllib.parse.unquote(metin))
    bulunan = sorted({k for k in yasakli for g in govdeler
                      if re.search(f"(?<![{HARF}]){re.escape(k)}(?![{HARF}])", g)})
    if not bulunan:
        return 0

    goreli = hedef.relative_to(PROJE)
    return cikti({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason":
            f"Gerçek veri kalkanı: {goreli} açık depoda ve yazılacak metin "
            f"gerçek ad içeriyor: {', '.join(bulunan)}. Takma adı kullan "
            f"(src/anonimlestir.py), ya da bu veri özel depoya aitse oraya yaz.",
    }})


if __name__ == "__main__":
    sys.exit(main())
