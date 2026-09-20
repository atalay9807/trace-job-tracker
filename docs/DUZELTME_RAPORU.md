# Trace düzeltme raporu — 18 Eylül 2026

## Sonuç

Kod düzeltmeleri `codex/trace-guvenilirlik-ve-ortak-calisma` dalında hazırlandı.
Başlangıç commit'i: `da59cd42e5eae7eb78889c1bdb9942608abd1d9d`.
Çalışma mevcut JSON raporlama mimarisini korur; yeni bir sunucu, ücretli model
çağrısı, Gmail taraması veya zamanlanmış görev başlatmaz.

29 Python regresyon testi ve 13 DOM davranış testi geçti. 68 demo kaydı şema ve
beceri kataloğuna göre doğrulandı. Dört Python giriş noktası demo ve boş kullanıcı
verisiyle çalıştırıldı. Üç bozuk YAML başlığı düzeltildi; dokuz ajan ve yedi
skill'in başlıkları ayrıştırıldı.

GitHub bağlantısı 18 Eylül'de kullanılabilir hale geldi. Değişiklikler ayrı
geliştirme dalı ve taslak PR üzerinden teslim edilir. Ana dala birleştirme ve
canlı dağıtım bu paketin kapsamında değildir. Uzak doğrulamanın güncel sonucu
PR'nin Checks bölümünden izlenir.

## Hesaplama ve veri düzeltmeleri

| Sorun | Yapılan değişiklik | Doğrulama |
|---|---|---|
| Boş başvuru listesi analizde çöküyordu | Sıfır paydalar ve boş kullanım durumu desteklendi | Boş veriyle dört komut ve altı arayüz sayfası |
| Haftalar Ağustos 2026'ya sabitti | Gerçek tarihten ISO hafta gruplaması | Yıl geçişi, Eylül ve bilinmeyen tarih |
| Bugünkü yanıt sıfır gün olduğu için kayboluyordu | Yanıt kanıtı iki raporda ortak tanıma bağlandı | Aynı gün yanıt raporda %100 |
| Son temas, ilk yanıt süresi sayılıyordu | İsteğe bağlı first_response; yoksa ölçüm yok | Son temas farklıyken ilk yanıttan hesap |
| Çift örneklemde medyan yanlıştı | İki orta değerin ortalaması | 1 ve 10 gün → 5,5 gün; aynı gün → 0 |
| 12/21 gün sınırları belgelerden farklıydı | Sınır günleri dahil edildi | 11, 12 ve 21 günlük sessizlik |
| Kapanmış kayıt hatırlatma üretiyordu | Kapalı/red kayıt puan, odak ve hatırlatmadan çıkarıldı | Deadline geçmiş kapalı kayıt |
| Anlık aşamalar geçiş oranı gibi sunuluyordu | Kanıtlanamayan ardışık dönüşümler kaldırıldı | Teklif kaydında uydurma mülakat dönüşümü yok |
| Gelecek/tekrarlı kullanım günleri sayılıyordu | Tekilleştirme ve tarih penceresi | Gelecek, başlangıç öncesi ve tekrar günleri |
| Yanlış aşama sessizce varsayılan puan alıyordu | Ortak şema denetimiyle açık hata | Bilinmeyen aşama, bozuk tarih ve kimlik |
| Boyut sınırları doğrulanmıyordu | Sayı, tavan, null ve gerekçe kontrolleri | Boolean, NaN, negatif ve tavan aşımı |
| Aynı süreçte veri yolu önbellekte kalabiliyordu | TRACE_DATA her okumada çözülüyor | İki profil klasörü ve eksik dosya |
| Puanlama kaynak kayıtları değiştiriyordu | Türetilmiş alanlar yeni kayıt kopyalarında | Girdi/çıktı sonrası kaynak eşitliği |

Yanıt tanımı bilinçli olarak daha muhafazakâr oldu: salt son temas değişimi,
otomatik onay olabilir. Kanıtlı aşama/red veya açık yanıt kaydı sayılır; bu sayı
alt sınırdır. Mevcut demo verisinde ilk yanıt tarihi bulunmadığından medyan
artık gösterilmez. Eski sayıların değişmesi bu ölçüm düzeltmesinin sonucudur.

## Arayüz ve çıktı güvenliği

- HTML belge iskeleti, UTF-8 ve mobil viewport eklendi.
- Desteklenmeyen CV seçimi kapatıldı; mevcut olmayan Claude nesnesi artık
  ReferenceError üretmiyor. Destekli ortamda paylaşım onayı, izin hatası,
  model yanıtı ve eşzamanlı istek kontrolü var. PDF okuyucusu gerektiğinde yüklenir.
