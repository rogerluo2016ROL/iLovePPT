# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**This is a navigation file** — high-level architecture + invariants live here; substantive protocol / handoff / gate rules are in linked specs.

## What this repository is

iLovePPT is a **Claude Code skill library** — not a standalone application. The deliverable is the `skills/` directory: three skills (`pptx-deck`, `pptx`, `diagram`), each consisting of a `SKILL.md` entry doc, child `.md` docs, and Python helper modules. When installed into a project's `.claude/skills/`, Claude reads these docs at runtime to generate PowerPoint decks end-to-end.

The repo is consumed two ways: (1) as a skill library other projects link into `.claude/skills/`; (2) directly via `python3 skills/pptx-deck/build.py deck_plan.json`.

## Commands

```bash
# Run all tests (42 tests; pythonpath auto-configured via pyproject.toml)
python3 -m pytest tests/ -v

# Run a single test
python3 -m pytest tests/pptx/test_helpers.py::test_set_font_writes_ea_typeface -v

# Check external dependencies (python-pptx, soffice, pdftoppm, fonts)
bash skills/pptx/scripts/check_deps.sh

# End-to-end: build a deck from a deck_plan.json
python3 skills/pptx-deck/build.py deck_plan.json
# Optional: skip PNG rendering
python3 skills/pptx-deck/build.py deck_plan.json --no-render

# Smoke tests (exercise the helper + render pipeline)
python3 skills/pptx/examples/minimal_deck.py     # → /tmp/iloveppt_minimal.pptx
bash skills/diagram/examples/render.sh           # → skills/diagram/examples/minimal.png

# Render a .pptx for visual inspection
soffice --headless --convert-to pdf <file>.pptx --outdir /tmp/
pdftoppm -jpeg -r 120 /tmp/<file>.pdf /tmp/slide
```

No build step and no linter are configured.

## Architecture

### Agent pipeline (5 agents + 1 bypass)

`.claude/agents/` holds the runtime pipeline:

| agent | role |
|---|---|
| `iloveppt-brainstorm` | Stage A-B: collect brief + assets via dialog |
| `iloveppt-author` | Stage C-D: produce outline.md + content.md |
| `iloveppt-critic` | Partner-style critic: 14-check baseline + 4-dimension judgmental review (论据强度/节奏/措辞/平衡), runs at Stage C (after outline approval) and Stage D (after content approval) |
| `iloveppt` (builder) | Stage E: build .pptx + visual QA loop |
| `iloveppt-audience` | Simulated audience review (9-point gate) |
| `iloveppt-template-extractor` | Bypass: ingest .pptx template tokens |

👉 **Runtime pipeline protocol (dispatch sequence, handoffs, gates, exit conditions)** — AI-readable, lives in `.claude/`: [`.claude/pipeline-protocol.md`](.claude/pipeline-protocol.md)

👉 **Agent design rationale (human-readable, why we have N agents)**: [`docs/superpowers/specs/2026-05-23-iloveppt-agent-design.md`](docs/superpowers/specs/2026-05-23-iloveppt-agent-design.md)

👉 **Markdown-first design (brief.md / outline.md / content.md schemas)**: [`docs/superpowers/specs/2026-05-23-iloveppt-v3-markdown-first.md`](docs/superpowers/specs/2026-05-23-iloveppt-v3-markdown-first.md)

### Main thread dispatch rule (one-line summary)

