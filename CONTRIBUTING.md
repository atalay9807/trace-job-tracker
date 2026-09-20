# Contributing to Trace

Thanks for looking. This is a small, single-maintainer project, so the rules
below are short — but the ones about data and about unmeasurable claims are
not negotiable.

## Before you start

- Open an issue before writing code for anything larger than a typo. The
  project has a narrow scope and a roadmap (`ROADMAP.md`); a pull request that
  does not fit it will be declined no matter how good the code is.
- Read `CLAUDE.md`. It is the project specification, not just an AI prompt:
  scoring formulas, data schema, and design rules all live there.
- Read `docs/ORTAK_CALISMA.md` for the shared working rules between
  development sessions.

## Development setup

There is nothing to install for the Python core.

```bash
git clone https://github.com/atalay9807/trace-job-tracker
cd trace-job-tracker
python3 --version   # 3.11 or newer
```

The Python core uses **only the standard library**. Do not add a runtime
dependency; a pull request that introduces one needs to justify itself in the
issue first.

Node is needed only for the DOM behaviour tests:

```bash
npm ci --ignore-scripts
```

The web application under `web-live/` is a separate Next.js project with its
own dependencies and its own `CLAUDE.md`. See `web-live/README.md`.

## Running things

```bash
python3 src/pipeline.py          # reports (md / text / csv / json)
python3 src/match.py             # match summary and segments
python3 src/insights.py          # eight reports plus the training plan
python3 src/build_dashboard.py   # build the UI into reports/pano.html
```

All four scripts read their data from the repository's own `data/` directory
unless the `TRACE_DATA` environment variable points somewhere else:

```bash
TRACE_DATA=/path/to/data python3 src/pipeline.py
```

## Verification — run this before every pull request

```bash
python3 src/veri.py
python3 -m unittest discover -s tests -v
python3 src/build_dashboard.py --site
npm ci --ignore-scripts
npm test
git diff --check
```

CI runs exactly these. A pull request that fails them will not be reviewed
until it passes.

**Do not claim a check passed without running it.** "I could not test this"
is an acceptable thing to write in a pull request. Saying it works when you
did not check is not.

## Generated files

`reports/pano.html` and `site/_artifact.html` are generated and ignored by
git. `site/app.html` is generated *and* tracked, because it is the published
version.

Never edit a generated file by hand. Edit `src/dashboard.template.html`, then
regenerate:

```bash
python3 src/build_dashboard.py --site
```

CI fails if `site/app.html` differs from what the template produces.

## Data rules

The `data/` directory in this repository holds **anonymous demo data**. It is
not anyone's real job search.

- Never commit real application records, a real CV-derived profile, or a
  screenshot containing either.
- Never commit a third party's name or email address. Recruiters and hiring
  managers are represented by their role and a `.example` domain
  (`Hiring Manager — hr@x.example`). RFC 2606 guarantees `.example` can never
  resolve to a real address.
- Never invent a URL. Only links verified in an email are stored as real
  URLs; anything else becomes a Gmail search deep link.
- Unknown values are `null` or `—`. They are never a guess.

## The three measurement limits

Trace is trustworthy because it says what it cannot measure. These labels are
in the interface on purpose and **must not be removed or softened**:

| Limit | Why | How it is shown |
|---|---|---|
| Rejection reasons are unknown | No rejection email states one | Missing skills are labelled as *inference* |
| There is no impression data | LinkedIn does not report it | The first funnel step is a hatched "lower bound" bar; no conversion rate is computed past it |
| Course enrolments are simulated | No course API is connected | Labelled in three places: page banner, list item, click notification |

A pull request that removes one of these labels, or presents simulated data
as real, will be declined.

## Code style

- Python: standard library only, 3.11+, no formatter enforced — match the
  surrounding code.
- **Code is written in English**: identifiers, comments, docstrings, commit
  messages, documentation.
- **The product speaks both Turkish and English.** The interface ships a
  language switch that works like the light/dark theme switch, and Turkish is
  the default. Never hard-code a user-visible string in one language — add
  both the `tr` and the `en` entry to the locale table.
- Free text written by the user or carried in `data/` (record notes, match
  rationales, next steps) is stored as written and is not translated at
  runtime. The switch changes the interface, not the contents of a record.

## Commits and pull requests

- Write commit messages in English. First line ≤ 72 characters, imperative
  mood. The body explains **why**, not what — the diff already says what.
- Do not put a model name or a session identifier in a commit message.
- Branch off `main`. Merge into `main` happens with `--no-ff` and is the
  maintainer's call.
- One topic per pull request. A finished small change beats three unfinished
  large ones.
- Fill in the pull request template, including which verification commands
  you actually ran.

## Constants live in two places

Stage weights and dimension sizes are in `src/veri.py`, urgency thresholds in
`src/pipeline.py`, and segment boundaries in `src/match.py`. The same numbers
are documented in `config/rules.yaml` and in the skill files under
`.claude/skills/`.

If you change a constant, change its documentation in the same commit.
Otherwise the code and the rubric drift apart, and the rubric is what the
next contributor reads.
