# Digital Geometry Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bring the three active Marimo geometry lessons into conformance with the repository's Cache-First, POEM, exact-verification, and Ukrainian-only contracts.

**Architecture:** Markdown lessons declare their cached source pages. The lesson loader validates those pages through a read-only SQLite readiness API before the Marimo app renders them. `CheckTask` owns the Predict and Mission data, while `app_geometry.py` remains a thin reactive presentation layer.

**Tech Stack:** Python 3.11, Marimo 0.25+, SQLite, SymPy, DrawSVG, JSXGraph, pytest, Ruff.

**Spec:** `AGENTS.md` and `ARCHITECTURE_DIGITAL_GEOMETRY.md`, plus the accepted 2026-10-09 project audit in this chat.

## Global Constraints

- Modify only `app_geometry.py`, `content/geometry/*.md`, `src/geometry_engine/`, `data/geometry/book_kb.db`, active tests, and root-level project documentation.
- Do not modify `docs/`, `book_geometry/`, `src/geometry_pipeline/`, PDF/TeX artifacts, or algebra code.
- Keep all learner-facing copy in Ukrainian.
- Do not mark a cached page verified without reviewing its Ukrainian translation and supplying its missing pedagogical fields.
- Preserve the current dirty worktree and do not overwrite unrelated user changes.

## Review Focus

- A lesson referencing a missing or non-verified source page must fail before rendering.
- A `BookPage` created without an explicit status must not silently become verified.
- Every active lesson must expose a prediction, three ordered hints, and an exact checked mission.
- Changing the selected lesson must select that lesson's prediction/task without duplicate Marimo definitions.
- JSXGraph network failure must produce a clear learner-facing fallback instead of a blank frame.

---

### Task 1: Executable Cache-First contract

**Files:**
- Modify: `src/geometry_engine/db.py`
- Modify: `src/geometry_engine/lesson.py`
- Modify: `tests/test_lessons_and_app.py`

**Interfaces:**
- Produces: `BookDatabase.page_readiness(book_id, page_nums) -> dict[int, str]`
- Produces: `BookDatabase.require_verified_pages(book_id, page_nums) -> None`
- Produces: `Lesson.source_pages: tuple[int, ...]`
- Produces: `load_all_lessons(..., require_verified_cache: bool = True)`

- [x] Write tests for safe default status, page-readiness errors, source-page parsing, and app-facing cache rejection.
- [x] Run focused tests and confirm they fail for the missing contract.
- [x] Implement the minimal database and lesson-loader APIs.
- [x] Run focused and active suites to green.

### Task 2: Verify the triangle cache and reconcile lesson scope

**Files:**
- Modify: `data/geometry/book_kb.db`
- Modify: `content/geometry/00_introduction.md`
- Modify: `content/geometry/01_angles.md`
- Modify: `content/geometry/02_triangles_equality.md`
- Modify: `tests/test_lessons_and_app.py`

**Interfaces:**
- Consumes: Task 1 cache gate and `Lesson.source_pages`.
- Produces: three lessons whose declared source pages are completely verified.

- [x] Add a failing integration test requiring all active lesson pages to be verified and pedagogically populated.
- [x] Review pages 21–28, add missing Feynman/misconception notes, and set only reviewed pages to `verified`.
- [x] Declare source page ranges in all lessons and narrow the triangle lesson to the complete §§30–38 scope.
- [x] Restore missing §§31, 35, and 36 from the verified cache without adding a new chapter.
- [x] Run cache/content tests to green.

### Task 3: POEM and three-level scaffolding

**Files:**
- Modify: `src/geometry_engine/tasks.py`
- Modify: `app_geometry.py`
- Modify: `tests/test_lessons_and_app.py`

**Interfaces:**
- Produces: `CheckTask.prediction_prompt`, `prediction_options`, `prediction_answer`, `prediction_explanation`, and `hints`.
- Produces: a Marimo prediction control that gates interactive lesson widgets and a three-level hint panel for every mission.

- [x] Add failing tests for complete POEM task metadata and headless Marimo definitions.
- [x] Implement Ukrainian prediction data and three progressively explicit hints for each lesson.
- [x] Render Predict before lesson content, gate Observe widgets until a choice is made, and render hints beside Mission.
- [x] Run focused and active suites to green.

### Task 4: Cache/content regression coverage

**Files:**
- Modify: `tests/test_lessons_and_app.py`

**Interfaces:**
- Consumes: Tasks 1–3.
- Produces: regression coverage for section ranges, cached figure links, pedagogical fields, and POEM metadata.

- [x] Add tests that independently assert literal source-page and section coverage for the three active lessons.
- [x] Add tests for valid `figures_json` linkage and no translated page leaking into an active lesson.
- [x] Run active tests to green.

### Task 5: JSXGraph reliability boundary

**Files:**
- Modify: `src/geometry_engine/jsx_templates.py`
- Modify: `tests/test_geometry_engine.py`
- Modify: `README.md`

**Interfaces:**
- Produces: visible CDN-load failure fallback and an effective `initial_angle` parameter.

- [x] Add failing template tests for fallback markup and use of `initial_angle`.
- [x] Implement the minimal fallback and parameter wiring without adding a new frontend build system.
- [x] Document that JSXGraph requires network access while all text, cached SVG, and SymPy missions remain local.
- [x] Run focused and active suites to green.

### Task 6: Root documentation and final verification

**Files:**
- Modify: `README.md`
- Modify: `ARCHITECTURE_DIGITAL_GEOMETRY.md`
- Modify: `pyproject.toml`

**Interfaces:**
- Produces: contributor documentation aligned with the single active Marimo track.

- [x] Replace frozen-track onboarding with the actual Marimo/Markdown/SQLite workflow.
- [x] Remove claims that nonexistent lessons or Marimo Studio views are already implemented; label them as future work if retained.
- [x] Replace the placeholder package description without changing frozen entry points.
- [x] Run the complete active pytest set, Ruff check/format, headless app smoke test, and bounded Marimo static check.
- [x] Inspect `git diff --check`, database readiness, and final worktree status.

## Verification record

- Active pytest suite: 53 passed.
- Ruff check and format check: passed for the active Python scope.
- Headless Marimo run: three lessons loaded; Observe remains locked before Predict.
- Cache audit: pages 9–28 verified; 50 unique lesson figure references resolved.
- `marimo check --strict -q app_geometry.py`: passed outside the Windows sandbox; the sandboxed CLI blocks while creating its internal `asyncio` socketpair.
