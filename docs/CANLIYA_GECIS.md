# Trace'i canlı ürüne hazırlama

17 Eylül 2026 itibarıyla çalışan bölüm, kayıtlı veriden rapor üreten Python
çekirdeği ve statik demodur. Bu belge tamamlanmış entegrasyonları değil,
canlı ürün için yapılacak işleri ve kabul koşullarını tanımlar.

## Geliştirme araçları ile çalışan ürünün ayrımı

Claude Code ve Codex aynı depoda geliştirme yapabilir. Uygulama sunucusunda
bu iki kodlama oturumunu çalıştırmak zorunlu değildir. İleride Claude ve OpenAI
modellerinin ikisini de ürün içinde kullanmak istenirse bu, ayrı bir sunucu
entegrasyonudur: sağlayıcı seçimi, anahtar yönetimi, zaman aşımı, yeniden deneme,
bütçe ve veri paylaşımı uygulanmalıdır. Bu düzeltme paketi model çağrısı veya
ücretli hizmet başlatmaz; mevcut Python hesaplamaları deterministiktir.

## Sıralı geliştirme işleri

| Sıra | İş | Kabul koşulu |
|---|---|---|
| 1 | Hesap, veri izolasyonu ve kalıcı kayıt | İki test kullanıcısı birbirinin kaydını okuyamaz/değiştiremez; eşzamanlı güncelleme kaybolmaz |
| 2 | Manuel başvuru/ilan metni girişi | Kullanıcı Gmail olmadan kaydedebilir, düzenleyebilir ve silebilir; boş durum çalışır |
| 3 | Sunucuda AI sağlayıcı katmanı | Anahtarlar tarayıcıya gitmez; şema dışı yanıt yazılmaz; zaman aşımı/başarısızlık görünürdür; maliyet ölçülür |
| 4 | İlan/profil kanıtı ve değerlendirme seti | Kaynak metin, profil/rubrik sürümü ve belirsizlik saklanır; örnek senaryolarda doğruluk ölçülür |
| 5 | Google yetkilendirmesi ve arka plan taraması | Kullanıcı kendi hesabını bağlar/ayırır; token güvenli saklanır; yinelenen mesaj çift kayıt oluşturmaz |
| 6 | Olay geçmişi ve rapor gönderimi | İlk yanıt ve aşama tarihleri ayrı saklanır; tekrar çalışan görev aynı mesajı iki kez göndermez |
| 7 | Silme, yedekleme, izleme ve gizlilik açıklamaları | Silme/geri yükleme denenir; loglara CV ve token yazılmaz; gerçek veri akışı kullanıcıya açıklanır |

Google izin/doğrulama koşulları ve veri aktarımı gereklilikleri entegrasyon
seçildiğinde güncel resmi kaynaklardan doğrulanmalıdır. Önceki notlardaki fiyat
ve hukuki varsayımlar bu planın doğrulanmış girdileri değildir.

## Yayın öncesi doğrulama

Python/DOM testlerine ek olarak gerçek tarayıcıda masaüstü ve mobil akışlar,
klavye kullanımı, gerçek model hata durumları, hesaplar arası izolasyon ve Google
bağlantısını kaldırma denenmelidir. Bu kontroller yapılmadan “canlıya hazır”
denmez. Statik demo yayını, kişisel veri kabul eden ürün yayınıyla aynı değildir.

## Şu an bilinmeyenler

Kullanıcı başına model maliyeti, ikinci kullanıcı başarısı, kaynak ilan olmadan
puanların güvenilirliği ve mail sınıflandırma doğruluğu ölçülmedi. Çok sayıda
ajan tanımı bu ölçümlerin yerine geçmez. Önce küçük bir değerlendirme setiyle
model ve kuralların hatalarını görünür kılmak gerekir.
