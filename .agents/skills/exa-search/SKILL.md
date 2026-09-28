---
name: web-search-pro
description: "Web Toolkit powered by Exa, Tavily, DuckDuckGo, and Wikipedia. Use this skill when the user needs to search the web or fetch/extract URL content. Covers: semantic web search, academic research, general web search, Wikipedia lookups, and URL extraction. Use Exa for scientific/academic filtering, Tavily for direct AI answers, DuckDuckGo for general free search, and Wikipedia for encyclopedic facts."
compatibility: Requires uv, and optionally EXA_API_KEY and/or TAVILY_API_KEY in .env.
license: MIT
metadata:
  skill-author: CogDelta
  updated_for: Multi-engine support
---

# Web Search Pro (Multi-Engine Toolkit)

A skill for web-powered research tasks backed by multiple engines: **Exa** (scientific/academic), **Tavily** (AI-optimized), **DuckDuckGo** (general/free), and **Wikipedia**.

## Routing — pick the right engine

| Scenario | Tool | Command |
|---|---|---|
| **Scientific / Deep Research** | Exa | `uv run "$SKILL_PATH/scripts/exa_search.py" "query" --category "research paper"` |
| **URL Extraction** | Exa Extract | `uv run "$SKILL_PATH/scripts/exa_extract.py" https://... --text` |
| **General AI Answers** | Tavily | `uv run "$SKILL_PATH/scripts/tavily_search.py" "query" --include-answer` |
| **General Open Search** | DuckDuckGo | `uv run "$SKILL_PATH/scripts/ddg_search.py" "query"` |
| **Encyclopedic Facts** | Wikipedia | `uv run "$SKILL_PATH/scripts/wikipedia_search.py" "query"` |

### Engine Guide

1. **Exa (exa_search.py)**: Best for technical, scientific, or conceptual queries. Use `--category "research paper"` and `--include-domains` to bias towards academic sources. (Requires `EXA_API_KEY`).
2. **Tavily (tavily_search.py)**: Best for fast, AI-optimized summaries and general facts. Use `--include-answer` to get a pre-synthesized answer alongside results. (Requires `TAVILY_API_KEY`).
3. **DuckDuckGo (ddg_search.py)**: Free, unbounded search. Good fallback if API keys are missing.
4. **Wikipedia (wikipedia_search.py)**: Best for entity lookups. Actions: `summary`, `search`, `page`.

---

## Setup & Authentication

The scripts use inline PEP 723 metadata, so just run them with `uv run`. 
API keys (`EXA_API_KEY`, `TAVILY_API_KEY`) are automatically loaded from `.env` in the current working directory via `python-dotenv`.

You don't need `dotenv run` or manual setup — just ensure `.env` has the keys:

```bash
uv run "$SKILL_PATH/scripts/tavily_search.py" "latest AI news" --include-answer
```

---

## Files in this skill

- `SKILL.md` — this file (routing and setup)
- `scripts/exa_search.py` — Exa web search (academic/scientific)
- `scripts/exa_extract.py` — Exa URL extractor
- `scripts/tavily_search.py` — Tavily AI search
- `scripts/ddg_search.py` — Free DuckDuckGo search
- `scripts/wikipedia_search.py` — Wikipedia API search
- `references/web-search.md` — (Legacy) Exa search detailed reference
- `references/web-extract.md` — (Legacy) Exa extract reference
