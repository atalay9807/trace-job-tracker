-- Faz 1 sertleştirme: 0001'in bağımsız denetiminde bulunan veri kurallarını
-- veritabanına taşır (web-live/docs/reviews/2026-10-01-step-1-scaffold.md).
-- 0001 düzenlenmez; uygulanmış bir migration'ı değiştirmek, onu çalıştırmış
-- veritabanlarıyla kodun ayrışması demektir.

-- ------------------------------------------------------------- updated_at

-- Sabit search_path: fonksiyon çağıranın şema yoluna göre farklı bir now()
-- ya da tablo çözemesin (Supabase güvenlik danışmanı uyarısı).
create or replace function set_updated_at() returns trigger
language plpgsql
set search_path = ''
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

-- ----------------------------------------------------------------- events

-- Olay zamanını istemci değil sunucu yazar. RLS kullanıcının yalnızca kendi
-- satırını eklemesine izin veriyordu ama created_at'i geçmişe atmasını
-- engellemiyordu; Faz 4-5'in ölçümü bu sıraya dayanıyor.
create function events_zamani_sunucuda() returns trigger
language plpgsql
set search_path = ''
as $$
begin
  new.created_at = now();
  return new;
end;
$$;

create trigger events_created_at
  before insert on events
  for each row execute function events_zamani_sunucuda();

-- Kapalı olay listesi src/lib/tipler.ts'teki OlayAdi ile aynıdır. Yeni bir
-- olay eklemek için iki yer birlikte değişir: bu kısıt (yeni migration ile)
-- ve OlayAdi.
alter table events
  add constraint events_ad_listesi
  check (event_name in (
    'signup', 'cv_uploaded', 'application_created', 'status_changed'
  ));

-- signup kullanıcı başına bir kez. Uygulama tarafındaki "önce say, sonra
-- ekle" kontrolü iki eşzamanlı girişte (çift tıklanan bağlantı) iki satır
-- yazabiliyordu; tekilliği veritabanı garanti eder.
create unique index events_signup_tek
  on events (user_id)
  where event_name = 'signup';

-- ---------------------------------------------------------------- storage

-- Spec CV için PDF istiyor; tür kontrolü yalnızca tarayıcıda kalırsa
-- atlatılabilir. 10 MB sınırı spec'te yok, bizim seçimimiz: tek sayfalık bir
-- CV PDF'i bunun çok altında kalır.
-- Bucket'a bilerek update politikası verilmiyor: her yükleme yeni bir yola
-- yazılır (upsert yok), eski dosya gerekirse silinir.
update storage.buckets
set allowed_mime_types = array['application/pdf'],
    file_size_limit    = 10485760
where id = 'cvs';
