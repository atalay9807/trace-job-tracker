-- Faz 1 şeması: CV, başvuru ve olay tabloları + Row Level Security.
-- Her tabloda user_id auth.users'a bağlıdır; RLS olmadan hiçbir satır okunamaz.

-- ---------------------------------------------------------------- enum'lar

create type application_status as enum (
  'saved', 'applied', 'interview', 'offer', 'rejected'
);

-- Red nedeni ölçülemediğinde uydurulmaz, 'unknown' seçilir.
create type rejection_reason as enum (
  'skill_gap', 'experience', 'position_closed', 'unknown'
);

-- ---------------------------------------------------------------- tablolar

create table cvs (
  id          uuid primary key default gen_random_uuid(),
  user_id     uuid not null references auth.users (id) on delete cascade,
  file_url    text not null,
  uploaded_at timestamptz not null default now()
);

create index cvs_user_id_idx on cvs (user_id, uploaded_at desc);

create table applications (
  id               uuid primary key default gen_random_uuid(),
  user_id          uuid not null references auth.users (id) on delete cascade,
  company          text not null,
  position         text not null,
  job_url          text,
  job_description  text,
  status           application_status not null default 'saved',
  rejection_reason rejection_reason,
  rejection_note   text,
  created_at       timestamptz not null default now(),
  updated_at       timestamptz not null default now(),

  -- Arayüzdeki zorunlu modalın veritabanı karşılığı: 'rejected' nedensiz yazılamaz.
  constraint applications_red_nedeni_zorunlu
    check (status <> 'rejected' or rejection_reason is not null)
);

create index applications_user_id_idx on applications (user_id, status, updated_at desc);

-- Faz 4-5'in dayanacağı olay akışı. Satırlar değiştirilemez, yalnızca eklenir.
create table events (
  id         uuid primary key default gen_random_uuid(),
  user_id    uuid not null references auth.users (id) on delete cascade,
  event_name text not null,
  properties jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index events_user_id_idx on events (user_id, created_at desc);
create index events_name_idx on events (event_name, created_at desc);

-- ------------------------------------------------------------- updated_at

create function set_updated_at() returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger applications_updated_at
  before update on applications
  for each row execute function set_updated_at();

-- -------------------------------------------------------------------- RLS

alter table cvs          enable row level security;
alter table applications enable row level security;
alter table events       enable row level security;

create policy "kendi cv kayitlarini okur" on cvs
  for select using ((select auth.uid()) = user_id);
create policy "kendi cv kaydini ekler" on cvs
  for insert with check ((select auth.uid()) = user_id);
create policy "kendi cv kaydini siler" on cvs
  for delete using ((select auth.uid()) = user_id);

create policy "kendi basvurularini okur" on applications
  for select using ((select auth.uid()) = user_id);
create policy "kendi basvurusunu ekler" on applications
  for insert with check ((select auth.uid()) = user_id);
create policy "kendi basvurusunu gunceller" on applications
  for update using ((select auth.uid()) = user_id)
       with check ((select auth.uid()) = user_id);
create policy "kendi basvurusunu siler" on applications
  for delete using ((select auth.uid()) = user_id);

-- Olaylar için bilerek update/delete politikası yok: geçmiş yeniden yazılamaz.
create policy "kendi olaylarini okur" on events
  for select using ((select auth.uid()) = user_id);
create policy "kendi olayini yazar" on events
  for insert with check ((select auth.uid()) = user_id);

-- ---------------------------------------------------------------- storage

-- CV'ler herkese açık değil; imzalı URL ile okunur.
insert into storage.buckets (id, name, public)
values ('cvs', 'cvs', false)
on conflict (id) do nothing;

-- Dosya yolu <user_id>/<dosya-adi> biçiminde; ilk klasör kimliğin kendisidir.
create policy "kendi cv dosyasini okur" on storage.objects
  for select using (
    bucket_id = 'cvs'
    and (storage.foldername(name))[1] = (select auth.uid())::text
  );
create policy "kendi cv dosyasini yukler" on storage.objects
  for insert with check (
    bucket_id = 'cvs'
    and (storage.foldername(name))[1] = (select auth.uid())::text
  );
create policy "kendi cv dosyasini siler" on storage.objects
  for delete using (
    bucket_id = 'cvs'
    and (storage.foldername(name))[1] = (select auth.uid())::text
  );
