# Job Tracker (web-live)

## Proje
İş başvurularını takip eden ve CV ile iş ilanlarını eşleştiren bir web uygulaması.
Önce web, ileride mobil (Expo) gelebilir. Bu yüzden iş mantığını UI'dan ayrı tut.

Bu klasör (web-live/) repo içindeki web uygulamasının tamamını barındırır.
Repo'daki diğer klasörlere dokunma, tüm dosyaları bu klasör içinde oluştur.

## Ana özellikler (fazlar)
1. Başvuru takibi: statü hattı (saved, applied, interview, offer, rejected), red nedeni
2. CV-ilan eşleştirme: eşleşme skoru ve eksik skill listesi (Claude API)
3. Kişisel eğitim sayfası: eksik skill'lere göre kurs önerisi. Red nedeni skill
   eksikliğiyse ilgili kurs kartı başvuru sayfasında da gösterilir.
4. Funnel navigasyonu: kullanıcıyı newcomer, activated, engaged, habit
   segmentlerinden geçirecek sayfa akışı ve yönlendirmeler
5. Ölçüm: event tracking, segment geçiş oranları

Şu an aktif faz: Faz 1 (spec: docs/faz-1-spec.md).
Diğer fazlara ait kodu ben istemeden yazma.

## Stack
Next.js (App Router), TypeScript, Tailwind, Supabase (Postgres, Auth, Storage), Vercel.

## Kurallar
- Her kullanıcı sadece kendi verisini görür (Row Level Security).
- Önemli kullanıcı aksiyonları events tablosuna yazılır (Faz 4-5 buna dayanıyor).
- Tüm sayfalar mobil uyumlu olmalı.
- Veritabanı değişikliklerini migration dosyası olarak yaz.
- Gizli anahtarlar sadece .env.local içinde durur, repo'ya commit edilmez.
- Büyük bir değişiklikten önce ne yapacağını kısaca özetle, onayımı bekle.

## Her adımın sonunda: doğrulama ve rapor
Bu uygulamanın sahibi kod okumuyor. Bu yüzden hiçbir adım, aşağıdaki iki iş
bitmeden "tamam" sayılmaz.

1. **Doğrulama.** Adım commit'lenmeden önce `code-verifier` ajanı çalıştırılır.
   Ajanın raporu `web-live/docs/reviews/YYYY-AA-GG-<adım>.md` dosyasına
   **değiştirilmeden** kaydedilir; ana oturum cevabını altına yazar. Raporda
   `BLOCKER` varsa adım bitmemiştir — önce o düzeltilir.
2. **Sahibe rapor.** Sade Türkçeyle, teknik terim kullanılıyorsa açıklanarak:
   - **Ne yapıldı** — bir iki cümle, dosya listesi değil.
   - **Neden** — bu adım ürüne ne kazandırıyor.
   - **Nasıl doğrulandı** — çalıştırılan komutlar ve denetçinin kararı
     (PASS / PASS WITH NOTES / FAIL).
   - **Neyi doğrulayamadık** — ve neden. "Test edemedim" demek, test edilmiş
     gibi davranmaktan iyidir.
   - **Senden gereken** — varsa, tek bir somut eylem.
   - **Token** — yerel oturumda adımın başında ve sonunda `/cost` çıktısı;
     fark bu adımın maliyetidir. Bulut oturumunda bu sayı görünmez, o zaman
     "ölçülmedi" yazılır, tahmin yazılmaz.
   - **Sıradaki adım** — tek cümle.
