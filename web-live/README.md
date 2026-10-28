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

`supabase/migrations/` altındaki dosyaları numara sırasıyla Supabase SQL
Editor'de çalıştır ya da Supabase CLI kullanıyorsan `supabase db push` ile
uygula. `0001` tabloları, Row Level Security politikalarını ve CV'ler için
özel (public olmayan) storage bucket'ını kurar; `0002` olay kayıtlarını ve
CV bucket'ını sıkılaştırır (sunucu zamanı, kapalı olay listesi, yalnızca PDF,
10 MB sınırı).

Auth tarafında yapılması gereken tek ayar: Authentication → URL Configuration
içinde `Site URL` ve `Redirect URLs` listesine uygulamanın adresi
(`http://localhost:3000` ve dağıtım adresi) eklenir. Giriş e-posta ile
gönderilen tek kullanımlık bağlantıyla yapılır, parola yok.

### Telefonda giriş: e-posta şablonu

Varsayılan giriş bağlantısı, girişi başlatan tarayıcıda saklanan bir
anahtarla doğrulanır. Bağlantı başka bir tarayıcıda açılırsa — örneğin
telefondaki e-posta uygulamasının kendi içindeki tarayıcıda — giriş
tamamlanmaz. Bağlantının her tarayıcıda çalışması için Authentication →
Email Templates → Magic Link şablonundaki bağlantıyı şununla değiştir:

```
{{ .SiteURL }}/auth/callback?token_hash={{ .TokenHash }}&type=email
```

`/auth/callback` iki biçimi de kabul ediyor; şablon değişmezse eski biçim
çalışmaya devam eder. Not: bu biçimde giriş sonrası dönülecek sayfa
bilgisi taşınmaz, kullanıcı ana sayfaya gelir.

## Komutlar

```bash
npm run dev        # geliştirme sunucusu
npm run build      # üretim derlemesi
npm run start      # derlenmiş sürümü çalıştır
npm run lint       # eslint
npm run typecheck  # next typegen + tsc --noEmit
```

## Durum

Faz 1 / Adım 1 kuruldu: proje iskeleti, veri katmanı (migration + RLS),
oturum yönetimi ve e-posta ile giriş. Başvuru sayfaları (`/onboarding`,
`/applications`, `/applications/new`, `/applications/[id]`) sonraki
adımlarda geliyor.
