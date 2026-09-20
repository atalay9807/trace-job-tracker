# Çalışma kararları — kısa sohbet özeti

Bu dosya sohbet dökümü değildir. Yalnızca sonraki çalışma oturumlarının
davranışını, yetki sınırını veya ürün/mimari yönünü etkileyen kararları kısa
biçimde tutar. Böyle bir karar değiştiğinde bu dosya güncellenir.

## 2026-09-20

- **Ürün Sahibi:** Kullanıcı. Ürün yönü, öncelik, `main` birleştirmesi ve canlı
  yayın için son karar kullanıcıdadır.
- **Tech Lead:** Claude. Ana mimari, teknik bütünlük ve entegrasyon yönünün
  sahibidir.
- **Engineering Partner:** Codex/ChatGPT. Bağımsız reviewer ve destek geliştirici
  olarak çalışır; gerektiğinde Web Architecture, Frontend/UX, Security/Privacy
  ve QA/Release rollerini üstlenir.
- **Çalışma ilkesi:** Claude'un yaklaşımı yalnızca tercih farkı nedeniyle
  yeniden yazılmaz. Öneriler somut hata, güvenlik, veri kaybı,
  sürdürülebilirlik, performans veya UX gerekçesine dayanır.
- **İlerleme yetkisi:** Onaylanmış kapsam içindeki rutin ve geri alınabilir
  geliştirmelerde kullanıcıdan her adımda yeniden yanıt beklenmez. Yüksek
  riskli işlemler ve yeni ürün/mimari yön değişiklikleri ayrıca karar gerektirir.
- **Karar sunumu:** Karar gerektiğinde kısa seçenekler sunulur; önerilen seçenek
  işaretlenir, belirgin avantaj ve önemli bedel belirtilir.
- **Branch disiplini:** Codex/ChatGPT değişiklikleri ayrı dalda yürütür;
  `main` doğrudan değiştirilmez.
- **web-live Faz 1:** Başvuru durumu sade tutulur:
  `saved | applied | interview | offer | rejected`. Eski Trace'in ayrıntılı
  `stage/status` modeli Faz 1'e taşınmaz.
- **Ajan/skill yapısı:** Mevcut Claude ajanları ve skill'leri korunur;
  mühendislik rolleri tamamlayıcı katmandır.
- **Sohbet → çalışma alanı devri:** Rol dağılımı, onay biçimi, yetki sınırı,
  ürün yönü veya mimari yön gibi konuşma dinamiklerini etkileyen kararlar
  bu dosyaya kısa biçimde aktarılır; günlük sohbet ayrıntıları aktarılmaz.
