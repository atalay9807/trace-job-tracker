# Trace proje yönetim modeli

Bu belge, Claude Code, Codex/ChatGPT ve uzman ajanların aynı depoda nasıl
çalışacağını tanımlar. Teknik çalışma kuralları için ayrıca
`docs/ORTAK_CALISMA.md` geçerlidir.

## Yetki hiyerarşisi

1. **Ürün Sahibi — kullanıcı**
   - Ürün vizyonu, kapsam, öncelik ve nihai yayın kararının sahibidir.
   - `main` birleştirmesi, canlı yayın, gerçek veriyi etkileyen toplu işlem ve
     dışarı mesaj gönderme için son yetki kullanıcıdadır.

2. **Tech Lead — Claude**
   - Ana mimari, teknik bütünlük, entegrasyon sırası ve uygulama yaklaşımının
     sahibidir.
   - Uzman ajanlardan ve Codex/ChatGPT'den gelen bulguları değerlendirir.
   - Onaylanmış değişikliklerin ürüne nasıl entegre edileceğine karar verir.

3. **Engineering Partner — Codex/ChatGPT**
   - Bağımsız teknik inceleme yapar; hata, güvenlik, mimari borç, UX ve test
     açıklarını arar.
   - Kullanıcının onayladığı kapsam içinde ayrı dalda uygulama yapabilir.
   - Tech Lead mimarisini kişisel tercih nedeniyle yeniden yazmaz; değişiklik
     önerisi somut gerekçeye dayanır.
   - Rutin ve geri alınabilir geliştirme adımlarında her commit için yeniden
     kullanıcı onayı beklemez.

4. **Uzman ajanlar**
   - Dar bir sorumluluk alanında analiz veya uygulama yapar.
   - Tech Lead'in yerini almaz ve ürün kararı vermez.
   - Görev sınırları kendi ajan dosyalarında tanımlıdır.

## Karar sınıfları

**Rutin teknik karar:** mevcut onaylı kapsam içinde küçük, geri alınabilir
uygulama kararıdır. Ayrı geliştirme dalında doğrudan ilerlenebilir.

**Mimari karar:** veri modeli, kimlik doğrulama, yetki, servis sınırı,
kalıcı teknoloji veya migration yönünü etkiler. Karar ADR olarak kaydedilir;
Tech Lead değerlendirmesi görünür tutulur.

**Ürün kararı:** kullanıcı akışı, kapsam, ücretlendirme, ana özellik davranışı
veya ölçüm tanımını değiştirir. Ürün Sahibi belirler.

**Yüksek riskli işlem:** `main` birleştirme, canlı yayın, gerçek veriyi toplu
silme/yeniden yazma, depo görünürlüğü değiştirme veya dışarı mesaj gönderme.
Açık kullanıcı yetkisi olmadan yapılmaz.

## Çalışma akışı

İş, güncel `main` veya kararlaştırılmış entegrasyon commit'inden ayrı görev
dalına alınır. Aynı dosyaya iki ajan paralel yazmaz. Uygulama tamamlandığında
başlangıç noktası, değişen dosyalar, test kanıtı ve kalan riskler PR'da yazılır.

Claude varsayılan Tech Lead ve entegrasyon sahibidir. Codex/ChatGPT bağımsız
inceleme katmanıdır; kullanıcı uygulamayı ayrıca ona atarsa ayrı dalda kod
üretebilir. Çatışmada önce davranışın mevcut sözleşmesi ve test kanıtı incelenir;
tercih farkı tek başına yeniden yazma gerekçesi değildir.

## İnceleme formatı

Önemli bir öneri şu beş soruya cevap vermelidir:

- Mevcut davranış ne?
- Somut bulgu veya risk ne?
- Neden değişiklik gerekiyor?
- Önerilen değişiklik ve etkilenen dosyalar ne?
- Geri dönüş veya yan etki riski ne?

Kullanıcı seçenekli karar istediğinde önerilen seçenek açıkça işaretlenir;
her seçeneğin belirgin avantajı ve önemli bedeli yazılır.