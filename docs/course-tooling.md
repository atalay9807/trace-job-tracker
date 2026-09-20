# Classifying the tools shown in the course

Source: `docs/source-claude-code-course.md` (a transcript of the YouTube
course that was watched). The owner asked for "a sweep and classification of
the applications shown in the video" — this document is the answer.

**A warning about the counts:** the transcript is machine-generated speech
recognition and names are spelled phonetically: `Epify`→Apify, `Kanva`→Canva,
`Supase`→Supabase, `Anti Gravity`→Antigravity, `N8`→n8n. The mention counts
below are the totals of those variants. They are **not a ranking of
importance** — only of how much the course talked about each one.

---

## By role

### 1. Automation and orchestration

| Tool | Mentions | What it is for in the course | Equivalent in Trace |
|---|---|---|---|
| **n8n** | ~80 | The course's second axis. 9,500 ready-made automation templates, a visual flow builder. Also connects to Claude Code as a connector | **Absent, and not needed.** The course itself builds one of its examples without n8n, saying "I don't want n8n, let's set this up for Claude". Our orchestration is the Routine plus `pipeline.py`; for rule-driven work n8n is one layer too many |
| **Routine** (Claude) | — | Introduced in the course as "a routine works like an n8n automation" | **In use** — the daily 09:00 scan |

### 2. Data collection

| Tool | Mentions | What it is for in the course | Equivalent in Trace |
|---|---|---|---|
| **Apify** | ~48 | Connected as an MCP connector; used to pull Instagram data and as a source in the lead-generation system | **Not used — cannot be used.** The only external data we need is LinkedIn posting text, and that cannot be scraped (User Agreement). Pointing Apify at LinkedIn would make it our problem, not the tool's |
| **Indeed MCP** | — | Not in the course | **In use** — the official search API, backing the posting-existence check in the `rol-onerici-gecmis` agent |

### 3. Development environment

| Tool | Mentions | What it is for in the course | Equivalent in Trace |
|---|---|---|---|
| **Claude Code** | — | The main axis of the course | **This project already is that** |
| **Antigravity** | ~16 | Shown as a downloadable alternative IDE | **Not needed.** Our agent and skill architecture lives in the repository, not in an IDE. It makes no difference to the move either (`docs/local-setup.md`) |

### 4. Connectors (MCP)

| Tool | Mentions | Equivalent in Trace |
|---|---|---|
| **Gmail** | ~34 | **In use — the project's only input.** The one critical tool that overlaps with the course |
| **Google Drive** | 3 | **In use** — reading the CV |
| **GitHub** | 2 | **In use** — repository, Actions, Pages |
| **Slack** | 5 | Not needed. This is a single-user tool; the notification channel is email |
| **Telegram** | 1 | Not needed — same reason |
| **Figma / Canva** | 1 / 1 | Not needed. The interface is a single HTML file and the design system is written down in `docs/technical-contract.md` |
| **Supabase** | 1 | **Tied to an open item.** If the "persistent database and session management" item in `CLAUDE.md` happens, this is the first place to look — today the data layer is `data/*.json` |
| **Shopify** | 6 | Irrelevant — e-commerce |
| **Stripe** | 5 | **Irrelevant today, required if this becomes a product.** It does two jobs in the course: payment infrastructure and proof of revenue ("earnings were checked one-to-one against Stripe"). The second is a note for us too: a revenue claim can only be verified from the payment system |

### 5. The sales stack (the course author's own business)

Apollo, Clay, Lemlist, Gong, HubSpot, and **Instantly** (for high-volume mail
sending; "there's no problem when you send 30–40 mails").

**All irrelevant.** These belong to the course author's agency business; Trace
is not a sales tool. Instantly's bulk-sending logic is the opposite of our
single-user follow-up mail.

### 6. Other

| Tool | Mentions | Note |
|---|---|---|
| **Excalidraw** | 6 | The diagramming skill the course author calls "the skill I use most". We have no equivalent; `docs/technical-contract.md` is currently text. If an architecture diagram is ever needed, this is one of the candidates |
| **Nano Banana / Veo 3** | — | Image and video generation. Irrelevant |

---

## Summary

**Three things from the course actually touch us:** the Gmail connector
(already here), the Routine idea (already here), and the agent/skill
architecture (already built). The rest either belongs to the author's own
agency business (the sales stack, Shopify, Apify) or is an alternative to a
layer we already have (n8n, Antigravity).

**Two names that may matter later:** Supabase (the persistent database open
item) and Stripe (productization). Neither is needed today; adding either now
would sit there as the answer to a problem nobody has solved yet.

**The number of tools in a course and the power of a system are not the same
thing.** The course demonstrates a 20-agent setup; we stopped at nine, and the
reason is written in `CLAUDE.md`: rule-driven work is done in code, without
agents and more cheaply, and an agent is used only where judgement is
required. The same measure applies to tools.
