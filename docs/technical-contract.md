# The Trace technical contract

## What runs

The Python core reads JSON and produces output. It never calls Gmail or a
model. Posting interpretation, profile extraction, and mail scanning are a
separate authorized-session workflow. `src/dashboard.template.html` is the
six-page interface. `reports/pano.html` and `site/app.html` are generated and
never edited by hand.

## Data source and schema

`src/veri.py` resolves the environment variable on every read. Without
`TRACE_DATA`, the repository's own `data/` directory is used; when the
variable is set but a file is missing, the code does **not** fall back to demo
data. The dashboard expects `applications.json`, `profile.json`,
`skills_catalog.json`, `journey.json`, `engagement.json`, `saved_jobs.json`,
and `role_targets.json`. Only the reporting and match commands can work with
fewer files.

Required fields on an application: `id`, `company`, `role`, `channel`,
`applied`, `last_contact`, `stage`, `status`, `track`, `fit`, `deadline`,
`next_step`, `notes`, `match`, `gap_skills`, `links_actions`. The identifier
is unique and made of lowercase ASCII letters, digits, hyphens, and
underscores. Company and role are non-empty text. An unrecognized stage,
status, or channel is rejected; no default stage score is granted.

`match`, `fit`, dates, and description fields may be null when unknown.
`gap_skills` and `links_actions` must be lists, with `[]` when there is
nothing to record. If a `match` object exists, four numeric dimensions, a
zero-or-negative location adjustment, and a rationale are all required. A
negative dimension, a value above its ceiling, a boolean, NaN, or infinity is
rejected. Catalog references are checked by `python3 src/veri.py` and during
analysis and dashboard builds.

| Optional field | Meaning |
|---|---|
| `first_response` | `YYYY-MM-DD` date of the first real reply that is not an automated application acknowledgement; null when unknown |
| `response_received` | true when there is evidence of a reply; false when only an automated acknowledgement exists; null or absent when unknown |
| `contact`, `location` | Contact and location details; the public demo contains no real person's details |

The first response cannot be before the application or after the last contact.
`response_received: false` alongside a first response, a later stage, or a
rejection is a contradiction. Old schema v1 records are readable without the
two newer fields; no date is invented retroactively.

`profile.json: null` and empty application and engagement lists are supported.
The other files must contain the expected dictionaries and lists. Validation
of the full user data model will be extended before the product goes live.

## Urgency and closure

```
urgency = stage_weight + (fit × 4) + deadline_urgency − silence_penalty
```

The ceiling is 160: offer 100 + fit 20 + past deadline 40. An unknown fit adds
nothing. Stage weights live in `src/veri.py`, the remaining thresholds in
`src/pipeline.py`. `config/rules.yaml` is not runtime configuration; it is a
reference.

Deadline: past +40; today or tomorrow +35; 2–3 days +25; 4–7 days +15; 8–14
days +8. Silence: −8 at 12 days **inclusive**, −20 at 21 days **inclusive**.
Follow-up days are calendar days. The critical band is ≥ 100, or *action
required* with a deadline ≤ 3 days or unknown; high is ≥ 75, normal is ≥ 45,
everything else is low. `stage: closed` or `status: rejected` means closed:
score zero, band *archive*, no reminders and no focus list. Long silence alone
never closes a record; it suggests a check-in. The source JSON is never
modified during computation.

## Match scoring and the agent check

```
match = role_family(0–35) + seniority(0–25) + skills(0–25) + domain(0–15) + location(≤0)
```

The total is clamped to 0–100; dimension errors are not silently trimmed away.
Segments: strong ≥ 78, good ≥ 62, medium ≥ 45, weak < 45. A missing match is
null. Scores are not probabilities of success. The rubric carries the context
of the demo profile; for a new candidate it must be applied against that
person's profile and posting evidence, and the demo seniority must not be
treated as universal.

`python3 src/eslesme_kontrol.py < suggestion.json` validates the total, the
segment, and catalog consistency without writing to a file. Judging the
quality of a posting interpretation needs the source text, the profile
version, and an independent assessment; this CLI does not measure that.

## What the analyses mean

