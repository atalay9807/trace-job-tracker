# Verification — web-live Phase 1 Step 1b: hardening after the first review

- Date: 2026-10-02
- Scope: uncommitted working tree on top of 6a2dbff. Modified: `web-live/README.md`, `src/app/auth/callback/route.ts`, `src/app/login/giris-formu.tsx`, `src/app/login/page.tsx`, `src/lib/olaylar.ts`, `src/lib/tipler.ts`. Untracked: `src/lib/giris-hatalari.ts`, `supabase/migrations/0002_faz1_sertlestirme.sql`
- Spec: `web-live/docs/faz-1-spec.md`: Sayfalar §1 (/login), Tablolar, Kurallar (events, RLS, PDF CV). Findings carried over from `web-live/docs/reviews/2026-10-01-step-1-scaffold.md`
- Verdict: PASS WITH NOTES

## Commands run
| Command | Result |
|---|---|
| `npm run typecheck` on a clean copy of the working tree (tracked and untracked files, no `.next/`) | exit 0 |
| `npm run lint` | exit 0 |
| `npm run build` with dummy `NEXT_PUBLIC_SUPABASE_*` | exit 0. Routes unchanged: `/`, `/login`, `/auth/callback`, `/auth/cikis`, Proxy |
| test command | none in `package.json` (N/A) |
| `next start` + curl `/auth/callback` with no params, `?code=x`, `?token_hash=abc&type=email`, `?token_hash=abc`, `?code=x&devam=/%5Cevil.example` | 307 to `hata=baglanti_eksik`, `baglanti_gecersiz`, `baglanti_gecersiz`, `baglanti_eksik`, `baglanti_gecersiz`. No raw Supabase text in any `Location` |
| curl `/login?hata=` with each of the 3 codes, free text, `toString`, `__proto__`, `constructor`, `hasOwnProperty`, and repeated `hata` | Each of the 3 codes renders its fixed Turkish alert. Free text and prototype keys render no alert (`girisHatasi:null`). With repeated params, only the first value counts |
| Chromium (Playwright) at 375×667, light and dark, with a local mock of Supabase `/auth/v1/otp` returning 200, 429 and 500 | `scrollWidth` = 375 in all 8 states. 200 shows the "sent" panel with the new same-browser hint. A long email address wraps. 429 shows the rate-limit text, 500 the generic text. No English error text |
| `node test.mjs` (main session's PGlite script) | 13/13 pass |
| My own PGlite probe, `scratchpad/pgtest/probe.mjs` (same stubs) | See the NOTE on the test script. B's row exists and A cannot see, update, delete or take it over. Events rows survive A's update and delete. `cvs` and storage are isolated per user. `'Signup'` is rejected with 23514 |
| PGlite: apply 0001, insert two `signup` rows for one user, then apply 0002 | `could not create unique index "events_signup_tek"`. The whole of 0002 rolled back (trigger count 0) |
| `git diff --quiet HEAD -- .../0001_faz1.sql`; `git ls-files` / `check-ignore`; grep the diff for `service_role`, `eyJ`, `secret`, out-of-phase terms | 0001 is unchanged. Only `.env.local.example` is tracked. No secrets. The one `matcher` hit is the Next proxy config, a false positive |

## Findings

### [MINOR] Login texts say "open in the same browser", which becomes wrong once the README template change is applied
- Where: `web-live/src/app/login/giris-formu.tsx:56-59`, `web-live/src/lib/giris-hatalari.ts:8-9`, `web-live/README.md:31-45`
- Evidence: I read the code, and the Chromium "sent" state shows: "Bağlantıyı bu tarayıcıda aç. Telefonunda e-posta uygulaması … giriş tamamlanmayabilir." The README tells the owner to switch to the `token_hash` template precisely so that the link works in any browser. After that switch, both texts describe a limitation that no longer exists.
- Why it matters: The texts are correct today. Their accuracy depends on a dashboard setting that the code cannot see, so they will drift without anyone noticing.
- Suggested fix: Pick one path. Either make the template change part of setup and drop the same-browser wording, or keep the wording and add a README line saying it must be removed after the template change.

### [NOTE] What the PGlite test does and does not prove
- Where: `scratchpad/pgtest/test.mjs`
- Evidence: Line 48 discards the result of B's insert, so on its own "A cannot see B's application" (line 50) would also pass if B's row had never been written. I re-checked separately: as superuser B has 1 row, B sees 1, A sees 0, and A's update and delete hit 0 rows while B's data stays the same. Lines 41, 44 and 46 count any error as a pass, not only an RLS denial. In line 54 the superuser's `updated_at = '2020-01-01'` is itself overwritten by the trigger, so the 2020 baseline never exists. The check still fails if the trigger is missing, so it remains valid. The signup uniqueness check is sequential, so concurrency relies on Postgres's unique-index guarantee and was not measured.
- What the stubs prove: the policy expressions, constraints, triggers and index behave correctly in Postgres when the caller is a non-owner role with a given `auth.uid()`.
- What they do not prove:
  - That hosted Supabase's `postgres` role may run `update storage.buckets` and create these objects. The script ran as the PGlite superuser.
  - That the Storage API enforces `allowed_mime_types` or `file_size_limit`. The script only checks that the columns were written.
  - The behaviour of the `anon` role.
  - That PostgREST returns `code: "23505"` to supabase-js. I read this, I did not run it.
- Suggested fix: Assert the result of each setup insert, and match RLS denials on SQLSTATE `42501`.

### [NOTE] 0002 cannot be applied to a database that already has duplicate `signup` rows
- Where: `web-live/supabase/migrations/0002_faz1_sertlestirme.sql:50-52`
- Evidence: Measured in PGlite as shown above. The migration fails as a whole and leaves nothing half-applied.
- Why it matters: This only applies if 0001 already runs on a real project where the old check-then-insert race fired. On a fresh project it does not apply.
- Suggested fix: If 0001 is already live, check `select user_id from events where event_name='signup' group by 1 having count(*)>1` before applying.

### [NOTE] "PDF only" in the bucket checks the declared type, not the file content
- Where: `0002_faz1_sertlestirme.sql:63-66`
- Evidence: Not measured. As far as I know, Supabase Storage compares `allowed_mime_types` with the uploader's Content-Type and does not sniff the bytes.
- Why it matters: For Step 2, a non-PDF file sent with `contentType: 'application/pdf'` would pass. This is still far better than a check in the interface only.
- Suggested fix: None needed now. In Step 2, decide whether a server-side magic-byte check (`%PDF-`) is worth adding.

### [NOTE] Smaller items
- Every repeat login now does a failing insert and leaves a unique-violation ERROR in the Postgres logs. This is expected noise. PostgREST's `on_conflict` cannot target a partial index, so the chosen approach is reasonable.
- The `token_hash` template in the README drops `devam`, as the README says. Using `{{ .RedirectTo }}&token_hash={{ .TokenHash }}&type=email` might keep it, because `emailRedirectTo` already carries `?devam=`. Untested.
- `applications` Insert and Update types still accept `created_at`, and the update policy allows any column. The client can backdate its own applications. This is only the user's own data, but worth considering for Step 3.
- `giris-hatalari.ts` and `0002_…sql` are untracked. `git commit -a` would leave them out and break the build. Add them explicitly.

## Checklist status
1. Build, lint and typecheck: run, all exit 0, including typecheck on a clean copy. There is no test command.
2. Spec: this step adds no new spec scope. It closes the 5 MINOR findings and the race NOTE from the previous report. The 10 MB limit is not in the spec; the migration comment says so.
3. Phase: no code for Steps 2–3 or Phases 2–5. The event list contains only the four Phase 1 events.
4. RLS: there are no new tables. Runtime behaviour was re-checked in PGlite with stubs. `events` still has no update or delete policy.
5. Events: `signup` still fires at `callback/route.ts:60`, and the database now guarantees it is written at most once. The other three events belong to Steps 2–3 (N/A).
6. Two-place rules: the event list, server time and PDF type are now enforced in the database or the bucket, not just in TypeScript. Real enforcement by the Storage API is UNVERIFIED.
7. Secrets and redirects: no secrets. Error texts can no longer be injected via the URL (measured). The redirect guard is unchanged since 6a2dbff.
8. Migrations: the change is a new file, 0002, and 0001 is untouched. The `events` Insert type no longer has `created_at`, and `event_name` is `OlayAdi`, which matches the check constraint.
9. Mobile: `/login` was measured at 375 px in 8 states. `/` was not measured (it needs a session).
10. Generated Python files: N/A. Only `web-live/` changed.

## Not verified
- Real Supabase login through either the `code` or the `token_hash` path, a successful `devam` redirect, and the `signup` row being written: there is no Supabase project here. To verify, log in end to end, twice, and check that `events` holds exactly one `signup` row.
- That 0002 applies on hosted Supabase (`update storage.buckets`, triggers, index as role `postgres`): only PGlite as superuser was tested. To verify, apply it in the SQL Editor and run the Supabase security advisor (it should no longer flag `function_search_path_mutable`).
- Storage MIME and size enforcement: to verify, upload a 1 KB `.txt` and an 11 MB PDF to `cvs` from the app and expect both to be rejected.
- The `token_hash` email template and cross-device login: this is a dashboard setting with no network access from here. To verify, request a link on a laptop and open it on a phone in the mail app's own browser.
- PostgREST returning `code: "23505"` to supabase-js: read, not run.
- Email delivery, and the 375 px layout of `/`: no Supabase, no session.

## Summary for the owner
This step closes everything left over from the first review, and nothing I ran is broken. Login errors now show as short, fixed Turkish messages. A stranger can no longer put their own text on your login page; I tried it and it did not appear. The database itself now stops fake event names, backdated events, double sign-up records and non-PDF uploads. One small cleanup: the login page tells people to open the link in the same browser. That advice becomes outdated once you make the email-template change the README describes, so keep the two in step. Before Step 2, apply migration 0002 on your real Supabase project, try one login from your phone, and try uploading a non-PDF. None of these could be tested here.

Artifacts (scratchpad, not project files): `/tmp/claude-0/-home-user-trace-job-tracker/8237d8ee-20a1-51ca-9258-4d4154c64505/scratchpad/pgtest/probe.mjs`, `mock-sb.mjs`, `mobil1b.cjs`, `1b-{light,dark}-{gecersiz,gonderildi,429,500}.png`.

---

## Main session response

**Fixed in this commit**

- **[MINOR] Same-browser wording.** Took a third path: the texts were rewritten
  so they are true under either email template. Opening the link in the
  browser that started the login works with both the `code` and the
  `token_hash` link, so the advice is now phrased as a fallback ("if it does
  not open, open it in this browser") instead of a limitation. The sent panel
  and `baglanti_gecersiz` both changed; a comment in `giris-hatalari.ts`
  records why. Lint and typecheck exit 0 after the change.
- Untracked files are added explicitly to the commit, as the report warns.

**Accepted, carried forward**

- The PGlite script stays in the scratchpad, not in the repository; adding it
  as a test would mean a new dev dependency, which is the owner's call. If it
  is added, it will assert each setup insert and match RLS denials on `42501`.
- Duplicate `signup` rows before 0002: no live project has run 0001 yet, so
  this does not apply today. The pre-check query is kept here for the day it
  does.
- PDF magic-byte check and the `{{ .RedirectTo }}` template variant: Step 2
  decisions.
- Backdating of the user's own `applications.created_at`: Step 3 design.

**Not disputed.** The repeat-login unique-violation log line is expected.