When user signals "做 PPT" intent → main thread **must** `TeamCreate` and dispatch to agents (don't write brief / content / do visual QA yourself). When modifying repo code (helpers.py / themes / build.py / tests) → main thread does it directly (cross-file consistency).

Full table + reasoning: see [pipeline protocol §12](.claude/pipeline-protocol.md#12-主线程派发表v050-引入v051-扩展).

### Three-skill layering

```
pptx-deck  ── orchestrator: brief.yaml → complete .pptx
   ├── calls → pptx     (helpers.py, office scripts, render pipeline)
   └── calls → diagram  (draw.io / mermaid / matplotlib → PNG)
pptx       ── low-level .pptx read/write; also usable standalone
diagram    ── diagram generation; also usable standalone
```

### build.py is a mechanical builder; the smart steps are Claude-driven documented processes

The most important thing to understand: `build.py` is an **honest mechanical builder** — it takes `deck_plan.json` and produces a `.pptx` + PNGs. It contains no placeholder functions and no LLM calls.

- **The seam is `deck_plan.json`**: `{theme, output, slides: [{layout, ...fields}]}`. Claude produces it; `build.py` consumes it.
- **Content expansion** (brief → full per-page `deck_plan.json`) is a Claude-executed process documented in `content-writing.md` — not a Python function.
- **Visual QA** (read rendered PNG → score against 17-point checklist → edit `deck_plan.json` → rerun `build.py`) is a Claude-executed process documented in `visual-qa.md` — not a Python function.

When improving generation *quality*, edit the prompt docs (`content-writing.md`, `visual-qa.md`), not `build.py`.

### SSOT standard — helpers.py is the single source of truth

`skills/pptx/helpers.py` is the authoritative definition for two things; nothing downstream may redefine them, only reference or extend:

1. **Low-level pptx operations** — every font/shape/table primitive (`set_font`, `_fix_ph_font`, `card`, `bullets`, `table_modern`, `section_header`, etc.). Theme modules build their `make_*` layout functions on top of these; never duplicate font/shape logic into a theme.
2. **Design tokens** — fonts (`FONT_CN`, `FONT_NUM`), brand colors (`BRAND_PRIMARY`, `BRAND_DARK`, `BRAND_TINT`, `ACCENT`), grays, and slide dimensions (`SLIDE_W`, `SLIDE_H`). `tech_blue.py` does **not** redefine these — it aliases them (`PRIMARY = H.BRAND_PRIMARY`, `FONT_HEADER = H.FONT_CN`). `build.py` uses `H.SLIDE_W/H` rather than hardcoded `Inches(...)`.

`skills/pptx/layout.py` provides **geometry primitives** (`Box`, `content_region`, `full_region`, `columns`, `rows`, `stack`, `split`, `inset`) that are theme-agnostic and sit beside `helpers.py`. Theme `make_*` functions use these to compute element positions without duplicating geometry math.

Consequences for changes:
- Changing a color or font = editing `helpers.py` in **one** place; it propagates to the theme and every helper default.
- Markdown docs cannot import, so hex values in `design-system.md` / `diagram/*.md` are **labelled copies** — they cite `helpers.py` as authoritative and must be re-synced by hand if the palette changes.
- A genuinely different theme (e.g. a future `party_red.py`) may define its own palette — that is a new SSOT scope, not a duplication. The rule forbids re-stating the *same* value, not having distinct themes.

### Skill docs are the product

The `SKILL.md` + child `.md` files are not auxiliary documentation — they are what Claude reads at runtime to know how to generate decks. Editing them changes product behavior. They cross-reference each other with `[[skill-name]]` syntax.

`skills/pptx/scripts/office/` is vendored verbatim from Anthropic's pptx skill — do not modify it.

## Core principle — 一图胜千文 (a picture beats a thousand words)

Content that expresses structure, flow, relationships, or data comparison should become a **diagram**, not a wall of bullet text. When generating or reviewing a deck, actively use AI drawing capability (the `diagram` skill) for such content; when in doubt, draw it. This principle is enforced operationally by the diagram-planning step (workflow Step 3, a Claude-executed process) documented in `skills/pptx-deck/diagram-planning.md`. Any change to generation behavior should preserve this bias toward visuals.

Structural diagrams (flowcharts, architecture, matrices, decision trees, relationship maps) default to **draw.io** — precise color, controllable layout, cross-diagram visual consistency. Mermaid is only a quick-sketch fallback; matplotlib handles data charts. See `skills/diagram/SKILL.md` for the tool-selection table.

## Critical invariants

- **Chinese fonts must be written via lxml `<a:ea>` + `<a:cs>`** (`helpers.py:set_font`). python-pptx's default `font.name` only writes `<a:latin>`, so Chinese text falls back to an ugly font cross-platform. This is the #1 source of broken output.
- **Default font is Microsoft YaHei** (a deliberate project decision). `PingFang SC` / `Heiti SC` appear only in the fallback chain, never as a default. macOS needs Microsoft YaHei installed for LibreOffice rendering to match Windows PowerPoint.
- **Placeholder fonts need `_fix_ph_font`, not `set_font`.** Placeholders inherit `<a:ea>` from the slide master; run-level `set_font` cannot reach that layer.
- **Tests verify structure, not visuals.** They check shape counts and font attributes — a layout can render visually broken and still pass. After any layout/helper change, render to PNG and inspect.

## Conventions

- Commit messages use conventional commits with a scope: `feat(pptx-deck):`, `fix(pptx):`, `docs(diagram):`, `refactor:`, `test(pptx):`, `chore:`.
- `pyproject.toml` sets `pythonpath = ["skills/pptx", "skills/pptx-deck"]`, so tests import `helpers` / `layout` / `themes.tech_blue` / `build` directly with no `sys.path` hacks. Non-test modules keep an idempotent `sys.path.insert` for direct script execution.
- Design specs live in `docs/superpowers/specs/`, implementation plans in `docs/superpowers/plans/`. The pipeline protocol spec (link above) is the authority for agent dispatch / handoff behavior.
