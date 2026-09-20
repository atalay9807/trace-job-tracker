<div align="center">

<img src="docs/img/01-ana.png" alt="Trace home page: urgency and match in separate columns, with today's closable work shown as cards" width="880">

# Trace

### A tracking system that prioritises job applications, scores postings against a CV, and derives the skills that are missing

**It answers three questions:** What should I do today? · Where should I spend my energy? · What do I need to learn?

<br>

### [🚀 Live demo — open the app](https://atalay9807.github.io/trace-job-tracker/app.html) &nbsp;·&nbsp; [📖 Overview page](https://atalay9807.github.io/trace-job-tracker/trace.html)

<br>

`Python 3.11+` · `Zero external dependencies` · `Single-file HTML interface` · `9 AI agents` · `7 skills`

[![Checks](https://github.com/atalay9807/trace-job-tracker/actions/workflows/kontrol.yml/badge.svg)](https://github.com/atalay9807/trace-job-tracker/actions/workflows/kontrol.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

[Technical contract](docs/technical-contract.md) · [Production readiness](docs/production-readiness.md) · [Collaboration](docs/collaboration.md) · [Roadmap](ROADMAP.md) · [Contributing](CONTRIBUTING.md)

</div>

> **The interface speaks Turkish.** An English option is planned and will work
> like the light/dark theme switch — see [the roadmap](ROADMAP.md#bilingual-interface).

---

## What it does

When 60+ applications are open at once, three things get lost at the same time:
where each process stands, which one is worth spending energy on, and why you
were screened out. Trace measures those three separately, and **says plainly
what it cannot measure.**

<table>
<tr>
<td width="50%" valign="top">

### 📋 Applications — two axes never mix

Every row keeps **urgency** and **match** in separate columns. A weakly matched
posting can still have an urgent deadline; the decision is left to the user.

Open and closed processes, urgency, match and date are filtered together.
Unscored records are selected separately — they are **never confused with a
score of zero.** Sorting switches between urgency, match, application date,
deadline and company.

</td>
<td width="50%" valign="top">

<img src="docs/img/04-basvurular.png" alt="Applications table: match score, stage, deadline, days of silence, and missing-skill badges">

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🎯 Match — a four-dimension breakdown

Role family (35) + seniority (25) + skill overlap (25) + sector (15) − location
penalty. Not a single number, but a number **whose origin is visible.**

🟢 Strong 78–100 · 🔵 Good 62–77 · 🟡 Medium 45–61 · 🔴 Weak 0–44

</td>
<td width="50%" valign="top">

<img src="docs/img/05-detay.png" alt="Application detail panel: four-dimension match breakdown, process information, and a course card for the missing skill">

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 📊 Reports — what cannot be measured is not invented

The first step of the funnel is drawn as a **hatched bar**: "a lower bound, not
the whole." No conversion is **computed** past it, because LinkedIn does not
report impression data by email.

This is the project's most distinctive decision — no competitor has it.

</td>
<td width="50%" valign="top">

<img src="docs/img/02-raporlar.png" alt="Reports page: application funnel, hatched lower-bound bar, and the measurement-limit warning">

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🎓 Training — from a gap to a resource

The difference between a posting and the profile lands in `gap_skills`, and
from there into a priority-ordered training plan. Course enrolments are
**simulated**, and that is labelled in three separate places.

</td>
<td width="50%" valign="top">

<img src="docs/img/03-egitim.png" alt="Training page: priority-ordered missing skills and course suggestions carrying the simulation label">

</td>
</tr>
</table>

---

## The most important rule: what cannot be measured is not invented

This project is trustworthy because it says out loud what it cannot measure.
Three limits are labelled throughout the interface and are never removed:

| Limit | Why it is unknown | How it appears in the interface |
|---|---|---|
| **Rejection reasons** | No rejection email states one | Missing skills are labelled **"INFERENCE"** |
| **Impression counts** | LinkedIn does not report them by email | The first funnel step is a **hatched bar**; no conversion is computed past it |
| **Course enrolments** | No real course API is connected | The simulation label appears in **three places**: page banner, list, click |

Two rules follow from these: **URLs are never invented** (an unverified link
becomes a Gmail search deep link) and **no third party's name enters the
repository** (recruiters appear as a role label such as
`İK Müdürü — ik@x.example`).

---

## What works today

| Capability | State |
|---|---|
| Application list, filters, sorting, detail panel, two themes | ✅ A web interface running on demo data |
| CSV download of the visible applications | ✅ The active filter and on-screen order are preserved; the file is built in the browser |
| Urgency, match, reminders, eight analysis reports | ✅ Python standard library; makes no model call |
| Interpreting a posting and deriving match dimensions | ⚙️ A Claude Code agent workflow; does not run automatically in the web demo |
| Gmail scanning | ⚙️ Requires a separately authorized session or Routine |
| CV analysis | ⚙️ In an environment that supports `sample`; disabled in the public web demo |
| User accounts, saved data, connecting Gmail from the web | ❌ Not implemented |
| Training resources | ⚠️ Explicitly labelled simulation |

> The web demo connects to no personal account. Application and email action
> links are not included in the public HTML. The date the data was published is
> shown on screen.
>
> **CSV is not a backup or import format** — it exports only the results
> currently on screen, in the same order, and never modifies the source JSON
> files.

Notes from the version reviewed and developed by Codex are in
[`CODEX_CALISMA_ALANI.md`](CODEX_CALISMA_ALANI.md); current work is tracked in
[Issue #4](https://github.com/atalay9807/trace-job-tracker/issues/4).

---

## Quick start

Python 3.11+ is enough; the core has **no external Python dependency.**

```bash
git clone https://github.com/atalay9807/trace-job-tracker.git
cd trace-job-tracker

python3 src/veri.py                         # schema and catalog validation
python3 src/pipeline.py --format markdown   # daily report from stored data
python3 src/match.py                        # match summary and segments
python3 src/insights.py                     # eight reports + the training plan
python3 src/build_dashboard.py --site       # build the demo → site/app.html
```

Tests:

```bash
python3 -m unittest discover -s tests -v    # Python regressions
npm ci --ignore-scripts && npm test         # jsdom DOM tests (Node 20+, no network)
```

Those Node dependencies exist only for the development tests. Real model and
Gmail integration and visual browser tests are outside the scope of these
checks.

---

## Architecture

```
Gmail  ──▶  mail-classification ──▶  data/*.json  ──▶  pipeline.py  ──▶  report
(authorized        (skill)          (single source      match.py        (md/csv/json)
 session)                            of truth)          insights.py
                                          │
              posting-analyzer ──▶   matcher   ──▶  match object
                  (agent)            (agent)             │
                                                         ▼
                                          build_dashboard.py ──▶ site/app.html
```

**The data layer is the single source of truth.** The code reads the seven JSON
files under `data/`; data is never hard-coded.

| Path | Responsibility |
|---|---|
| `data/` | Applications, profile, skills catalog, journey, engagement, saved postings, role targets |
| `src/veri.py` | Data source, schema validation, shared date and status definitions |
| `src/pipeline.py` | Urgency computation, reminders, Markdown/text/CSV/JSON reports |
| `src/match.py` | Summing dimensions and assigning match segments |
| `src/eslesme_kontrol.py` | Validating an agent suggestion without writing it to a file |
| `src/insights.py` | Eight analyses and the training plan |
| `src/build_dashboard.py` | Safe data embedding and demo build |
| `src/anonimlestir.py` | Deriving demo data from real data |
| `src/dashboard.template.html` | Source of the six-page interface |
| `tests/` | Python regressions and DOM behaviour tests |
| `.claude/` | Nine agents and seven skills |
| `site/` | Overview page and the generated demo |
| `web-live/` | The Next.js web application, in its own project |

`reports/pano.html` and `site/_artifact.html` are **generated files** — never
edited by hand; the template is changed and they are rebuilt.

---

## How it was built with AI

The first version was built with Claude Code. Claude Code and Codex work
against the same codebase, data contract and tests.

**Nine agents, one job each.** The posting analyzer and the matcher are
deliberately separate: a single agent that both interprets and scores a posting
starts reading the posting in light of the score it is about to give. Kept
apart, the analyzer produces neutral data.

**The two role advisors are a pair.** One looks only at the CV, the other only
at application outcomes; their evidence bases deliberately do not overlap. A
title they agree on is a strong target, and **where they diverge is the real
information** — the two are never averaged.

- **One writer:** agents return suggestions; the main session writes the record.
- **Validation:** totals, segments, schema and edge cases are checked by code.
- **Reviewable change:** every task runs on its own branch and is delivered with
  test output and remaining limitations.

An agent definition does not imply measured success on every run, nor an AI
service wired into the web application.

[Claude instructions](CLAUDE.md) · [Codex instructions](AGENTS.md) · [Collaboration contract](docs/collaboration.md)

---

## Design system

Three colors do three separate jobs and never blur into each other:

- **Indigo** — brand and volume
- **The purple ramp** (`--m1`…`--m4`, ordered) — match quality only
- **Red / amber / green** — pipeline status

When a color is added, **contrast is measured, never eyeballed:** 4.5:1 for
text, 3:1 for chart fills — separately in both themes. The ramps are monotonic
in lightness. The palette values are in
[`docs/technical-contract.md`](docs/technical-contract.md).

<div align="center">
<img src="docs/img/06-profil.png" alt="Profile page: the skill profile derived from the CV, and role targets" width="49%">
<img src="docs/img/07-baglan.png" alt="Connect page: CV upload and the data-source connection flow" width="49%">
</div>

---

## Data and measurement limits

**Demo versus private data.** The public repository holds **anonymous demo
data** under `data/`; Kerem Aydın is a sample profile, not the project owner.
Real data lives in a separate private repository and is passed in from outside
through the `TRACE_DATA` environment variable:

```bash
TRACE_DATA=/path/private-data/data python3 src/pipeline.py
```

All four scripts read that variable; without it they use the repository's own
`data/` directory. If an external file is missing, the code does **not** fall
back to demo data.

**First response time is a separate measurement.** `last_contact` shows the most
recent contact, not the company's first reply. The duration is computed only
when `first_response` is recorded; the current demo data does not carry that
date, so no median is shown.

**Stages are a snapshot.** Showing every past interview, or the conversion rate
between stages, would require event history. Today's report shows current
stages and invents no sequential conversion.

**Match scores come from an assessment.** `match.py` does not analyse the CV
text itself; it validates and sums previously assigned dimensions. Historical
scores with no source posting text do not count as verified model success.

---

## The road to a live product

This version is **not a multi-user service.** The open work is separated with
its acceptance conditions in the
[production readiness plan](docs/production-readiness.md), and
[`ROADMAP.md`](ROADMAP.md) states what blocks a launch. Three items are
mandatory:

1. **Identity and data isolation** — today all data is embedded into the HTML at
   build time, and a static file has no authentication. There is also nowhere to
   delete from when a user says "delete my data" — a product that names what it
   cannot measure cannot claim to have deleted what it cannot reach.
2. **Server-side Gmail access** — `gmail.readonly` is a restricted scope,
   requiring Google verification and an annual CASA assessment.
3. **Write path and concurrency** — updating a record is currently a git commit.
   It does not break at scale; it breaks at **n = 2**.

A privacy notice also has to be written before launch (Turkish data protection
law exempts small operators from the VERBİS registry, but **the duty to inform
is not covered by that exemption**), and third-party requests (Google Fonts,
cdnjs) have to be removed.

---

## Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a pull request, and
[`SECURITY.md`](SECURITY.md) before reporting a vulnerability. Participation is
governed by the [Code of Conduct](CODE_OF_CONDUCT.md).

---

<div align="center">

**Maintainer: Atalay Denizer** · [GitHub](https://github.com/atalay9807)

Built out of a real job search. It is both a tool its owner uses daily and a
portfolio project shown to employers.

Licensed under the [MIT License](LICENSE).

</div>
