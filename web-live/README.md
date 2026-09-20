# Job Tracker — web uygulaması

İş başvurularını takip eden ve CV ile ilanları eşleştiren web uygulaması.
Kapsam ve fazlar `CLAUDE.md`'de, Faz 1 ayrıntısı `docs/faz-1-spec.md`'de.

## Kurulum

```bash
npm install
cp .env.local.example .env.local   # Supabase değerlerini gir
npm run dev
```

`.env.local` gerekli iki değeri Supabase panelinden alırsın:
Project Settings → API → Project URL ve anon/public key.

## Supabase şeması

`supabase/migrations/0001_faz1.sql` dosyasını Supabase SQL Editor'de çalıştır
ya da Supabase CLI kullanıyorsan `supabase db push` ile uygula. Migration
tabloları, Row Level Security politikalarını ve CV'ler için özel (public
olmayan) storage bucket'ını kurar.

Auth tarafında yapılması gereken tek ayar: Authentication → URL Configuration
içinde `Site URL` ve `Redirect URLs` listesine uygulamanın adresi
(`http://localhost:3000` ve dağıtım adresi) eklenir. Giriş e-posta ile
gönderilen tek kullanımlık bağlantıyla yapılır, parola yok.

## Komutlar

```bash
npm run dev        # geliştirme sunucusu
npm run build      # üretim derlemesi
npm run start      # derlenmiş sürümü çalıştır
npm run lint       # eslint
npm run typecheck  # tsc --noEmit
```

## Durum

Faz 1 / Adım 1 kuruldu: proje iskeleti, veri katmanı (migration + RLS),
oturum yönetimi ve e-posta ile giriş. Başvuru sayfaları (`/onboarding`,
`/applications`, `/applications/new`, `/applications/[id]`) sonraki
adımlarda geliyor.
