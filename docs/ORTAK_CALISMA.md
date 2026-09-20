# Claude Code ve Codex ile ortak geliştirme

Trace tek bir kod tabanıdır. Claude Code ve Codex geliştirme araçlarıdır;
uygulamanın çalışması için iki geliştirme oturumunun aynı anda açık kalması gerekmez.
Python hesaplama çekirdeği ikisinden de bağımsız çalışır. Claude ajan dosyaları
Codex'te kendiliğinden çalışmaz; aynı görev kuralları gerektiğinde okunabilir.

## İş paylaşımı

Her işe aynı güncel commit üzerinden, ayrı geliştirme dalı ve ayrı checkout/worktree
ile başla. Aynı dosyayı iki oturumun aynı anda değiştirmesine izin verme. İş tesliminde
başlangıç commit'ini, dalı, değişen dosyaları, çalıştırılan testleri ve kalan sorunları yaz.
İkinci araç bu teslimi ve diff'i okuyarak devam eder; ilk aracın açıklaması test kanıtı değildir.

Ana dala birleştirme ve canlı yayın kullanıcı kararıdır. Yetkilendirilmiş kod
çalışmasını tamamlamak için tekrar tekrar onay istenmez. Gerçek veriyi toplu silmek,
yeniden yazmak, depo görünürlüğünü değiştirmek veya dışarı mesaj göndermek ayrıca
açık yetkilendirme gerektirir. Eşzamanlılık kuralları oturum disiplinidir;
bugünkü dosya yapısı bir veritabanı kilidi sağlamaz.

## Veri kaynağı

- Açık depodaki `data/` demo veri içerir. Demo kimlik, proje sahibinin kimliği değildir.
- Gerçek veri dışarıda tutulur; `TRACE_DATA` ile **aynı veri klasörü** bütün
  scriptlere ve ilgili ajana aktarılır. Ajanlara mutlak klasör yolu ve okunmasına
  izin verilen dosyalar görev girdisinde verilir.
- Ajan metinlerindeki `data/...` yolları, seçilmiş veri klasörüne göre mantıksal
  yollardır. Profil/geçmiş rol önericilerinin birbirinin verisini okumama sınırı korunur.
- Dış veri dosyası yoksa dur ve eksik dosyayı bildir; demo profile sessizce dönme.
  Pano yedi JSON dosyasını da bekler. Özel depoda yalnızca başvuru ve profil varsa
  diğer dosyalar o kullanıcı için hazırlanmalıdır; demo CV seviyeleri kopyalanmaz.
- Scriptler kaynak JSON'u değiştirmez. Ajanlar öneri döndürür; seçilmiş tek yazıcı
  kaynak kaydı günceller ve doğrular. Özel veriyi açık deponun içine kopyalama.
- Özel HTML tüm veriyi içerir ve kimlik doğrulamaz; kişisel kullanım içindir,
  herkese açık sunucuya yüklenmez. `--site` yalnızca depo demo verisini kabul eder.

## Doğrulama ve teslim

```bash
python3 src/veri.py
python3 -m unittest discover -s tests -v
python3 src/build_dashboard.py --site
npm ci --ignore-scripts
npm test
git diff --check
```

Python çekirdeği 3.11+ standart kütüphanesiyle çalışır. Node 20+ ve jsdom yalnızca
arayüz geliştirme testlerindedir; kullanıcının bilgisayarına kurulum gerekmez,
bu kontroller bulutta/GitHub Actions'ta çalışabilir.

`src/dashboard.template.html` düzenlenir, `site/app.html` elle düzenlenmez.
Üretim referans tarihi demo `meta.last_scan` değeridir; aynı girdi aynı siteyi üretir.
`TRACE_DATA` özel veriyi gösteriyorsa site üretmeden önce demo klasörünü seç.

DOM testleri JavaScript davranışını denetler; görsel düzen, gerçek OAuth veya gerçek
model erişimini doğrulamaz. Ekran görüntüsünü yenilemeden yenilenmiş gibi sunma.
Ana dalın yayın iş akışı da bu kontrolleri çalıştırır ve siteyi kaynaktan üretir.

## Ölçüm ve AI sınırları

Red gerekçesi, görüntülenen ilan sayısı ve gerçek kurs kaydı uydurulmaz.
Bilinmeyen eşleşme `null` kalır; sıfır uyum anlamına gelmez. Kaynak ilan metni
olmayan kaydın sayısal puanı doğrulanmış gibi sunulmaz.

`first_response` otomatik başvuru onayı dışındaki ilk yanıtın tarihidir;
`last_contact` yerine kullanılamaz. Geçmiş olay verisi yoksa anlık aşamaların
oranlarını ardışık dönüşüm gibi sunma. Demo profil/rubrik bütün adaylara genellenmez.

Eşleştirici çıktısı kayda yazılmadan kontrol edilebilir:

```bash
python3 src/eslesme_kontrol.py < /tmp/eslesme-onerisi.json
```

Dosya `match`, `gap_skills`, `hesaplanan_toplam`, `segment`, `guven` içerir.
Bu kontrol aritmetik ve şemayı doğrular; ilanın/CV'nin doğru yorumlandığını kanıtlamaz.
Gerçek verili öneri dosyası açık depoya eklenmez.
