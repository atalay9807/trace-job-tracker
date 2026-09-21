# README tanıtımı — kaynak ve bakım notları

## Kapsam

20 Eylül 2026 tarihli çalışma, `9ca7c333ee2426e7e57c73cecf13edeac6277fc2`
commit'inden `codex/readme-gorsel-tanitim` dalında başlatıldı. Amaç GitHub
ziyaretçisinin ürünü hızla anlaması ve demoya kolayca ulaşmasıdır.

Üst bölümde uygulama ve web sitesi bağlantıları, kısa ürün mesajı ve gerçek
demo ekranları bulunur. AI ile geliştirme yaklaşımı galeri sonrasında görünür;
teknik başlıklar aşağıda açılır bölümlerdedir. Uygulama kodu, veri, yayın iş
akışları ve `web-live/` bu çalışmanın değişiklik kapsamına dahil değildir.

## Görsellerin kaynağı

Beş JPEG, [yayındaki demodan](https://atalay9807.github.io/trace-job-tracker/app.html)
20 Eylül 2026'da, 1341 × 921 piksel tarayıcı görünümünde alınmıştır. Bunlar
arayüz taslağı değil, gerçek ekran görüntüsüdür. Görsel içeriğine sonradan
müdahale edilmemiştir. O sırada demo 109 kayıt ve 19 Eylül 2026 veri tarihini
gösteriyordu; yakalama tarihi ile veri tarihi aynı şey değildir.

| Dosya (`docs/img/readme/` altında) | Demo yolu |
|---|---|
| `ana-2026-09-20.jpg` | `app.html#/ana` |
| `basvurular-2026-09-20.jpg` | `app.html#/basvurular` |
| `eslesme-2026-09-20.jpg` | `app.html#/basvurular/kavza-project-cfo-office-executive` |
| `raporlar-2026-09-20.jpg` | `app.html#/raporlar` |
| `egitim-2026-09-20.jpg` | `app.html#/egitim` |

`trace-cover.svg`, `open-app.svg` ve `open-site.svg` bu tanıtım için hazırlanmış
vektör varlıklardır. Metin ve şekiller depodadır; dış görsel servisi, betik,
gömülü kişisel veri veya uzak font kaynağı kullanmazlar. README'de tüm görsellere
anlamlı alternatif metin, ekran görüntülerine ilgili demo bağlantısı eklenmiştir.
Eski `docs/img/` görselleri başka sayfalarda kullanılabildiği için korunmuştur.

## Doğrulama ve güncelleme

Bu dalda 29 Python testi ve 25 DOM testi geçti. Veri doğrulama 109 kaydı kabul
etti; kaynaklardan site üretimi takip edilen uygulama dosyalarını değiştirmedi.
README'deki 45 bağlantı başvurusu (tekrarlar dahil), sekiz görsel ve beş açılır
bölüm kontrol edildi. SVG'ler XML olarak ayrıştırıldı ve PNG'ye işlenerek
görsel olarak incelendi. Metin/zemin kontrastının en düşük değeri **7,05:1**
olarak ölçüldü. Bu oran yeni SVG varlıklarına aittir, tüm uygulamanın
erişilebilirlik denetimi değildir.

- Her göreli dosya bağlantısını, sekiz görseli ve sayfa içi bağlantıları kontrol et.
- SVG dosyalarının XML olarak açıldığını, yazıların sığdığını ve metin/zemin
  kontrastını doğrula. GitHub'ın açık ve koyu temalarında sabit renkli görselleri
  kontrol et; README içine stil veya JavaScript ekleme.
- GitHub'ın işlediği README'yi dal üzerinde incele: iki ana bağlantı galeri
  öncesinde görünmeli, kartlar ve açılır teknik bölümler düzgün açılmalıdır.
- Ekranları yenilerken gerçek demoyu aç, yönlendirme ve panel animasyonunun
  tamamlandığını görsel olarak doğrula. Aynı ekranı farklı adlarla kaydetme.
- Yeni yakalama tarihini dosya adlarına ve README notuna işle. Demo verisinin
  tarihini değiştirme veya güncelmiş gibi sunma.
- Değişiklik davranış eklemediğinden yeni uygulama testi yazılması gerekmez;
  mevcut GitHub Actions kontrollerinin sonucunu PR teslimine kaydet.

## Claude için devir

Bu çalışma ayrı dal ve PR ile teslim edilir. `AGENTS.md` ve ortak çalışma
sözleşmesine göre ana dala birleştirme kullanıcı yetkilendirmesi gerektirir;
entegrasyon Claude'un teknik liderliğiyle koordine edilir.

Bağlantı kontrolünde tanıtım sitesinin `trace.html` sayfasının açıldığı görüldü.
Ancak sayfa hâlâ **68 başvuru** ve **1 Ağustos–1 Eylül 2026** penceresini
anlatırken güncel uygulama **109 kayıt** ve **19 Eylül 2026** tarihini gösteriyor.
Bu, README çalışmasından önceki bir içerik tutarsızlığıdır. Tanıtım sitesinin
sayıları ve zamanlanmış Gmail akışına ilişkin ifadeleri, ayrı bir site içerik
çalışmasında mevcut demo/özel otomasyon ayrımıyla birlikte gözden geçirilmelidir.
README tanıtımında değişken başvuru sayıları satış iddiası olarak kullanılmadı.

Gelecekte `web-live/` uygulanınca özellik durum tablosunu gerçek sürüme göre
yenile. Planlanan hesap, CV ve AI özelliklerini tamamlanmış gibi tanıtma.
