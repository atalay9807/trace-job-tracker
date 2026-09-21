# The README showcase — sources and maintenance notes

## Scope

The work of 20 September 2026 started from commit
`9ca7c333ee2426e7e57c73cecf13edeac6277fc2` on the branch
`codex/readme-gorsel-tanitim`. The goal is for a GitHub visitor to understand
the product quickly and reach the demo easily.

The top section carries the app and site links, a short product message, and
real demo screens. The AI development approach appears after the gallery;
technical headings sit below it in collapsible sections. Application code,
data, publishing workflows, and `web-live/` were not in the scope of that
change.

## Where the images come from

The five JPEGs were captured from the
[published demo](https://atalay9807.github.io/trace-job-tracker/app.html) on
20 September 2026, in a 1341 × 921 pixel browser view. They are real
screenshots, not interface mockups, and their content was not retouched
afterwards. At the time the demo showed 109 records and a data date of
19 September 2026; the capture date and the data date are not the same thing.

| File (under `docs/img/readme/`) | Demo path |
|---|---|
| `ana-2026-09-20.jpg` | `app.html#/ana` |
| `basvurular-2026-09-20.jpg` | `app.html#/basvurular` |
| `eslesme-2026-09-20.jpg` | `app.html#/basvurular/kavza-project-cfo-office-executive` |
| `raporlar-2026-09-20.jpg` | `app.html#/raporlar` |
| `egitim-2026-09-20.jpg` | `app.html#/egitim` |

`trace-cover.svg`, `open-app.svg` and `open-site.svg` are vector assets made
for this showcase. Their text and shapes live in the repository; they use no
external image service, no script, no embedded personal data and no remote font
source. Every image in the README has meaningful alternative text, and every
screenshot links to the matching demo screen. The older `docs/img/` images were
kept because other pages may still use them.

**Their text is English.** The repository's documentation is English while the
product interface is Turkish, so the buttons and the cover were translated and
re-measured: with the interface rendered in a browser, every text box was
checked against its `viewBox`, and none overflows or collides with the arrow
glyphs.

## Verification and updating

On that branch 29 Python tests and 25 DOM tests passed. Data validation
accepted 109 records, and building the site from source did not modify the
tracked application files. The README's 45 link references (including repeats),
eight images and five collapsible sections were checked. The SVGs were parsed
as XML and rendered to PNG for visual inspection. The lowest measured
text-on-background contrast was **7.05:1**. That ratio belongs to the new SVG
assets; it is not an accessibility audit of the whole application.

- Check every relative file link, the eight images and the in-page anchors.
- Verify that the SVG files parse as XML, that the text fits, and that the
  text-on-background contrast holds. Check fixed-color images against both
  GitHub's light and dark themes; never add style or JavaScript inside the
  README.
- Review the README as GitHub renders it on the branch: the two main links
  should appear before the gallery, and the cards and the collapsible technical
  sections should open cleanly.
- When refreshing the screens, open the real demo and visually confirm that
  navigation and panel animation have finished. Never save the same screen
  under two different names.
- Write the new capture date into the file names and into the README note.
  Never change the demo data's own date or present it as more recent than it
  is.
- The change adds no behaviour, so no new application test is required; record
  the result of the existing GitHub Actions checks in the pull request
  handover.

## Handover to Claude

This work is delivered on its own branch and pull request. Under `AGENTS.md`
and the collaboration contract, merging to the main branch requires the user's
authorization; integration is coordinated under Claude's technical lead.

During the link check, the overview site's `trace.html` page was confirmed to
open. However, the page still describes **68 applications** and a window of
**1 August – 1 September 2026**, while the current application shows **109
records** and the date 19 September 2026. That inconsistency predates the
README work. The overview site's numbers and its statements about the scheduled
Gmail flow should be reviewed in a separate site-content pass, together with
the current demo versus private automation distinction. Variable application
counts were not used as a sales claim in the README showcase.

Once `web-live/` is implemented, refresh the feature status table against the
real release. Never present planned account, CV and AI features as finished.
