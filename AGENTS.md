# Trace — Codex çalışma kuralları

Önce `docs/collaboration.md` dosyasını oku. Claude Code aynı sözleşmeyi
`CLAUDE.md` üzerinden kullanır. Ürün bağlamı için README ve docs/technical-contract.md'ye bak.

- Kullanıcıyla, arayüzde ve yeni dokümantasyonda Türkçe kullan.
- Onaylanmış işi ayrı geliştirme dalında tamamla; aynı dosyalara paralel yazma.
- Demo ve gerçek veri ayrımını, TRACE_DATA seçimini ve ölçüm sınırlarını koru.
- Şablonu düzenle; türetilen siteyi `python3 src/build_dashboard.py --site` ile üret.
- Değişen davranışı anlamlı testlerle doğrula; çalıştırılmayan testi geçti sayma.
- `.claude/agents/` rol tanımlarıdır; `.claude/skills/` görev kurallarıdır.
  Gerekenleri oku; araç/model adlarının Codex'te aynı olduğu varsayılmaz.
- Ana dala birleştirme ve canlı yayın için kullanıcının açık yetkilendirmesi gerekir.
