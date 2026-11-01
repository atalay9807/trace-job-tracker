# Verification: maintenance pass (Next.js 16.4.3, pending-step reminder, stale figures)

- Date: 2026-11-01
- Scope: uncommitted working tree on `claude/bakim-2026-11-01` against `origin/main`, 14 modified files, nothing untracked
- Spec: none. This is maintenance, not a Phase 1 step. Phase 1 checks 2 to 8 are N/A: no pages, migrations, tables or events changed.
- Verdict: PASS WITH NOTES

## Commands run
| Command | Result |
|---|---|
| `python3 src/veri.py` | "Doğrulandı: 109 başvuru.", exit 0 |
| `python3 -m unittest discover -s tests -v` | 30/30 OK, including `test_bekleyen_adim_deadline_yoksa_hatirlatilir` |
| `python3 src/build_dashboard.py --site`, run twice | Output byte-identical to the working tree both times (sha1 `35f021e9…`). The diff against main is 7 `reminders` arrays, each changing from `[]` to one 📌 line. Nothing else changed |
| `npm ci --ignore-scripts && npm test` (root) | 25/25 pass, 0 vulnerabilities |
| `git diff --check` | exit 0 |
| web-live `npm ci` | OK. `next@16.4.3`, `sharp@0.35.5`, `source-map-js@1.2.2` |
| web-live `npm run lint` / `npm run typecheck` | exit 0 / exit 0 |
| web-live `npm run build` with dummy `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` (the names come from `ortam.ts`) | exit 0. Routes unchanged: `/`, `/_not-found`, `/auth/callback`, `/auth/cikis`, `/login`, Proxy |
| `npm audit --omit=dev` | 0 vulnerabilities |
| `npm audit` | 16 moderate, 0 high, 0 critical. All 16 come from `minimatch` in the eslint toolchain |
| `npm audit --package-lock-only` on the `origin/main` lockfile (scratchpad copy) | 1 critical (`next` 16.0.0–16.4.0), 3 high (`sharp`, `source-map-js`, `zod`) |
| grep the diff for secrets; `git ls-files` for `.env` | Only `.env.local.example` is tracked. One hit is a lockfile integrity hash (false positive) |

## Findings

### [MINOR] Stale "68" figures are only partly replaced
- Where: `.claude/skills/add-application/SKILL.md:3,14,89`, `.claude/skills/cv-analysis/SKILL.md:10`, `.claude/skills/role-targeting/SKILL.md:57`, `.claude/agents/market-researcher.md:84`, `.claude/agents/matcher.md:22`, `CLAUDE.md:12,334,341`
- Evidence: Running `grep -n "\b68\b"` still finds these lines. Some of them are history ("built on 68", "bands derived from 68") and are fine as they are. Others read as current facts: `add-application:89` says "6 of 68 records" have a contact, but the demo data now has 7 of 109. `cv-analysis:10` says "all 68 applications". `role-targeting:57` uses `"basvuru_sayisi": 68` as its example.
- Why it matters: Item 3 claims the figures were replaced. A reader will take the remaining ones as current.
- Suggested fix: Date-stamp the historical mentions, and replace or generalise the ones that read as current.

### [NOTE] Some critical records still have no reminder line
- Where: `src/pipeline.py:117-124`, compared with `band()` at `:88`
- Evidence: In the built `site/app.html`, 14 `action_required` records are all critical. 12 now carry a reminder. Two have no deadline and have been silent for 2 and 11 days, so they get no reminder line.
- Why it matters: The code comment says the user "couldn't see why it was critical". That is still true for silences under 12 days. This may be intended: the 12-day threshold matches `STALE_DAYS` and the skill row.
- Suggested fix: The owner decides whether a no-deadline `action_required` record should show the 📌 line from day 0.

### [NOTE] `npm audit fix` changed more than the brief lists
- Evidence: The lockfile diff also bumps `zod` 4.6.5→4.6.7, which closes a fourth high advisory (dev-only, through `eslint-plugin-react-hooks`), and `typescript-eslint` 8.70.0→8.72.1. 53 lockfile entries changed in total. All of them are patch/minor bumps of `next`, `sharp`, `@img/*`, `@next/*`, `typescript-eslint`, `source-map-js` and `zod`.

### [NOTE] Lockfile warning carried over
- Evidence: `next build` still infers the repo root because there are two lockfiles. This was already reported on 2026-10-01 and is unchanged by this pass.

### [NOTE] `next/og` not used
- Evidence: grep finds no `next/og`, `ImageResponse`, `use cache` or `draftMode` in `web-live/src`. The critical advisory's RCE path was not reachable before the bump either.

## Not verified
- Runtime behaviour of Next 16.4.3 with real Supabase auth: no credentials in this session. The upgrade is verified at build level only. A login round-trip on a preview deploy would verify it.
- Layout of the longer 📌 reminder lines on the dashboard cards at 375 px: no visual check was run. A Playwright screenshot of `site/app.html` would verify it.
- `config/rules.yaml`: no code reads it. It is a reference document, so its new row was checked by reading, not by execution.

## Summary for the owner
The update is safe to build on. The serious security warnings in the web app (one critical, three high) are gone, and the app still builds, lints and typechecks. What remains are 16 moderate warnings in developer-only tools, which never reach users. The new "a step is waiting on you" reminder works and is tested. It now appears on 7 demo applications that were marked urgent without explanation. A few old "68 applications" mentions are still in the instruction files and should be cleaned up next time. Nothing has to be fixed before committing.

---

## Main session response

**Process note.** The first commit on this branch was pushed before this
report arrived. The report reviewed exactly that working tree (14 files), so
the verified content and the committed content are the same; the order of
commit and review is what deviated from `web-live/CLAUDE.md`.

**Fixed in this commit**

- **[MINOR] Stale "68" figures.** The ones that read as current facts are
  replaced: `add-application` (contact count now "7 of 109, 01.11.2026"),
  `cv-analysis` ("all applications"), `role-targeting` example
  (`"basvuru_sayisi": 109`). `add-application:14` is date-stamped as the
  first 68 real records of September 2026. Kept as history, because they
  describe a past cohort: `CLAUDE.md:12,334,341`, `matcher.md:22`,
  `market-researcher.md:84`. `add-application:3` was checked and contains no
  count.

**Left to the owner**

- **[NOTE] Reminder from day 0.** Kept at 12 days on purpose: the same
  threshold as the follow-up reminder for other statuses, so one rule covers
  both. Showing it from day 0 is a product decision.

**Accepted, no action**

- Extra lockfile bumps (`zod`, `typescript-eslint`): patch/minor, all close
  advisories or ride along with them.
- Two-lockfile root warning and the 375 px check: carried over from
  2026-10-01, still open.
