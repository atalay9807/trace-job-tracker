# Trace remediation report — 18 September 2026

## Outcome

The code fixes were prepared on the `codex/trace-guvenilirlik-ve-ortak-calisma`
branch. Starting commit: `da59cd42e5eae7eb78889c1bdb9942608abd1d9d`. The work
preserves the existing JSON reporting architecture; it starts no new server,
no paid model call, no Gmail scan, and no scheduled task.

29 Python regression tests and 13 DOM behaviour tests passed. 68 demo records
were validated against the schema and the skills catalog. Four Python entry
points were run against both demo data and empty user data. Three broken YAML
headers were fixed; the headers of nine agents and seven skills now parse.

The GitHub connection became available on 18 September. Changes are delivered
on a separate development branch through a draft pull request. Merging to the
main branch and deploying live are outside the scope of this package. The
current result of the remote verification is followed in the pull request's
Checks section.

## Computation and data fixes

| Problem | Change | Verification |
|---|---|---|
| An empty application list crashed the analyses | Zero denominators and the empty-engagement case are supported | Four commands and six interface pages against empty data |
| Weeks were pinned to August 2026 | ISO week grouping derived from the real date | Year boundary, September, and unknown dates |
| A same-day reply was lost because it was zero days | Reply evidence is bound to a shared definition across both reports | A same-day reply reports as 100% |
| Last contact was being counted as first response time | Optional `first_response`; without it, no measurement | Computed from the first response while last contact differs |
| The median was wrong for an even sample | The two middle values are averaged | 1 and 10 days → 5.5 days; same day → 0 |
| The 12/21-day boundaries differed from the documentation | Boundary days are inclusive | 11, 12, and 21 days of silence |
| Closed records were producing reminders | Closed and rejected records are removed from scoring, focus, and reminders | A closed record with a past deadline |
| Snapshot stages were presented as transition rates | Unprovable sequential conversions were removed | No invented interview conversion on an offer record |
| Future and repeated engagement days were counted | Deduplication and a date window | Future, pre-start, and repeated days |
| An invalid stage silently received a default score | An explicit error through shared schema validation | Unknown stage, malformed date, and malformed id |
| Dimension bounds were not validated | Numeric, ceiling, null, and rationale checks | Boolean, NaN, negative, and above-ceiling values |
| The data path could stay cached within one process | `TRACE_DATA` is resolved on every read | Two profile directories and a missing file |
| Scoring mutated the source records | Derived fields go into new record copies | Source equality after input and output |

The definition of a reply was made deliberately more conservative: a
last-contact change on its own may be an automated acknowledgement. An
evidenced stage or rejection, or an explicit reply record, is what counts —
so the number is a lower bound. Because the current demo data carries no
first-response date, the median is no longer shown. Old numbers changing is
the result of this measurement fix.

## Interface and output safety

- An HTML document skeleton, UTF-8, and a mobile viewport were added.
- Unsupported CV selection is disabled; a missing Claude object no longer
  raises a `ReferenceError`. In a supported environment there are checks for
  sharing consent, permission errors, the model response, and concurrent
  requests. The PDF reader loads only when needed.
- The Gmail button no longer hangs as if a connection were being established;
  it explains this version's limit.
- Missing scores and dates and an empty training list are displayed properly.
  The last-N-days filter excludes future dates and anything outside the
  window. Turkish search was verified.
- The demo banner explains that the profile is a sample, and states the
  reference date.
- The public HTML carries no application or email actions, no contact fields,
  and no recruiter messages. Building `--site` from private data, and
  targeting the wrong destination inside the repository, are both blocked.
- A closing script tag inside the JSON does not become executable HTML; action
  URLs and CSV formula prefixes are validated.
- Modal focus return and Tab trapping were added. Visual and accessibility
  conformance still needs separate verification in a real browser.

## Claude Code / Codex alignment

`docs/collaboration.md` became the shared contract. `AGENTS.md` and
`CLAUDE.md` both point at it. Every task runs on its own branch and working
copy; two agents never write to the same source JSON. This is a session
discipline, not a database lock.

The matcher's contradiction — "write to the record and validate" versus "do
not write to the file" — was removed. `src/eslesme_kontrol.py` validates a
suggestion without writing it to a record. When the posting text is
insufficient, a null result is used; missing data is not counted as a bad
match for the candidate.

In the mail classification reference, rejection is handled before positive
invitation signals, so the positive substring inside "not moving forward" no
longer produces an invitation. Quoted older messages are excluded; generic or
contradictory wording is left as *under review*. This is an instruction and
configuration fix; no claim is made that classification accuracy was measured
against a real inbox.

A colon in the `description` field of two skills and the interview
preparation agent was breaking YAML parsing; those values are now quoted
properly.

## Automated verification and publishing

The new checks workflow runs the Python tests, the demo build, the npm/DOM
tests, and the generated-file checks. The Pages job does not deploy until
those checks pass, and it also watches code, data, and template changes. The
demo output was produced byte-for-byte identically under different Python
hash seeds.

The checks passed in this working environment. The GitHub Actions result is
followed separately in the pull request's Checks section; when a new commit is
pushed, the previous result does not count as success for the new version.

## Verification not completed, and live-product limits

The cloud browser blocked access to the local preview address, so no new
desktop or mobile screenshots were taken; the previous images are labelled as
an archive. DOM tests are neither a real browser nor a visual review. Real
Claude `sample`, Google OAuth, model cost, and multi-user isolation were not
exercised.

Static HTML does not provide a backend that serves personal data safely to
multiple users. Accounts, a database, a write path, the Google connection, the
model provider layer, and event history are all open work.
`docs/production-readiness.md` defines the acceptance conditions. No claim of
"ready for production" is made.

The source demo JSON files in the public repository and the old commit history
were not modified. Removing links from the HTML does not mean that data in an
old commit was deleted. Comprehensive validation of every JSON schema beyond
applications, and a real model evaluation set, are left to later work.
