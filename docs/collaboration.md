# Working with Claude Code and Codex on the same repository

Trace is a single codebase. Claude Code and Codex are development tools; the
application does not need two development sessions open to run. The Python
core works independently of both. Claude agent files do not run by themselves
under Codex; the same task rules can be read there when needed.

For Codex the visible entry point is the
[work hub](https://github.com/atalay9807/trace-job-tracker/issues/4), and the
handover log is [CODEX_CALISMA_ALANI.md](../CODEX_CALISMA_ALANI.md). The
working branch `codex/calisma-alani` is the development branch that shows the
user the latest state. New tasks are branched off that branch's current commit
onto their own task branch; two agents never write into the same checkout.
`main` and Pages do not stand in for the current development view. Remote
branches are checked again at the start of the next task.

## Splitting the work

Start every task from the same current commit, on its own development branch
and its own checkout or worktree. Never let two sessions edit the same file at
the same time. When handing work over, state the starting commit, the branch,
which files changed, which checks were run, and what is still broken. The
second tool continues by reading that handover and the diff — the first tool's
description is not test evidence.

Merging to the main branch and publishing are the user's decisions.
Authorized code work does not need repeated approval to finish. Bulk-deleting
or rewriting real data, changing repository visibility, and sending anything
outward each need separate, explicit authorization. The concurrency rules are
session discipline; today's file layout provides no database lock.

## Data sources

- `data/` in the public repository holds demo data. The demo identity is not
  the project owner's identity.
- Real data is kept outside the repository. `TRACE_DATA` passes **one data
  directory** to every script and to the relevant agent. Agents receive an
  absolute directory path and an explicit list of readable files in their task
  input.
- The `data/...` paths in agent instructions are logical paths relative to the
  selected data directory. The rule that the profile-based and history-based
  role advisors never read each other's evidence still holds.
- If an external data file is missing, stop and report it — never fall back to
  the demo profile silently. The dashboard expects all seven JSON files. When
  a private repository holds only applications and profile, the remaining
  files must be prepared for that user; demo CV levels are never copied.
- Scripts never modify the source JSON. Agents return suggestions; a single
  designated writer updates and verifies the source record. Never copy private
  data into the public repository.
- The private dashboard HTML contains all of the data and authenticates
  nobody. It is for personal use and is never uploaded to a public server.
  `--site` accepts the repository's demo data only.

## Verification and handover

```bash
python3 src/veri.py
python3 -m unittest discover -s tests -v
python3 src/build_dashboard.py --site
npm ci --ignore-scripts
npm test
git diff --check
```

The Python core runs on the 3.11+ standard library. Node 20+ and jsdom are
only used by the interface development tests; nothing needs to be installed on
a user's machine, and these checks can run in the cloud or in GitHub Actions.

Edit `src/dashboard.template.html`; never edit `site/app.html` by hand. The
build's reference date is the demo `meta.last_scan` value, so the same input
produces the same site. If `TRACE_DATA` points at private data, switch to the
demo directory before building the site.

The DOM tests check JavaScript behaviour. They do not verify visual layout,
real OAuth, or real model access. Never present a screenshot as refreshed
without refreshing it. The main branch's publish workflow runs these same
checks and builds the site from source.

## Measurement and AI limits

Rejection reasons, impression counts, and real course enrolments are never
invented. An unknown match stays `null`; that does not mean zero fit. A record
with no source posting text never has its numeric score presented as verified.

`first_response` is the date of the first reply that is not an automated
application acknowledgement; it cannot stand in for `last_contact`. Without
historical event data, never present the ratios between current stages as if
they were a sequential conversion funnel. The demo profile and rubric do not
generalize to every candidate.

A matcher's output can be checked before it is written to a record:

```bash
python3 src/eslesme_kontrol.py < /tmp/match-suggestion.json
```

The file contains `match`, `gap_skills`, `hesaplanan_toplam`, `segment`, and
`guven`. This check verifies the arithmetic and the schema. It does not prove
that the posting or the CV was interpreted correctly. A suggestion file built
from real data is never added to the public repository.