- **Reply count:** `first_response` or an explicit reply marker; for older
  records, evidence of a later stage or a rejection is used. A last-contact
  date moving forward on its own can also be an automated acknowledgement. The
  number shown is an evidenced lower bound.
- **Response time:** only `first_response − applied`; same day counts as zero
  days. With an even number of measurements, the two middle values are
  averaged. With no measurements the median is null; it is never filled in
  from the last contact.
- **Stage distribution:** a snapshot. Which stages a closed record passed
  through earlier is unknown. Only the application → evidenced reply rate is
  shown; other sequential conversions and the impression → application rate
  are not.
- **Weekly trend:** ISO weeks starting on Monday, derived from the dates. A
  record with an unknown application date does not appear in the trend. The
  progress and rejection counts are the current state of the people who
  applied that week, not the number of events that happened that week.
- **Engagement:** distinct report days between the start date and the
  reference day are counted. Future days do not count toward the last 7 days
  or the streak; coverage never exceeds 100%. An empty list produces complete
  output with zero values. Sending a report does not prove the app was opened.
- **Gaps:** inferred from the stored assessment. They are not the employer's
  stated reason for rejection. Priority = appearances in rejections × 3 +
  appearances in open processes + level difference × 2.
- **Saved postings:** the closed flag is the last known state. Its absence is
  not confirmation that the posting is still open today.

## Dashboard and output limits

`python3 src/build_dashboard.py --site` builds `site/app.html` from the public
repository's labelled demo data only. The date is fixed through
`meta.last_scan`. A private `TRACE_DATA` or a private dashboard is rejected as
a site or data target. The public payload does not carry contact fields,
application and email action links, or recruiter messages. This check is not
an anonymization service: the data and the git diff must also be reviewed by
hand, and information in old commits is not removed retroactively.

`<`, `>`, `&`, and line separators inside the JSON are embedded safely into
the HTML; text containing `</script>` cannot open a new script. Action URL
protocols are restricted, and external links use `noopener noreferrer`. In
CSV output, external text is prevented from being evaluated as a formula.

The personal dashboard carries all of the data in HTML. It provides no access
control and is never served publicly. `--out` can write to a chosen private
location; that output is never added to the public repository. The HTML is
moved atomically from a temporary file, which only prevents a half-written
output — it is not a multi-user update lock.

CV selection is disabled in the web demo. In a supported Claude environment
there is a sharing confirmation, a size and type check, permission-error
handling, a model-response check, and a single-active-request guard. The
result stays on screen and is not stored. The real provider integration is
mocked in the DOM tests; that does not count as a real model test.

## The application list and CSV

`basvurulariSec()` is the shared selection behind both the table and the
browser CSV export. Urgency, match, open/closed process, date, and Turkish
search conditions are applied together. The selection builds a new array; the
order of the source `D.applications` is never changed.

Urgency sorting uses the band first and the score within a band: a record the
core counts as critical because action is required does not drop down the list
merely because its score is low. Match sorts in both directions; applications
sort newest first, deadlines nearest first, and companies in Turkish
alphabetical order. In urgency and deadline sorting, open processes come first
and unknown values stay at the end of their own group. Ties are broken by
company and id. A `null` match score is filtered separately from a score of
zero.

The browser CSV uses a UTF-8 BOM, a comma separator, and CRLF line endings.
Cells are quoted and inner quotes escaped; formula prefixes in external text
are neutralized with a single-quote prefix. A numeric zero is preserved and an
unknown value is left empty. Contact details, notes, and action URLs are not
exported; the CSV carries summary columns only. The file is created in the
browser with a `Blob` and the temporary address is revoked after the download;
this operation sends no data to a server. The browser download behaviour is
mocked in a DOM test; a real Excel and a real browser download still need
separate verification.

## Maintenance

`docs/collaboration.md` defines the verification commands and the handover
between tools. GitHub Actions runs the Python and DOM checks. Pages builds the
site from source; it does not depend only on changes under `site/`. This
prevents publishing stale HTML after code or data changed.

The source of truth for typography and color values is the template's CSS.
Without a visual test, contrast and mobile behaviour do not count as verified.
`docs/img` and `site/img` were regenerated from the current template with
headless Chromium on 2026-09-20; because Google Fonts is blocked by the egress
policy, the typography appears in a fallback typeface.
