# Trace teknik sözleşmesi

## Çalışan bileşenler

Python çekirdeği JSON okur ve çıktı üretir; Gmail'e veya bir modele istek yapmaz.
İlan yorumlama, profil çıkarma ve mail taraması ayrı yetkili oturum iş akışıdır.
`src/dashboard.template.html` altı sayfalı arayüzdür. `reports/pano.html` ve
`site/app.html` türetilir; elle düzenlenmez.

## Veri kaynağı ve şema

`src/veri.py` ortam değişkenini her okumada çözer. `TRACE_DATA` yoksa deponun
`data/` klasörü kullanılır; verilmiş fakat eksik dosyada demo veriye dönülmez.
Pano `applications.json`, `profile.json`, `skills_catalog.json`, `journey.json`,
`engagement.json`, `saved_jobs.json`, `role_targets.json` dosyalarını bekler.
Yalnızca raporlama/eşleşme komutları daha az dosya kullanabilir.

Başvurular için zorunlu alanlar: `id`, `company`, `role`, `channel`, `applied`,
`last_contact`, `stage`, `status`, `track`, `fit`, `deadline`, `next_step`,
`notes`, `match`, `gap_skills`, `links_actions`. Kimlik tekil, küçük ASCII
harf/rakam/tire/alt çizgiden oluşur. Şirket ve rol boş olmayan metindir.
Tanınmayan aşama/durum/kanal reddedilir; varsayılan aşama puanı verilmez.

`match`, `fit`, tarih ve açıklama alanları bilinmiyorsa null kullanılabilir.
`gap_skills` ve `links_actions` liste olmalı; kayıt yoksa `[]` kullanılır.
`match` nesnesi varsa dört sayısal boyut, negatif/sıfır lokasyon düzeltmesi ve
gerekçe zorunludur. Negatif boyut, tavan aşımı, boolean, NaN/sonsuzluk reddedilir.
Katalog referansı `python3 src/veri.py` ve analiz/pano üretiminde kontrol edilir.

| İsteğe bağlı alan | Anlam |
|---|---|
| `first_response` | Otomatik başvuru onayı dışındaki ilk gerçek yanıtın `YYYY-MM-DD` tarihi; bilinmiyorsa null |
| `response_received` | Yanıt kanıtı varsa true; yalnızca otomatik onay varsa false; bilinmiyorsa null/eksik |
| `contact`, `location` | İletişim/lokasyon bilgisi; kamuya açık demoda gerçek kişi bilgisi bulunmaz |

İlk yanıt başvurudan önce veya son temastan sonra olamaz. İlk yanıt, ileri aşama
veya red kaydı varken `response_received: false` çelişkidir. Eski şema v1
kayıtları iki yeni alanı içermeden okunabilir; geriye dönük tarih uydurulmaz.

`profile.json: null` ve boş başvuru/kullanım listeleri desteklenir. Diğer dosyalar
beklenen sözlük/listeleri içermelidir; tam kullanıcı veri modelinin doğrulaması
canlı ürün öncesinde genişletilecektir.

## Aciliyet ve kapanma

```
aciliyet = aşama_ağırlığı + (fit × 4) + deadline_aciliyeti − sessizlik_cezası
```

Üst sınır 160'tır: teklif 100 + fit 20 + geçmiş deadline 40. Bilinmeyen fit
puan eklemez. Aşama ağırlıkları `src/veri.py`, diğer eşikler `src/pipeline.py`
içindedir. `config/rules.yaml` çalışma zamanı yapılandırması değildir; referanstır.

Deadline: geçmiş +40; bugün/yarın +35; 2–3 gün +25; 4–7 gün +15; 8–14 gün +8.
Sessizlik: 12 gün **dahil** −8, 21 gün **dahil** −20. Takip günleri takvim günüdür.
Kritik bant ≥100 veya aksiyon gerekli + deadline ≤3 gün/bilinmiyor; yüksek ≥75,
normal ≥45, diğerleri düşük. `stage: closed` veya `status: rejected` kapanmıştır:
puan sıfır, bant arşiv, hatırlatma ve odak listesi yoktur. Uzun sessizlik kendi
başına kayıt kapatmaz; kontrol önerir. Kaynak JSON hesaplamada değiştirilmez.

## Eşleşme ve ajan kontrolü

```
eşleşme = rol_ailesi(0–35) + kıdem(0–25) + beceri(0–25) + sektör(0–15) + lokasyon(≤0)
```

Toplam 0–100'e sınırlandırılır; boyut hataları kırpılıp gizlenmez.
Segmentler güçlü ≥78, iyi ≥62, orta ≥45, zayıf <45. Eksik match null'dır.
Puanlar başarı olasılığı değildir. Rubrik demo profilin bağlamını taşır;
yeni adayda profil/ilan kanıtına göre uygulanmalı, demo kıdemi evrenselleştirilmemelidir.

`python3 src/eslesme_kontrol.py < öneri.json` toplam/segment ve katalog
uyumunu dosyaya yazmadan doğrular. İlan yorumunun kalitesi için kaynak metin,
profil sürümü ve bağımsız değerlendirme gerekir; bu CLI bunu ölçmez.

## Analizlerin anlamı

- **Yanıt sayısı:** `first_response` veya açık yanıt işareti; eski kayıtlarda
  ileri aşama/red kanıtı kullanılır. Salt son temas tarihinin ilerlemesi otomatik
  onay da olabilir. Gösterilen sayı kanıtlı alt sınırdır.
- **Yanıt süresi:** Yalnızca `first_response − applied`; aynı gün sıfır gün
  geçerlidir. Çift sayıda ölçümde iki orta değerin ortalaması alınır. Ölçüm yoksa
  medyan null'dır; son temasla doldurulmaz.
