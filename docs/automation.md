# How the automation works

## The daily routine

This document describes a flow designed for an authorized Claude session or
Routine. Cloning this repository and running the Python commands does not
create a scheduled task, does not scan Gmail, and does not send email. The
current Routine identity and run history are verified from the connected
service; the old session identifier that used to be recorded here has been
removed.

Scheduled at `0 6 * * *` UTC = 09:00 Europe/Istanbul. The data-source and
single-writer rules in `docs/collaboration.md` apply.

Every morning it runs these steps:

1. **Scan** — search Gmail for the last 24 hours of job-related email
   (`config/rules.yaml` → `scan.daily_query`).
2. **Classify** — label each email following the `status_rules` order:
   rejection → offer → interview invitation → action required → under review.
   Only the new text of the last message is evaluated; a contradictory signal
   is left as *under review*. Senders on the `noise_senders` list are counted
   and nothing more.
3. **Update** — refresh `stage`, `status`, `last_contact`, `deadline`, and
   `next_step` on the matching record in the selected
   `TRACE_DATA/applications.json`, and add a record for a new application.
4. **Report** — if sending is separately authorized, send a summary to the
   verified user address. Nothing is sent to the demo address; read permission
   is not permission to send. Subject: `📋 Günlük İş Takip Raporu — <date>`.
5. **Remind** — apply the `reminders` rules to processes whose deadline is
   near or past and to those that have gone quiet.

If nothing critical happened, the email says so plainly and repeats the open
actions. It never stays silent.

## Weekly feedback

On Mondays the report includes a `--weekly` section: four questions are asked,
and the answers feed into `fit` scores on the next scan. This is what makes
the system a loop rather than a one-way notification stream.

## Maintenance

**Adding an application by hand:** the current schema is in
`docs/technical-contract.md` and `src/veri.py`. After writing, validate with
`python3 src/veri.py`. Without the posting text, `match` stays null. If the
date of the first real reply is known, record it as `first_response`; later
messages only move `last_contact` forward.

**Changing the scoring:** `config/rules.yaml` → `scoring` is a reference
document. The real stage weights live in `src/veri.py` and the urgency
thresholds in `src/pipeline.py`. Update both together.

**Editing the Routine:** change the prompt with `update_trigger` — never
delete and recreate it, or the run history is lost.

**Full rebuild:** the four queries in `config/rules.yaml` →
`scan.backfill_queries` re-scan the last 30 days from scratch. Running this
once a month catches applications that were missed.

## Known limits

- LinkedIn "Easy Apply" applications usually generate only a confirmation
  email from the company's ATS; LinkedIn's own record of the application never
  reaches the inbox. So the `applied` date is sometimes the ATS confirmation
  date, 0–2 days after the real application.
- The `fit` score is not computed automatically. It is assigned by hand and
  updated through the weekly feedback.
- The Gmail search relies on English and Turkish keywords; email in another
  language can fall through to noise.
