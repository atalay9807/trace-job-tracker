# Security Policy

## Supported versions

Trace is a single-branch project. Only the current state of `main` is
supported; there are no tagged releases or backports.

| Version | Supported |
|---|---|
| `main` | ✅ |
| Anything else | ❌ |

## Reporting a vulnerability

**Do not open a public issue for a security problem.**

Use GitHub's private vulnerability reporting instead:
[Report a vulnerability](https://github.com/atalay9807/trace-job-tracker/security/advisories/new).
That form is private between you and the maintainer until a fix is published.

Please include:

- what you found and where (file, line, or URL),
- the steps to reproduce it,
- what an attacker gains — data read, data written, code executed,
- anything you already tried that did *not* work, so nobody repeats it.

This is a one-person project. Expect a first reply within about a week, not
within hours. If a report is valid you will be credited in the fix commit
unless you ask otherwise.

## What is in scope

- The generated dashboard (`site/app.html`, `src/dashboard.template.html`) —
  injection, data leakage between records, anything that escapes the page.
- The Python pipeline (`src/`) — path traversal, unsafe file handling, or
  anything that can write outside the selected data directory.
- The web application under `web-live/` — authentication, session handling,
  and Row Level Security gaps.
- CI workflows under `.github/workflows/` — anything that lets a pull request
  run with more privilege than it should.

## What is out of scope

- **The published demo data is synthetic.** `data/` in this repository holds
  an anonymous demo profile. It is not anybody's real job search. Finding
  "personal data" in it is not a vulnerability.
- The published dashboard is a static file with no authentication by design.
  It contains only demo data. This is a documented limitation, not a bug —
  see `ROADMAP.md`.
- Missing security headers on GitHub Pages, which this project does not
  control.
- Reports produced only by an automated scanner, with no demonstrated impact.

## Known limitations

These are documented rather than fixed, and are tracked in `ROADMAP.md`:

- The dashboard embeds all of its data at build time. Anyone with the URL
  sees everything in that file.
- There is no server-side identity. Data isolation between users does not
  exist yet outside `web-live/`.
- The published page requests fonts and libraries from third-party CDNs, so
  a visitor's IP address reaches those services.
