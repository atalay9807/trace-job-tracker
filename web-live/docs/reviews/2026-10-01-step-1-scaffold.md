# Verification — web-live Phase 1 Step 1: scaffold, Supabase schema and email (magic-link) login

- Date: 2026-10-01
- Scope: commit 69b564e (25 files under `web-live/`); 267f476 and 34902b7 were read only for spec, rules and context
- Spec: `web-live/docs/faz-1-spec.md`: Stack, Tablolar, Sayfalar §1 (/login), Kurallar (events, RLS); rules from `web-live/CLAUDE.md` and root `CLAUDE.md`
- Verdict: PASS WITH NOTES

## Commands run
| Command | Result |
|---|---|
| `npm run typecheck` (working tree, with existing `.next/`) | exit 0 |
| `npx tsc --noEmit` on a clean `git archive HEAD` checkout (no `.next/`) | exit 2: `Cannot find name 'LayoutProps'`, `Cannot find name 'PageProps'` |
| `npm run lint` | exit 0 |
| `npm run build` with dummy `NEXT_PUBLIC_SUPABASE_*` | exit 0. Routes: `/`, `/login`, `/auth/callback`, `/auth/cikis`, Proxy. Warning: workspace root inferred as repo root (two lockfiles) |
| test command | none defined in `package.json` (N/A) |
| `next start` + curl: `/`, `/applications` with no session | 307 → `/login?devam=%2F` / `?devam=%2Fapplications` |
| curl `/auth/callback` (no params), `?code=x` | 307 → `/login?hata=…` (PKCE error passed through verbatim) |
| curl `POST /auth/cikis` | 303, `Location: /login` |
| Chromium (Playwright) 375×667, light and dark: `/login`, `/login?hata=<long text>`, submit form | `scrollWidth` 375 = `clientWidth`. Input and button span 16–359 px, height 40–42 px, input font 16 px. Only external request goes to the Supabase URL (no font/CDN calls) |
| Chromium test of the `guvenliYol` logic (copied verbatim) behind a 307 | `/\evil.example/x` and `/<TAB>/evil.example/x` both navigate to `http://evil.example/x` |
| `git ls-files web-live`, `git check-ignore` | `tsconfig.tsbuildinfo`, `next-env.d.ts`, `.next/`, `.env*` are ignored and untracked; only `.env.local.example` is tracked |
| grep for secrets, `service_role`, out-of-phase terms | no secrets (one `eyJ` hit is an npm integrity hash, a false positive); no service-role use; no out-of-phase code |
| Read `next/dist/.../app-route/module.js` | Session cookies set with `cookies()` are merged into the plain `Response` the callback returns (line ~524), so the relative-Location redirect keeps the session |

## Findings