- **Aşama dağılımı:** Anlık durumdur. Kapanan bir kaydın daha önce hangi aşamalara
  ulaştığı bilinmez. Yalnızca başvuru→kanıtlı yanıt oranı gösterilir; diğer ardışık
  dönüşümler ve görüntülenen ilan→başvuru oranı gösterilmez.
- **Haftalık trend:** Pazartesi başlayan ISO haftası, tarihten dinamik üretilir.
  Başvuru tarihi bilinmeyen kayıt trendde yer almaz. İlerleme/red sayıları o
  haftada başvuranların güncel durumudur; o hafta gerçekleşmiş olay sayısı değildir.
- **Kullanım:** Tekil, başlangıç ile referans gün arasındaki rapor günleri sayılır.
  Gelecek günler son 7 güne/streak'e girmez; kapsama %100'ü aşmaz. Boş listede
  tam ve sıfır değerli çıktı üretilir. Rapor gönderimi uygulama açılışını kanıtlamaz.
- **Eksikler:** Kayıtlı değerlendirmeden çıkarımdır, işverenin red gerekçesi değildir.
  Öncelik = redlerde görülme ×3 + açık süreçlerde görülme + seviye farkı ×2.
- **Kaydedilen ilan:** Kapanış bayrağı son bilinen kayıttır; yokluğu ilanın bugün
  hâlâ açık olduğunun doğrulaması değildir.

## Pano ve çıktı sınırları

`python3 src/build_dashboard.py --site` yalnızca açık depodaki etiketli demo
verisiyle `site/app.html` üretir. Tarih `meta.last_scan` üzerinden sabittir.
Özel TRACE_DATA veya özel pano için site/data hedefi reddedilir. Kamuya açık
payload iletişim alanlarını, başvuru/e-posta bağlantılarını ve recruiter mesajlarını
almaz. Bu kontrol bir anonimleştirme servisi değildir: veri ve git diff ayrıca
incelenmelidir; eski commit'lerdeki bilgi geriye dönük silinmez.

JSON içindeki `<`, `>`, `&` ve satır ayırıcılar HTML içine güvenli gömülür;
`</script>` içeren metin yeni script oluşturamaz. Aksiyon URL protokolleri
sınırlanır; harici linklerde `noopener noreferrer` kullanılır. CSV'de harici
metnin formül olarak değerlendirilmesi engellenir.

Kişisel pano tüm veriyi HTML'de taşır; erişim denetimi sağlamaz ve kamuya
sunulamaz. `--out` istenen özel konuma yazabilir; bu çıktı açık depoya eklenmez.
HTML geçici dosyadan atomik taşınır; bu yalnızca yarım yazılmış çıktıyı önler,
çok kullanıcılı veri güncelleme kilidi değildir.

Web demosunda CV seçimi kapalıdır. Destekli Claude ortamında paylaşım onayı,
boyut/tür kontrolü, izin hatası yakalama, model yanıtı kontrolü ve tek aktif istek
koruması vardır. Sonuç ekrandadır; kaydedilmez. Gerçek sağlayıcı entegrasyonu
DOM testlerinde taklit edilir; gerçek model testi yapılmış sayılmaz.

## Başvuru listesi ve CSV

`basvurulariSec()` tablonun ve tarayıcı CSV çıktısının ortak seçimidir. Aciliyet,
eşleşme, açık/kapanan süreç, tarih ve Türkçe arama koşulları birlikte uygulanır.
Seçim yeni bir dizi oluşturur; kaynak `D.applications` sırası değiştirilmez.

Aciliyet sıralaması önce bandı, aynı bant içinde puanı kullanır: çekirdeğin
aksiyon gereği kritik saydığı bir kayıt yalnızca puanı düşük diye geriye düşmez.
Eşleşme iki yönde, başvuru en yeni, deadline en yakın, şirket Türkçe alfabetik
sırayla gösterilir. Aciliyet/deadline sıralamasında açık süreçler önce gelir;
bilinmeyen değerler kendi grubunun sonunda kalır. Eşitlik şirket ve kimlikle
çözülür. `null` eşleşme puanı, sıfır puandan ayrı filtrelenir.

Tarayıcı CSV'si UTF-8 BOM, virgül ayırıcı ve CRLF satır sonu kullanır. Hücreler
tırnaklanır, iç tırnaklar kaçırılır; harici metnin formül başlangıçları tek tırnak
önekiyle etkisizleştirilir. Sayısal sıfır korunur, bilinmeyen değer boş kalır.
İletişim, not ve aksiyon URL'leri aktarılmaz; CSV yalnızca özet sütunlarını taşır.
Dosya tarayıcıda `Blob` ile oluşturulur, indirme sonrası geçici adres temizlenir;
bu işlem sunucuya veri göndermez. Tarayıcı indirme davranışı DOM testinde taklit
edilir; gerçek Excel ve gerçek tarayıcı indirmesi ayrıca doğrulanmalıdır.

## Bakım

`docs/ORTAK_CALISMA.md` kontrol komutlarını ve araçlar arası teslimi tanımlar.
GitHub Actions Python ve DOM kontrollerini çalıştırır. Pages kaynaktan siteyi
üretir; yalnızca `site/` değişikliğine bağımlı değildir. Kod/veri değişip eski
HTML'in yayımlanması önlenir.

Tipografi ve renk değerlerinin kaynağı şablon CSS'idir. Görsel test yapmadan
kontrast/mobil uyum doğrulanmış sayılmaz; `docs/img` ilk prototipin arşividir.
