# Faz 1: Temel yapı ve başvuru takibi

## Stack
Next.js (App Router), TypeScript, Tailwind, Supabase (Postgres, Auth, Storage). Deploy: Vercel.
Proje web-live/ klasörünün içinde kurulacak.

## Tablolar
- users: Supabase Auth
- cvs: id, user_id, file_url, uploaded_at
- applications: id, user_id, company, position, job_url, job_description (text),
  status (saved | applied | interview | offer | rejected),
  rejection_reason (skill_gap | experience | position_closed | unknown, nullable),
  rejection_note (text, nullable), created_at, updated_at
- events: id, user_id, event_name, properties (jsonb), created_at

## Sayfalar
1. /login: e-posta ile giriş (Supabase Auth)
2. /onboarding: CV yükleme (PDF, Supabase Storage)
3. /applications: kanban görünümü, 5 kolon (statüler). Kart sürükle-bırak ile statü değişir.
4. /applications/new: başvuru ekleme formu
5. /applications/[id]: detay sayfası, statü değiştirme, not alanı

## Kurallar
- Statü "rejected" yapılınca rejection_reason seçimi zorunlu modal açılsın.
- Şu aksiyonlarda events tablosuna kayıt at: signup, cv_uploaded,
  application_created, status_changed (from/to ile).
- Row Level Security: her kullanıcı sadece kendi verisini görür.
- Mobil uyumlu (responsive) tasarım.
