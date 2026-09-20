# Yerele taşınma — terminal ve masaüstü

Bu proje bugün **bulutta, geçici bir konteynerde** çalışıyor (claude.ai
üzerinden açılan uzak oturum). Kullanıcı yakında terminal/masaüstü Claude
Code'a geçmek istiyor. Bu belge o gün ne yapılacağını ve neyin **kendiliğinden
gelmeyeceğini** yazar. Not niteliğindedir; taşınma yapıldığında güncellenir.

> Bu belge kullanıcı istediği için yazıldı: taşınma geldiğinde hatırlatılacak.
> Oturumlar arasında hafıza yok — hatırlatmanın tek güvenilir yeri depo.

---

## Bugünkü kısıtlar (taşınınca kalkanlar)

| Kısıt | Bugün | Yerelde |
|---|---|---|
| **Egress kilidi** | Yalnızca paket kayıtları ve `github.com`. `WebFetch` kapalı — `huntr.co`, `builtin.com` denendi, `EGRESS_BLOCKED` döndü | Açık. Rakip arayüzü gerçekten açılıp bakılabilir, `pazar-arastirmacisi` ajanının en büyük eksiği kapanır |
| **Konteyner geçici** | Oturum bitince disk gider; commit edilmeyen her şey kaybolur | Disk kalıcı. Ekran görüntüleri, ara çıktılar, deneme dosyaları durur |
| **Yayınlanan sayfa doğrulanamaz** | `github.io` açılamıyor; Pages çıktısı ancak kullanıcıdan istenerek doğrulanır | Kendi tarayıcında açılır; Playwright ile gerçek yayın adresi test edilir |
| **Sunucu tarafı OAuth yok** | Bağlan sayfası gerçek Gmail bağlantısı kuramıyor, hata durumu gösteriyor | Yerelde de tek başına çözmez — OAuth için barındırılan bir arka uç gerekir. Bu taşınmayla **çözülmez**, ayrı iştir |

## Depodan gelen — hiçbir şey yapmana gerek yok

`claude` komutunu depo dizininde çalıştırdığın anda şunlar otomatik yüklenir:

- `CLAUDE.md` — proje talimatları
- `.claude/agents/*.md` — dokuz ajan
- `.claude/skills/*/SKILL.md` — yedi skill
- `src/`, `data/`, `config/`, `docs/` — kodun ve verinin tamamı

Yani ajan ve skill mimarisi **taşınabilir**; kurulum diye bir şey yok, `git
clone` yeter.

## Depodan gelmeyen — elle kurulacak

**1. MCP bağlayıcıları.** Gmail, Google Drive, GitHub, Indeed bağlayıcıları
hesap/oturum seviyesinde duruyor, depoda değil. Yerelde her biri yeniden
yetkilendirilecek (`claude mcp add …` ya da masaüstü uygulamasının bağlayıcı
ekranı). Gmail yetkilendirmesi olmadan günlük tarama çalışmaz — projenin
girdisi orası.

**2. Hesap seviyesindeki skill'ler.** CLAUDE.md `dataviz` skill'indeki
`validate_palette.js`'e atıf yapıyor ama o dosya bu depoda **yok** ve bu
oturuma da senkronlanmamış — kişisel bir skill. Kontrast ölçümü yerelde
tekrar gerekiyorsa ya o skill yerele de senkronlanmalı ya da ölçüm betiği
depoya alınmalı. İkincisi daha sağlam: ölçüm proje kuralı, kişisel tercih değil.

**3. Günlük Routine.** 09:00 taraması bulut tarafında yaşıyor. Yerel Claude
Code kapalıyken tetiklenmez. İki seçenek var, taşınırken karar verilecek:

- Routine bulutta kalsın, yerel oturum yalnızca geliştirme için kullanılsın
  (basit; bugünkü işleyiş bozulmaz)
- Tetikleme yerele alınsın (`cron`/`launchd` → `claude -p "…"`). Makine
  kapalıysa o gün rapor çıkmaz; buna karşılık her şey tek yerde olur

Routine **silinip yeniden kurulmaz** — geçmişi kaybolur. Değişiklik
`update_trigger` ile yapılır.

**4. Playwright.** Bu konteynerde Chromium hazır geliyor
(`/opt/pw-browsers/chromium-1194/chrome-linux/chrome`). Yerelde bir kez
`playwright install chromium` gerekir; `build_dashboard.py` sonrası arayüz
doğrulaması buna bağlı.

## Yerel gereksinimler

- Python **3.11+** — harici bağımlılık yok, standart kütüphane yeter
- `git`
- Claude Code CLI (terminal) ya da masaüstü uygulaması
- Node.js — yalnızca Playwright ve kontrast ölçümü için

```bash
git clone https://github.com/atalay9807/trace-job-tracker.git
cd trace-job-tracker
python3 src/pipeline.py        # çalışıyor mu, ilk kontrol bu
claude
```

## Taşınma sırası

1. Depoyu klonla, `python3 src/pipeline.py` çalıştır — veri katmanı sağlam mı
2. `claude` aç, `/agents` ve skill listesiyle dokuz ajanın ve yedi skill'in
   göründüğünü doğrula
3. Gmail + Drive + GitHub + Indeed bağlayıcılarını yetkilendir
4. Bir günlük taramayı elle koştur, çıktıyı buluttaki son raporla karşılaştır
5. Routine kararını ver (bulutta mı, yerelde mi)
6. Playwright kur, `build_dashboard.py` sonrası ekran görüntüsü al

## Taşınmanın değiştirmediği şey

**LinkedIn kazınamaz.** Bu teknik değil hukuki bir sınır — Kullanıcı
Sözleşmesi yasaklıyor ve fiilen takip ediliyor. Yerelde egress açılınca
"artık yapabiliriz" diye düşünme; LinkedIn'den gelen tek meşru veri
kullanıcının kendi gelen kutusudur, bu taşınmadan sonra da öyle kalır.

Aynı şekilde CLAUDE.md'deki üç ölçüm sınırı (red gerekçeleri, görüntülenen
ilan verisi, kurs simülasyonu) ortamla ilgili değil veriyle ilgili — yerelde
de aynen durur.