- Gmail düğmesi bağlantı kuruluyormuş gibi bekletmiyor; bu sürümün sınırını açıklıyor.
- Eksik puan/tarih ve boş eğitim listesi düzgün gösteriliyor. Son N gün filtresi
  gelecek tarihleri ve pencere dışını almıyor. Türkçe arama doğrulandı.
- Demo bandında profilin örnek olduğu ve referans tarihi açıklanıyor.
- Kamuya açık HTML'de başvuru/e-posta aksiyonları, contact ve recruiter mesajları
  bulunmuyor. Özel veriyle --site üretimi ve repo içinde yanlış hedef engelleniyor.
- JSON içindeki kapanış script etiketi çalıştırılabilir HTML'e dönüşmüyor;
  aksiyon URL'leri ve CSV formül başlangıçları denetleniyor.
- Modal odak dönüşü ve Tab sınırlandırması eklendi. Görsel/erişilebilirlik
  uygunluğu için gerçek tarayıcıyla ayrıca doğrulama gerekiyor.

## Claude Code / Codex uyumu

`docs/ORTAK_CALISMA.md` ortak sözleşme oldu. AGENTS.md ve CLAUDE.md bu belgeye
yönlendiriyor. Her görev ayrı dal ve çalışma kopyasında yürütülür; aynı kaynak
JSON'a iki ajan yazmaz. Bu bir oturum çalışma kuralıdır, veritabanı kilidi değildir.

Eşleştiricinin “kayda yaz ve doğrula” / “dosyaya yazma” çelişkisi kaldırıldı.
`src/eslesme_kontrol.py` öneriyi kayda yazmadan denetler. İlan metni yetersizse
null sonuç kullanılır; veri eksikliği adayın kötü eşleşmesi sayılmaz.

Mail sınıflandırma referansında red, olumlu davet işaretlerinden önce ele alınır;
`not moving forward` içindeki olumlu alt dizgiye göre davet verilmez. Alıntılanmış
eski mesaj dışlanır; genel/çelişkili kelimeler incelemeye bırakılır. Bu, talimat
ve yapılandırma düzeltmesidir; gerçek gelen kutusunda sınıflandırma başarısı
ölçüldüğü iddia edilmez.

İki skill ve mülakat hazırlık ajanının description alanındaki iki nokta
YAML ayrıştırmasını bozuyordu; değerler uygun biçimde tırnaklandı.

## Otomatik doğrulama ve yayın

Yeni kontrol iş akışı Python, demo üretimi, npm/DOM ve türetilmiş dosya
kontrollerini çalıştırır. Pages işi bu kontrol geçmeden dağıtıma geçmez; kod,
veri veya şablon değişikliklerini de izler. Demo çıktısı farklı Python
hash seed değerlerinde birebir aynı üretildi.

Kontroller bu çalışma ortamında geçti. GitHub Actions sonucu PR'nin Checks
bölümünde ayrıca izlenir; yeni commit gönderildiğinde önceki sonuç yeni sürüm
adına başarı sayılmaz.

## Tamamlanmayan doğrulamalar ve canlı ürün sınırları

Bulut tarayıcısı yerel önizleme adresine erişimi engelledi. Bu nedenle yeni
masaüstü/mobil ekran görüntüsü alınmadı; önceki görseller arşiv olarak etiketlendi.
DOM testleri gerçek tarayıcı veya görsel denetim değildir. Gerçek Claude sample,
Google OAuth, model maliyeti ve çok kullanıcılı izolasyon denenmedi.

Statik HTML kişisel veriyi güvenli biçimde çok kullanıcıya sunan bir backend
sağlamaz. Hesaplar, veritabanı, yazma yolu, Google bağlantısı, model sağlayıcı
katmanı ve olay geçmişi açık işlerdir. `docs/CANLIYA_GECIS.md` kabul koşullarını
tanımlar. “Canlıya hazır” iddiası yapılmaz.

Açık depodaki kaynak demo JSON dosyaları ve eski commit geçmişi değiştirilmedi.
HTML'de bağlantıların çıkarılması, eski commit'lerdeki bir verinin silindiği
anlamına gelmez. Başvuru dışındaki tüm JSON şemalarının kapsamlı doğrulaması
ve gerçek model değerlendirme seti sonraki çalışmaya kalır.
