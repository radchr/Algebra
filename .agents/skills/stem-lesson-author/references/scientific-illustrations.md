# Simplified scientific illustrations

Use this reference when a grade-7 lesson needs a simplified scientific illustration, especially an interactive biological cell diagram. It records the research decision made on 2026-09-26 so that later lesson runs do not repeat the same search.

## Default decision

For interactive instructional diagrams, use **D3.js with SVG** by default.

- Keep scientific facts in a reviewed Python or JSON domain model.
- Let D3 render that model as separate SVG elements.
- Keep visible labels as real text, not pixels baked into an image.
- Give clickable or draggable structures stable IDs and separate learner-friendly descriptions.
- Provide keyboard-operable controls and an equivalent HTML text/control layer where needed. SVG makes this easier but does not make accessibility automatic.
- Keep TTS narration separate from labels and formulas. Narration should contain natural Ukrainian sentences rather than raw terminology lists, symbols, or markup.

The renderer is not a source of scientific truth. It must draw only the reviewed domain model. For a cell comparison, explicitly encode which structures are present in each cell type and validate that model separately from the UI.

## Tool choices

### D3.js plus SVG — default for interaction

Use for clickable structures, highlighting, drag-and-drop, comparison views, and state-driven changes. D3 supports DOM events and a drag abstraction across SVG, HTML, and Canvas. Prefer SVG for the small number of meaningful objects in a school diagram.

Official sources:

- [D3 drag](https://d3js.org/d3-drag)
- [D3 event handling](https://d3js.org/d3-selection/events)
- [D3 API](https://d3js.org/api)

### SVG.js — simpler alternative

Use when the diagram is mostly hand-composed shapes and the lesson does not need D3's data binding or richer state transitions. SVG.js provides a concise API for SVG shapes, groups, text, animation, and events. Dragging is supplied by its draggable plugin.

Official sources:

- [SVG.js documentation](https://svgjs.dev/docs/3.0/)
- [SVG.js draggable plugin](https://svgjs.dev/docs/3.0/plugins/svg-draggable-js/)

### Bioicons — optional asset source, not the renderer

Use individual Bioicons SVG assets only when they improve a diagram and their scientific content fits the lesson. Do not assemble the whole lesson mechanically from icons. Each icon may have its own license and attribution requirement; record the author, license, source URL, and any modification for every reused asset. Prefer CC0 or MIT assets when equivalent choices exist.

Official sources:

- [Bioicons library](https://bioicons.com/)
- [Bioicons repository and licensing guidance](https://github.com/duerrsimon/bioicons)

### Matplotlib — static fallback and export

Use Python `matplotlib.patches` and `PathPatch` for static figures, printable diagrams, or deterministic SVG/PNG fallback output. Do not choose Matplotlib as the primary drag-and-drop layer.

Official sources:

- [Matplotlib PathPatch](https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.PathPatch.html)
- [Matplotlib savefig](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html)

### CellPAINT — scientific reference for molecular-scale scenes

CellPAINT builds scientifically informed molecular illustrations from structural evidence. It is useful as a reference when a lesson genuinely operates at molecular scale, but it is too detailed for the default simplified grade-7 cell-identification activity.

Official source:

- [CellPAINT by Scripps Research](https://ccsb.scripps.edu/cellpaint/)

## Findings to preserve

- The search did not identify a mature, reusable Python or JavaScript package that directly provides a scientifically reviewed `draw_bacterium()` or `draw_plant_cell()` API for this lesson.
- Ready-made educational cell websites and downloadable diagrams exist, but they are products or assets rather than dependable embeddable libraries.
- A generic graphics library cannot guarantee biological accuracy. Review the scientific model and each borrowed asset.
- Prefer SVG to Canvas for these small labeled diagrams because each meaningful structure can remain a separate DOM element. If Canvas is required, mirror every learner action with real HTML controls and text.
- Do not add 3D rendering merely for visual effect. Use it only when depth or spatial relationships are part of the learning goal.

## Research record

Exa was used on 2026-09-26. The search covered 47 returned results across seven queries in four areas: ready-made cell tools, JavaScript interaction libraries, Python vector output, and scientific SVG assets. Nine official documentation pages were then checked directly. The sources above are the retained primary references.

Do not repeat this research during ordinary lesson creation. Search again only when at least one of these conditions holds:

- the author requests another rendering technology or a molecular/3D representation;
- a selected library is unavailable or incompatible with the current runtime;
- an asset's license or provenance cannot be verified;
- accessibility requirements cannot be met with the recorded approach;
- the official documentation shows a breaking change relevant to the planned implementation.
