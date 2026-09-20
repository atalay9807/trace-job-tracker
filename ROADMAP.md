# Roadmap

This file says what Trace cannot do yet and in what order those gaps matter.
It is deliberately blunt: a tool whose selling point is naming its own limits
cannot keep a vague roadmap.

Nothing here has a date. This is a one-person project.

## Where the project stands

Working today:

- Application list, filters, detail view, and two themes, running on demo data.
- Urgency scoring, match scoring, reminders, and eight analysis reports —
  computed by the Python standard library, with no model call.
- Job-posting interpretation and match dimensions, as an agent workflow inside
  an authorized development session.

Not working yet:

- Connecting a Gmail account from the web.
- User accounts and persisted data.
- Automatic extraction of job-posting text.

## Blocking — the product does not work for a second user without these

### 1. Identity and data isolation

`src/build_dashboard.py` embeds every record into the HTML at build time
(~195 KB, about 2,170 bytes per application). A static file has no
authentication: whoever has the URL sees everything.

Worse, there is nowhere to delete from. A product whose premise is naming what
it cannot measure cannot claim to have deleted data it cannot reach.

The `web-live/` application is the answer to this: Postgres with Row Level
Security, real sessions, and a delete path.

### 2. Server-side Gmail access

Today's scanning runs under the maintainer's own identity inside a Claude Code
session. For a second user that is not a product — it is a service performed
by hand.

`gmail.readonly` is a **restricted scope**. It requires Google verification
and an annual CASA assessment. Published cost figures for that assessment
contradict each other, and no plan should be built on a contradiction that has
not been resolved.

### 3. Write path and concurrency

Updating a record is currently a git commit. That does not break at scale; it
breaks at **n = 2**.

## Required before any public launch

- **There is no privacy notice.** Nothing under `site/`. Competitors all ship
  one. Turkish data protection law (KVKK) exempts small operators from the
  VERBİS registry, but the *duty to inform* is not covered by that exemption,
  and CV text sent to a model provider is a cross-border transfer. This is the
  only item on this list that can be closed today without running a server.
- **Third-party requests.** The published page fetches fonts and libraries
  from Google Fonts and cdnjs. Job-search data is sensitive, and a visitor's
  IP address reaches those services.
- **Test coverage.** Python regression tests, network-free DOM tests, and CI
  exist. Real model calls, real Gmail, and visual browser tests do not.

## Planned features

### Bilingual interface

The interface ships Turkish only. The plan is a language switch that behaves
exactly like the light/dark theme switch — persisted per visitor, Turkish by
default, English as the second option.

The switch changes interface text. It does not translate the contents of a
record: notes, match rationales, and next steps are stored as written.

### `web-live/` — the web application

A separate Next.js application in its own directory, built in phases:

1. **Application tracking** — status pipeline, rejection reasons, Kanban view.
   *In progress.*
2. **CV / posting matching** — match score and missing-skill list.
3. **Personal training page** — course suggestions per missing skill.
4. **Funnel navigation** — newcomer → activated → engaged → habit.
5. **Measurement** — event tracking and segment transition rates.

## Liveable without, in priority order

These reduce quality. They do not stop the product, and they must not be
placed in front of the blocking items above.

1. Automatic match scoring
2. A real course API
3. A database
4. Multiple profiles per user
5. Streak tracking

## Open questions

- **Automatic extraction of posting text, then skill inference.** Match
  dimensions and `gap_skills` are assigned by hand today. This is the weakest
  link in the project.
- **The match scores of the 68 historical records cannot be verified from
  email.** Tested against a real posting in September 2026: LinkedIn's
  saved-job and job-alert emails never carry the job description, only title,
  company, and location. Two agents working from that thin input scored the
  posting 44 (weak); the hand-assigned record said 90 (strong). The gap is not
  an agent error — the manual score was based on the posting page as seen in a
  browser, which was never in the email. So for most of the 68 records the
  match dimensions cannot be checked retroactively. Only records where the
  posting text was kept are reliable.
- **Cost per user per day is the one number no decision can be made without.**
  Of the seven inputs to the unit-economics model, four are unknown, three are
  external benchmarks, and none is a measurement. The structural fact: cost
  scales with *existence*, not usage — the scan runs every morning whether the
  user opens the app or not. A dormant user is fully expensive here, which
  makes freemium structurally hard.
- **Are the classification rules founder-specific?** `config/rules.yaml`
  lists 16 ATS sender domains. The cheapest experiment: three job seekers run
  the `backfill_queries` searches against their own Gmail and share only the
  sender-domain and subject-line list. Count how many senders fall outside
  those 16. Costs nothing, takes a day, and n = 3 is enough because the
  question is existence, not a ratio. The same finding answers the
  country-scaling question: entering a country is not marketing, it is
  rebuilding `rules.yaml` for that country.
