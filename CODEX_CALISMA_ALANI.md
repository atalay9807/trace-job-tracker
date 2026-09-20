# Trace — Codex çalışma alanı

> **20 Eylül 2026 — bu dal `main`'e alındı.** Aşağıdaki "değişiklikler neden ana
> sayfada görünmüyordu" bölümü merge öncesi duruma aittir; sıralama, CSV indirme
> ve yeni testler artık `main` üzerinde ve yayındadır.

**[Çalışma merkezi — Issue #4](https://github.com/atalay9807/trace-job-tracker/issues/4)** ·
[Güncel dosyalar](https://github.com/atalay9807/trace-job-tracker/tree/codex/calisma-alani) ·
[Tüm değişiklikleri karşılaştır](https://github.com/atalay9807/trace-job-tracker/compare/main...codex/calisma-alani)

Bu alan, Claude Code ile geliştirilen Trace'in Codex tarafından incelenen,
test edilen ve geliştirilen sürümünü gösterir. Güncel PR bağlantısı ve GitHub
kontrolleri Issue #4'te tutulur; yalnızca yerelde kalan çalışma teslim sayılmaz.

## Değişiklikler neden ana sayfada görünmüyordu?

GitHub depo ana sayfasında varsayılan `main` dalı açılır. Önceki düzeltmeler
PR #2'nin `codex/trace-guvenilirlik-ve-ortak-calisma` dalındaydı. Bu oturum
sürerken aynı düzeltmeler [PR #3](https://github.com/atalay9807/trace-job-tracker/pull/3)
üzerinden `main` dalına alındı. `codex/calisma-alani` güncel ana dalın üzerinde
aşağıdaki yeni geliştirmelerle devam eder. Pages yayını ana daldan yapılır;
bir geliştirme dalı veya PR açmak otomatik olarak yeni sürümü yayınlamaz.

Kurulum yapmadan izlemek için çalışma merkezini aç; dosyalar için **Güncel
dosyalar**, kod farkı için **Tüm değişiklikleri karşılaştır** bağlantısını kullan.
GitHub'daki `site/app.html` bir kaynak dosya görünümüdür, çalışan web önizlemesi
değildir. Yeni sürüm görsel olarak doğrulandıktan ve yayın yetkisi verildikten
sonra ana dal üzerinden yayınlanabilir.

## 20 Eylül 2026 — başvuru listesi

Başlangıç commit'i: `2e73b6f3049667c74a0096800ba0e7b5b20b19fa`.
Oturum başında hem `main` hem Claude'un geliştirme dalı
`da59cd42e5eae7eb78889c1bdb9942608abd1d9d` commit'indeydi; yeni bir Claude
değişikliği yoktu. Çalışma sırasında PR #3 birleştirilince taban
`bdf55503cddb74044923fbea04f24f1069e1c009` commit'ine güncellendi; bu ana dalın
dosya ağacı ilk test edilen tabanla birebir aynıydı. Önceki Codex düzeltme
raporu [burada](docs/DUZELTME_RAPORU.md).

| İhtiyaç / sorun | Bu turdaki geliştirme |
|---|---|
| Kayıtlar tek sırayla geliyordu | Aciliyet, iki yönde eşleşme, başvuru tarihi, deadline ve şirket için altı sıralama |
| Düşük aciliyet ayrı seçilemiyordu | Düşük filtresi |
| Kapanan süreçler hep olumsuz etiketleniyordu | Kapanan etiketi ve açık/kapanan süreç seçimi |
| Değerlendirilmemiş kayıt bulunamıyordu | Puanlanmadı filtresi; sıfır puandan ayrı davranış |
| Çoklu filtreyi geri almak zordu | Tek düğmeyle filtre ve sıralamayı sıfırlama |
| Seçilen liste dışarı alınamıyordu | Görünen sonuçları aynı sırayla CSV indirme |
| Satırdaki bağlantıya Enter basınca detay da açılıyordu | Satır klavye dinleyicisi yalnızca satırın kendisinde çalışır |

Aciliyet ve deadline sıralamasında kapanan kayıtlar sonda tutulur. Aciliyet
önce kritik/yüksek/normal/düşük bandını, sonra puanı dikkate alır. Bilinmeyen
değerler kendi grubunun sonunda kalır. Kaynak JSON veya yüklenen kayıtların
sırası değiştirilmez. Tarih filtresinin referans günü ekranda açıklanır.

CSV Türkçe karakterleri, virgül/tırnak/satır sonlarını korur; formül gibi başlayan
metinler için koruma uygular. Kaydı olmayan puan boş, gerçek sıfır puan `0`
olarak çıkar. Not, iletişim ve aksiyon bağlantıları CSV'ye eklenmez.

## Doğrulama

- 68 demo kaydı: şema denetimi.
- 29 Python testi.
- 25 DOM davranış testi: önceki 13 teste 12 senaryo eklendi.
- Şablondan `site/app.html` üretimi ve `git diff --check`.
- Uzak kontrollerin güncel kanıtı: çalışma merkezindeki PR'nin **Checks** bölümü.

Bulut tarayıcısı `127.0.0.1` önizlemesini `ERR_BLOCKED_BY_CLIENT` ile engelledi.
Bu turda gerçek masaüstü/mobil görüntü ve gerçek tarayıcı CSV indirmesi
doğrulanamadı. DOM testleri bunların yerine geçtiği iddiasını taşımaz. Bu tur
görselleri güncellemedi ve kişisel hesaba/model sağlayıcısına bağlanmadı.

## Claude Code'a devir

1. `AGENTS.md` / `CLAUDE.md` ve [ortak sözleşmeyi](docs/ORTAK_CALISMA.md) oku.
2. Çalışma merkezindeki güncel dal ve PR'yi kontrol et; `main`'den başlatılan
   eski bir kopyada Codex düzeltmelerinin bulunduğunu varsayma.
3. Yeni görev için güncel çalışma commit'inden ayrı dal ve checkout aç.
4. Arayüzün kaynağı `src/dashboard.template.html`; `site/app.html` üretilir.
5. Önce gerçek tarayıcıda masaüstü/mobil, klavye ve CSV indirme akışını denetle.
   Sonuçları çalışma merkezine commit ve test kanıtıyla ekle.

Önerilen sonraki ürün işi, Gmail gerektirmeyen manuel başvuru girişidir.
Uygulamaya veri yazmadan önce saklama, hesap izolasyonu ve eşzamanlı güncelleme
kabul koşulları [canlıya geçiş planına](docs/CANLIYA_GECIS.md) göre belirlenir.
Bu listedeki açık işler atanmış veya arka planda çalıştırılan görevler değildir.