### [MAJOR] Open redirect after login: `devam` guard is bypassable with a backslash or tab
- Where: `web-live/src/app/auth/callback/route.ts:8-11`, `web-live/src/app/login/page.tsx:8-12`
- Evidence: The guard rejects only values that do not start with `/` or that start with `//`. I put the same function behind a 307 and opened it in Chromium. `devam=/\evil.example/x` and `devam=/%09/evil.example/x` both navigated to `http://evil.example/x`. The login page sends `devam` into `emailRedirectTo` unchanged. Supabase's allow-list only checks the outer callback URL, so a link like `/login?devam=/%5Cevil.example` takes the victim to the external site right after a real login. I could not run the full chain because a successful login needs Supabase. The guard bypass itself is measured.
- Why it matters: Checklist 7 requires redirect targets limited to the site's own paths. An attacker can use this for phishing that starts on the real login page.
- Suggested fix: Parse with `new URL(aday, "http://x")` and accept only when `origin` is unchanged. Or allow-list on `^/[A-Za-z0-9/_-]*$` and reject `\` and control characters. Keep one shared helper so the two copies cannot drift apart.

### [MINOR] `npm run typecheck` fails on a fresh clone
- Where: `web-live/package.json:10`, `src/app/layout.tsx:11`, `src/app/login/page.tsx:21`
- Evidence: On a clean `git archive` checkout, `tsc --noEmit` reports `TS2304 Cannot find name 'LayoutProps'` / `'PageProps'`. It passes only after `next build` has generated `.next/types`.
- Why it matters: CI, or the next session, will see a red typecheck that has nothing to do with its own change.
- Suggested fix: Change the script to `next typegen && tsc --noEmit`, or use explicit prop types.

### [MINOR] Login page shows any text from the URL, plus raw English Supabase errors
- Where: `web-live/src/app/auth/callback/route.ts:22-24,51-52`, `web-live/src/app/login/page.tsx:34`, `giris-formu.tsx:93`
- Evidence: `/login?hata=<anything>` is rendered as a red alert. React escapes it, so this is not XSS, but anyone can write any message there. The callback passes Supabase's error through unchanged. The screenshot shows a 6-line English "PKCE code verifier not found…" message, and a failed send shows "Failed to fetch".
- Why it matters: Message spoofing on the real domain. The target user is non-technical and Turkish-speaking.
- Suggested fix: Pass an error code (`hata=baglanti_gecersiz`) and map it to fixed Turkish text. Log the raw error on the server.

### [MINOR] Magic link fails when opened in another browser or device; the README does not cover it
- Where: `web-live/src/app/auth/callback/route.ts:38-46`, `web-live/README.md:24-27`
- Evidence: `?code=` without the verifier cookie returns the PKCE error above (curl). The `token_hash` branch that avoids this only works if the Supabase email template is changed, and the README does not mention it.
- Why it matters: On a phone, mail apps often open links in their own in-app browser. For a mobile-first user, login will fail without a clear reason.
- Suggested fix: Document the email-template change to `{{ .SiteURL }}/auth/callback?token_hash={{ .TokenHash }}&type=email`, or explain the limitation on the login page.

### [MINOR] Events can be backdated or invented by the client
- Where: `web-live/supabase/migrations/0001_faz1.sql:47-53,99-100`, `src/lib/tipler.ts:94-97`
- Evidence: The insert policy only checks `user_id`. `created_at` and `event_name` can be set by the client (the Insert type even allows `created_at`). The closed `OlayAdi` list exists only in TypeScript.
- Why it matters: The commit message says history cannot be rewritten. A user cannot edit rows, but can insert rows with past timestamps or with event names that are not in the list. Phases 4–5 depend on this stream. The effect is limited to the user's own rows.
- Suggested fix: Add a `before insert` trigger that sets `created_at = now()` (or revoke insert on that column), plus a `check (event_name in (...))` constraint.

### [MINOR] The CV bucket has no type or size limit, so "PDF only" will be enforced in the interface only
- Where: `web-live/supabase/migrations/0001_faz1.sql:105-107`
- Evidence: The bucket is created with only `id, name, public`. There is no `allowed_mime_types` and no `file_size_limit`. There is also no `update` policy on `storage.objects`, so an upload with `upsert: true` in Step 2 would be denied.
- Why it matters: The spec says PDF. If Step 2 checks the file type only in the browser, that is a MAJOR finding under checklist 6.
- Suggested fix: In a new migration (not by editing 0001), set `allowed_mime_types = '{application/pdf}'` and a size limit. Decide whether CV replacement uses upsert or delete+insert.

### [MINOR] `set_updated_at()` has a mutable `search_path`
- Where: `web-live/supabase/migrations/0001_faz1.sql:60-67`
- Evidence: There is no `set search_path = ''`. The Supabase security advisor flags this (`function_search_path_mutable`).
- Suggested fix: Add `set search_path = ''` in a new migration.

### [NOTE] `signup` deduplication can race
- Where: `web-live/src/lib/olaylar.ts:51-68`
- Evidence: The code checks the count, then inserts. Two callbacks at once (for example a double-clicked link) can both insert.
- Suggested fix: Add a partial unique index `on events (user_id) where event_name = 'signup'`.

### [NOTE] What Step 1 leaves for Steps 2–3
- `olayYaz` accepts any `Record<string, unknown>`, so nothing forces `status_changed` to carry `from` and `to`. A per-event property type would. The status update and its event are two separate requests and are not atomic. A database trigger on `applications.status` would guarantee the event fires.
- `cvs.file_url` points into a private bucket. Store the object path, not a URL, because signed URLs expire.
- The check constraint only works in one direction. When a card leaves `rejected`, the old `rejection_reason` stays on the row.
- Schema and `tipler.ts` agree column by column, and the enum values match the spec exactly. The foundation supports Steps 2–3.

### [NOTE] Build infers the repo root as the workspace root
- Where: `web-live/next.config.ts`
- Evidence: The build warns that it detected multiple lockfiles and selected `/home/user/trace-job-tracker/package-lock.json`.
- Suggested fix: Set `turbopack.root` (and `outputFileTracingRoot`) to `web-live`.

## Checklist status
1 Build/lint/typecheck: run. They pass in the working tree. Typecheck fails on a clean clone (MINOR). There is no test command.
2 Spec: `/login`, the tables, RLS and the bucket are present. Sign-out and the placeholder `/` are not in the spec but are reasonable support pieces.
3 Phase: no code from Steps 2–3 or Phases 2–5. `STATU_SIRASI` and its labels are Phase 1 constants only.
4 RLS: enabled on `cvs`, `applications` and `events`. `events` has no update or delete policy. Storage has select, insert and delete policies.
5 Events: `signup` fires at `callback/route.ts:63`. The other three events belong to Steps 2–3 (N/A this step).
6 Two-place rules: the rejection reason is enforced by a database check. PDF-only is not yet enforced anywhere (see MINOR).
7 Secrets and redirects: no secrets tracked, no service-role key. The redirect guard is bypassable (MAJOR).
8 Migrations: one new file. Types match the SQL.
9 Mobile: `/login` tested at 375 px. `/` was not tested (see below).
10 Generated Python files: N/A, the commit touches only `web-live/`.

## Not verified
- Real magic-link login, session cookie refresh, sign-out invalidation: no Supabase project or credentials. To verify, log in end to end against a Supabase project.
- RLS at runtime (cross-user reads and writes, events update/delete denied, storage folder isolation): no Postgres or Supabase available. To verify, apply 0001 and run queries as two users.
- That the migration runs at all: it was reviewed by reading only. To verify, run `supabase db reset` or use the SQL Editor.
- Magic-link email delivery and Supabase redirect allow-list behaviour: no network access to Supabase.
- `signup` event actually written: depends on a successful login.
- 375 px layout of `/` (the signed-in page): it needs a session.
- The open-redirect chain end to end through Supabase: the guard bypass was measured in Chromium, the full login flow was not.

## Summary for the owner
The groundwork is solid. It builds, passes its own checks, gives each user their own data at the database level, and the login page fits a phone screen. One security gap must be fixed before Step 2: an attacker can craft a login link that sends you to an outside website right after you log in. It is a small fix in one function. Also fix soon: the type check fails on a fresh copy of the project, error messages appear in raw English, and the login link may not work if you open it from your phone's mail app. None of the real login, email or database protections could be tried here because there is no Supabase project. They still need one live test on your Supabase account.

Artifacts (scratchpad, not project files): `/tmp/claude-0/-home-user-trace-job-tracker/8237d8ee-20a1-51ca-9258-4d4154c64505/scratchpad/login-*.png`, `redir.js`, `mobil.js`.

---

## Main session response

**Fixed in this commit**

- **[MAJOR] Open redirect.** Both copies are replaced by one shared helper,
  `src/lib/guvenli-yol.ts`. It rejects backslashes and control characters,
  parses the candidate with `new URL`, and accepts it only if the origin is
  unchanged. Re-tested in Chromium behind a 307 with 11 inputs, including both
  bypasses from this report, `/\n/…`, `/./\…` and an absolute URL: 0 left the
  site, and `/applications?x=1#y` survived intact. In the running app,
  `/login?devam=/%5Cevil.example/x` and `?devam=/%09/evil.example/x` now pass
  `devam: "/"` to the form.
- **[MINOR] Typecheck on a fresh clone.** The script is now
  `next typegen && tsc --noEmit`. It exits 0 on a clean copy without `.next/`.
  `npm run lint` and `npm run build` also exit 0.

**Accepted, not fixed yet: the next small step, before Step 2**

- Error messages: switch to error codes mapped to fixed Turkish text.
- Magic link on another device: document the `token_hash` email template in
  the README.
- A new migration `0002`: server-set `events.created_at`, a check on
  `event_name`, PDF-only and a size limit on the `cvs` bucket,
  `set search_path = ''` on `set_updated_at()`, and a unique index for
  `signup`.

**Carried into Step 2 and Step 3 design**

- `status_changed` needs a typed `from`/`to` payload, ideally written by a
  database trigger so the status change and its event cannot diverge.
- Store the storage object path in `cvs.file_url`, not a signed URL.
- Clear `rejection_reason` when an application leaves `rejected`.

**Not disputed.** The workspace-root build warning (NOTE) is left as is; it is
harmless.
