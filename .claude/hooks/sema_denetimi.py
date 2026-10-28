#!/usr/bin/env python3
"""PostToolUse hook'u: bir veri klasöründeki JSON değişince şemayı denetler.

Claude Code bu dosyayı bir dosya yazıldıktan ya da düzenlendikten hemen sonra
çalıştırır; model devrede değildir, token harcanmaz. Değişen dosya bir veri
klasöründeyse (yanında applications.json varsa) o klasör `src/veri.py` ile
denetlenir.

Denetim geçerse sessiz kalır. Geçmezse hatayı stderr'e yazıp 2 koduyla çıkar:
Claude Code bu kodu "modele geri bildir" diye okur, yani hata aynı turda
görülür ve düzeltilir — kullanıcının fark etmesini beklemeden.

Neden var: 2026-09-20'de bir kayıtta first_response başvuru tarihinin önüne
düştü. Hatayı veri.py yakaladı ama yalnızca biri onu çalıştırmayı hatırladığı
için. Bu hook hatırlamayı gereksiz kılar.
"""
import json
import os
import pathlib
import subprocess
import sys

PROJE = pathlib.Path(os.environ.get("CLAUDE_PROJECT_DIR")
                     or pathlib.Path(__file__).resolve().parents[2])


def main() -> int:
    try:
        girdi = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    yol = (girdi.get("tool_input") or {}).get("file_path") or ""
    if not yol.endswith(".json"):
        return 0
    klasor = pathlib.Path(yol).resolve().parent
    # Yalnızca gerçek bir Trace veri klasörü: yanında applications.json olmalı.
    # Aksi hâlde rastgele bir data/ klasörü yanlış alarm üretir.
    if not (klasor / "applications.json").is_file():
        return 0

    sonuc = subprocess.run(
        [sys.executable, str(PROJE / "src" / "veri.py")],
        env={**os.environ, "TRACE_DATA": str(klasor)},
        capture_output=True, text=True, timeout=60,
    )
    if sonuc.returncode == 0:
        return 0
    hata = (sonuc.stderr or sonuc.stdout).strip()
    print(f"Şema denetimi başarısız — {klasor}:\n{hata}\n"
          "Kaydı düzelt; bu hâliyle commit etme.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
