# Kurstaki araçların sınıflandırması

Kaynak: `docs/kaynak-claude-code-kursu.md` (izlenen YouTube kursunun
dökümü). Kullanıcı "videoda gösterilen uygulamaları tara ve sınıflandır"
dedi — bu belge onun cevabı.

**Sayım uyarısı:** döküm otomatik konuşma-metin çevirisi, adlar fonetik
yazılmış: `Epify`→Apify, `Kanva`→Canva, `Supase`→Supabase, `Anti Gravity`→
Antigravity, `N8`→n8n. Aşağıdaki geçiş sayıları bu varyantların toplamı;
**önem sırası değil, yalnızca kursta ne kadar konuşulduğu.**

---

## Rolüne göre

### 1. Otomasyon / orkestrasyon

| Araç | Geçiş | Kursta ne için | Trace'te karşılığı |
|---|---|---|---|
| **n8n** | ~80 | Kursun ikinci ekseni. Hazır 9500 otomasyon şablonu, görsel akış kurucu. Claude Code'a connector olarak da bağlanıyor | **Yok ve gerek yok.** Kursun kendisi bile "N8N istemiyorum, Claude için kuralım" diyerek bir örneği n8n'siz kuruyor. Bizim orkestrasyonumuz Routine + `pipeline.py`; kurallı iş için n8n bir katman fazlası |
| **Routine** (Claude) | — | Kursta "routine, n8n otomasyonu gibi çalışıyor" diye tanıtılıyor | **Kullanılıyor** — günlük 09:00 taraması |

### 2. Veri toplama

| Araç | Geçiş | Kursta ne için | Trace'te karşılığı |
|---|---|---|---|
| **Apify** | ~48 | MCP connector olarak bağlanıyor; Instagram verisi çekmek ve müşteri bulma sisteminde kaynak olarak kullanılıyor | **Kullanılmıyor — kullanılamaz.** İhtiyacımız olan tek dış veri LinkedIn ilan metni ve orası kazınamaz (Kullanıcı Sözleşmesi). Apify'ı LinkedIn'e doğrultmak aracın değil bizim sorunumuz olur |
| **Indeed MCP** | — | Kursta yok | **Kullanılıyor** — resmî arama API'si, `rol-onerici-gecmis` ajanının ilan varlığı kontrolü |

### 3. Geliştirme ortamı

| Araç | Geçiş | Kursta ne için | Trace'te karşılığı |
|---|---|---|---|
| **Claude Code** | — | Kursun ana ekseni | **Bu proje zaten bu** |
| **Antigravity** | ~16 | İndirilebilir alternatif IDE olarak gösteriliyor | **Gerek yok.** Ajan/skill mimarimiz depoda duruyor, IDE'ye bağlı değil. Taşınmada da fark etmez (`docs/yerel-kurulum.md`) |

### 4. Bağlayıcılar (MCP connector)

| Araç | Geçiş | Trace'te karşılığı |
|---|---|---|
| **Gmail** | ~34 | **Kullanılıyor — projenin tek girdisi.** Kurstaki tek örtüşen kritik araç |
| **Google Drive** | 3 | **Kullanılıyor** — CV okuma |
| **GitHub** | 2 | **Kullanılıyor** — depo, Actions, Pages |
| **Slack** | 5 | Gerek yok. Tek kullanıcılı bir araç; bildirim kanalı e-posta |
| **Telegram** | 1 | Gerek yok — aynı sebep |
| **Figma / Canva** | 1 / 1 | Gerek yok. Arayüz tek HTML dosyası, tasarım sistemi `docs/TEKNIK.md`'de yazılı |
| **Supabase** | 1 | **Açık maddeye bağlı.** CLAUDE.md'deki "kalıcı veritabanı ve oturum yönetimi" maddesi gerçekleşirse ilk bakılacak yer burası — bugün veri katmanı `data/*.json` |
| **Shopify** | 6 | Alakasız — e-ticaret |
| **Stripe** | 5 | **Bugün alakasız, ürünleşirse gerekir.** Kursta iki işi görüyor: ödeme altyapısı ve gelir kanıtı ("kazançlar birebir Stripe'tan kontrol edilmiş"). İkincisi bizim için de not: gelir iddiası ancak ödeme sisteminden doğrulanabilir |

### 5. Satış yığını (kursun kendi işi)

Apollo, Clay, Lemlist, Gong, HubSpot, **Instantly** (yüksek hacimli mail
gönderimi için; "30-40 mail gönderdiğinizde problem yok" deniyor).

**Tamamı alakasız.** Bunlar kurs sahibinin ajans işine ait; Trace bir satış
aracı değil. Instantly'nin toplu gönderim mantığı bizim tek kullanıcılı
takip mailimizin tersi.

### 6. Diğer

| Araç | Geçiş | Not |
|---|---|---|
| **Excalidraw** | 6 | Kurs sahibinin "en çok kullandığım yetenek" dediği diyagram skill'i. Bizde karşılığı yok; `docs/TEKNIK.md` şu an metin. Mimari şema gerekirse tek adaylardan biri |
| **Nano Banana / Veo 3** | — | Görsel-video üretimi. Alakasız |

---

## Özet

**Kurstan bize gerçekten değen üç şey var:** Gmail bağlayıcısı (zaten var),
Routine mantığı (zaten var) ve ajan/skill mimarisi (zaten kurulu). Geri
kalanı ya kurs sahibinin kendi ajans işine ait (satış yığını, Shopify,
Apify) ya da bizim mimarimizde karşılığı olan bir katmanın alternatifi
(n8n, Antigravity).

**Sonradan gerekebilecek iki isim:** Supabase (kalıcı veritabanı açık
maddesi) ve Stripe (ürünleşme). İkisi de bugün gerekmiyor; şimdi
eklenirse çözülmemiş bir problemin cevabı olarak durur.

**Kurstaki araç sayısı ile sistemin gücü aynı şey değil.** Kurs 20 ajanlı
bir kurulum gösteriyor, biz dokuzda kaldık — sebebi CLAUDE.md'de yazılı:
kurallı iş kod ile ajansız ve daha ucuza yapılıyor, ajan yalnızca yargı
gerektiren yerde kullanılıyor. Aynı ölçü araçlar için de geçerli.
