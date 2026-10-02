# Getting Trace ready to be a live product

As of 17 September 2026, what works is the Python core that produces reports
from stored data, plus the static demo. This document does not describe
finished integrations. It defines the work still to be done for a live
product, and the acceptance condition for each piece.

## Development tools versus the running product

Claude Code and Codex can both develop in this repository. Neither coding
session has to run on the application server. If at some point both Claude and
OpenAI models are wanted *inside* the product, that is a separate server
integration: provider selection, key management, timeouts, retries, budget,
and data sharing all have to be implemented. This remediation package starts
no model call and no paid service; the existing Python computations are
deterministic.

## Development work, in order

| # | Work | Acceptance condition |
|---|---|---|
| 1 | Accounts, data isolation, persistent storage | Two test users cannot read or modify each other's records; a concurrent update is not lost |
| 2 | Manual entry of applications and posting text | A user can save, edit, and delete without Gmail; the empty state works |
| 3 | Server-side AI provider layer | Keys never reach the browser; an off-schema response is never written; timeouts and failures are visible; cost is measured |
| 4 | Posting/profile evidence and an evaluation set | Source text, profile and rubric version, and uncertainty are stored; accuracy is measured on sample scenarios |
| 5 | Google authorization and background scanning | A user connects and disconnects their own account; tokens are stored securely; a duplicate message does not create a duplicate record |
| 6 | Event history and report delivery | First-response and stage dates are stored separately; a re-run job does not send the same message twice |
| 7 | Deletion, backup, monitoring, and privacy disclosures | Deletion and restore are exercised; CVs and tokens never reach the logs; the real data flow is explained to the user |

Google's permission and verification requirements, and the rules on data
transfer, must be verified against current official sources at the time the
integration is chosen. The price and legal assumptions in earlier notes are
not verified inputs to this plan.

## Verification before release

Beyond the Python and DOM tests, a real browser has to exercise the desktop
and mobile flows, keyboard use, real model error states, isolation between
accounts, and disconnecting the Google account. Until those are done, nobody
says "ready for production". Publishing a static demo is not the same as
publishing a product that accepts personal data.

## What is currently unknown

Model cost per user, whether a second user succeeds, how reliable the scores
are without the source posting, and the accuracy of email classification have
all gone unmeasured. A large number of agent definitions is not a substitute
for those measurements. The first step is a small evaluation set that makes
the errors of the model and the rules visible.
