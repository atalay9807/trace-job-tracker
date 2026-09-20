# Moving to a local machine — terminal and desktop

This project currently runs **in an ephemeral cloud container** (a remote
session opened through claude.ai). The owner intends to move to terminal or
desktop Claude Code before long. This document records what to do on that day,
and what will **not** come across by itself. It is a note, and it gets updated
when the move actually happens.

> This document exists because the owner asked for it: it is the reminder for
> the day of the move. There is no memory between sessions — the only reliable
> place for a reminder is the repository.

---

## Today's constraints, and which ones lift

| Constraint | Today | Locally |
|---|---|---|
| **Egress lock** | Package registries and `github.com` only. `WebFetch` is closed — `huntr.co` and `builtin.com` were tried and returned `EGRESS_BLOCKED` | Open. A competitor's interface can actually be opened and looked at, which closes the biggest gap in the `pazar-arastirmacisi` agent |
| **Ephemeral container** | The disk disappears when the session ends; anything uncommitted is lost | The disk persists. Screenshots, intermediate output, and scratch files stay |
| **The published page cannot be verified** | `github.io` cannot be opened; the Pages output can only be verified by asking the owner | It opens in your own browser, and Playwright can test the real published address |
| **No server-side OAuth** | The Connect page cannot establish a real Gmail connection and shows an error state | Moving locally does not solve this either — OAuth needs a hosted backend. The move does **not** fix it; it is separate work |

## What comes from the repository — nothing to do

The moment you run `claude` inside the repository directory, these load
automatically:

- `CLAUDE.md` — the project instructions
- `.claude/agents/*.md` — nine agents
- `.claude/skills/*/SKILL.md` — seven skills
- `src/`, `data/`, `config/`, `docs/` — all of the code and data

So the agent and skill architecture is **portable**; there is no installation
step, `git clone` is enough.

## What does not come from the repository — install by hand

**1. MCP connectors.** The Gmail, Google Drive, GitHub, and Indeed connectors
live at the account or session level, not in the repository. Each has to be
authorized again locally (`claude mcp add …`, or the connector screen in the
desktop app). Without Gmail authorization the daily scan does not run — that
is the project's input.

**2. Account-level skills.** `CLAUDE.md` refers to `validate_palette.js` in
the `dataviz` skill, but that file is **not** in this repository and is not
synced into this session — it is a personal skill. If contrast measurement is
needed locally, either sync that skill as well or bring the measurement script
into the repository. The second option is sturdier: measurement is a project
rule, not a personal preference.

**3. The daily Routine.** The 09:00 scan lives on the cloud side. It is not
triggered while local Claude Code is closed. There are two options, to be
decided during the move:

- Leave the Routine in the cloud and use the local session only for
  development (simple; today's behaviour is unchanged).
- Move the trigger locally (`cron` or `launchd` → `claude -p "…"`). If the
  machine is off, no report goes out that day; in exchange everything is in
  one place.

The Routine is **never deleted and recreated** — that loses its history.
Changes are made with `update_trigger`.

**4. Playwright.** Chromium comes ready in this container
(`/opt/pw-browsers/chromium-1194/chrome-linux/chrome`). Locally,
`playwright install chromium` is needed once; interface verification after
`build_dashboard.py` depends on it.

## Local requirements

- Python **3.11+** — no external dependency, the standard library is enough
- `git`
- The Claude Code CLI (terminal) or the desktop app
- Node.js — only for Playwright and contrast measurement

```bash
git clone https://github.com/atalay9807/trace-job-tracker.git
cd trace-job-tracker
python3 src/pipeline.py        # first check: does it run
claude
```

## Order of the move

1. Clone the repository and run `python3 src/pipeline.py` — is the data layer
   intact?
2. Open `claude` and confirm that nine agents and seven skills appear in
   `/agents` and the skill list.
3. Authorize the Gmail, Drive, GitHub, and Indeed connectors.
4. Run one daily scan by hand and compare the output with the last report from
   the cloud.
5. Decide about the Routine (cloud or local).
6. Install Playwright and take a screenshot after `build_dashboard.py`.

## What the move does not change

**LinkedIn still cannot be scraped.** This is a legal limit, not a technical
one — the User Agreement forbids it and it is actively enforced. When egress
opens locally, do not conclude "we can do it now"; the only legitimate
LinkedIn data is the user's own inbox, and that stays true after the move.

Likewise, the three measurement limits in `CLAUDE.md` (rejection reasons,
impression data, simulated courses) are about the data, not the environment.
They hold locally exactly as they do here.
