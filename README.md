<div align="center">

# Trace

**A job-application tracker that prioritises what to do today, scores stored
posting and CV assessments, and reports the skills that are missing.**

Built out of a real job search. The public repository carries 68 demo
records; Kerem Aydın is a sample profile, not the project owner.

[**Overview →**](https://atalay9807.github.io/trace-job-tracker/trace.html) ·
[**Live demo →**](https://atalay9807.github.io/trace-job-tracker/app.html) ·
[Technical contract](docs/technical-contract.md) ·
[Roadmap](ROADMAP.md) ·
[Contributing](CONTRIBUTING.md)

[![Checks](https://github.com/atalay9807/trace-job-tracker/actions/workflows/kontrol.yml/badge.svg)](https://github.com/atalay9807/trace-job-tracker/actions/workflows/kontrol.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![No dependencies](https://img.shields.io/badge/dependencies-none-brightgreen.svg)](#running-and-testing)

</div>

> The interface speaks Turkish. An English option is planned — see
> [the roadmap](ROADMAP.md#bilingual-interface).

## What works today

| Capability | Current state |
|---|---|
| Application list, filters, details, two themes | A web interface running on demo data |
| Urgency, match, reminders, and reports | Runs on the Python standard library; makes no model call |
| Interpreting a posting and deriving match dimensions | A Claude Code agent workflow; does not run automatically in the web demo |
| Gmail scanning | Requires a separately authorized development session or Routine; the repository commands never scan Gmail |
| Personal CV analysis | Disabled in the public web demo; available with explicit consent in a Claude environment that supports `sample` |
| Connecting Gmail from the web, user accounts, saved data | Not implemented |

The web demo connects to no personal account. Application and email action
links are not included in the public HTML. The date the data was published is
shown on screen. Where CV analysis is supported, the result is only displayed:
it never rewrites the stored profile or existing match scores. The PDF reader
loads only in a supported environment when a PDF is chosen, and analyses the
first 6 pages and at most 14,000 characters.

## The problem it solves

When many applications are open at once, three decisions get hard:

| Question | How Trace answers it |
|---|---|
| What should I do today? | Reminders based on deadline, process stage, and silence |
| Where should I spend my energy? | A 0–100 match score with a per-dimension breakdown, from the stored assessment |
| What do I need to learn? | Gaps inferred from posting/profile differences, ranked by priority |

Urgency and match are separate axes. A job being urgent does not mean it suits
the candidate; the interface keeps the two in separate columns and leaves the
decision to the user.

## How it is developed with AI

The first version was built with Claude Code. Claude Code and Codex work
against the same codebase, data contract, and tests. Nine Claude agents split
work such as posting analysis, matching, interview preparation, data auditing,
and strategy. Seven skills carry the task rules. An agent definition does not
imply measured success on every run, nor an AI service wired into the web
application.

- **Separate evidence:** the posting analyser never reads the CV; the matcher
  compares the structured posting against the selected profile.
- **One writer:** agents return suggestions; the main session updates the
  record.
- **Validation:** totals, segments, schema, and edge cases are checked by
  code.
- **Reviewable change:** every task runs on its own branch and is handed over
  with test output and remaining limitations.

[Claude instructions](CLAUDE.md) · [Codex instructions](AGENTS.md) ·
[Collaboration contract](docs/collaboration.md)

## Running and testing

Python 3.11+ is enough; the core has no external Python dependency. These can
also be run in a cloud development environment.

```bash
python3 src/veri.py                         # schema and catalog validation
python3 src/pipeline.py --format markdown   # daily report from stored data
python3 src/pipeline.py --format csv        # tabular output
python3 src/match.py                        # match summary
python3 src/insights.py                     # analyses
python3 src/build_dashboard.py              # personal dashboard → reports/pano.html
python3 src/build_dashboard.py --site       # demo only → site/app.html
python3 -m unittest discover -s tests -v
```

The interface behaviour tests run under Node 20+ in jsdom, with no network
access:

```bash
npm ci --ignore-scripts
npm test
```

Those dependencies exist only for the development tests. Real model and Gmail
integration and visual browser tests are outside the scope of these checks.
GitHub Actions runs the tests; on the main branch the Pages workflow builds
the site from the template after the tests pass. Merging to the main branch
starts a release.

## Data and measurement limits

**Demo versus private data.** Real data lives in a separate private
repository. `TRACE_DATA` points at the selected data directory. If an external
file is missing, the code does not fall back to demo data. The dashboard
expects all seven JSON files; details are in the
[technical contract](docs/technical-contract.md).

**Rejection reasons are unknown.** In the demo assessments, 7 of 15 rejection
records are marked with a team-management gap. That does not prove the
rejections were given for that reason, and 7/15 is not a majority. Gaps are
presented as inference.

**First response time is a separate measurement.** `last_contact` shows the
most recent contact, not the company's first reply. The duration is computed
only when `first_response` is recorded. The current demo data does not carry
that date, so no median is shown.

**Stages are a snapshot.** Showing every past interview, or the conversion
rate from one stage to the next, would require event history. Today's report
shows current stages and invents no sequential conversion.

**There is no impression data.** Saved postings cover only the records on
hand; no application conversion rate is computed from that number.

**Match scores come from an assessment.** `match.py` does not analyse the CV
text itself; it validates and sums previously assigned dimensions. Historical
scores with no source posting text do not count as verified model success. An
unscored record stays `null`.

**Courses are simulated.** Titles, durations, ratings, and prices are
examples. No guarantee is made about a candidate's success or the effect of
any training on finding a job.

## Repository layout

| Path | Responsibility |
|---|---|
| `data/` | Seven JSON files: applications, profile, skills catalog, journey, engagement, saved postings, role targets |
| `src/veri.py` | Data source, schema validation, shared date and status definitions |
| `src/pipeline.py` | Urgency, reminders, Markdown/text/CSV/JSON reports |
| `src/match.py` | Summing dimensions and assigning match segments |
| `src/eslesme_kontrol.py` | Validating an agent suggestion without writing it to a file |
| `src/insights.py` | Analyses and the training plan |
| `src/build_dashboard.py` | Safe data embedding and demo build |
| `src/dashboard.template.html` | Source of the six-page interface |
| `tests/` | Python regressions and DOM behaviour tests |
| `.claude/` | Claude agents and task skills |
| `site/` | Overview page and the generated demo |
| `web-live/` | The Next.js web application, in its own project |

## Interface screenshots

The image below is an archive of the first prototype; current feature support
is described in the table above and in the generated demo of the relevant
branch. The screenshots were not retaken in the latest remediation package.

![Home page of the first prototype](docs/img/01-ana.png)

## The road to a live product

This version is not a multi-user service. User accounts and data isolation,
persistent storage and concurrency, server-side Google authorization, a job
queue, real model integration, and measured costs are all open work for a live
release. The [production readiness plan](docs/production-readiness.md)
separates them with their acceptance conditions, and [`ROADMAP.md`](ROADMAP.md)
states what blocks a launch.

## Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a pull request, and
[`SECURITY.md`](SECURITY.md) before reporting a vulnerability. Participation
is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

[MIT](LICENSE) © 2026 Atalay Denizer · [GitHub](https://github.com/atalay9807)
