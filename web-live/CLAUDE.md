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
