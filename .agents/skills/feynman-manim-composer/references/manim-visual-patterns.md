# Manim CE Visual Patterns & Pedagogical Implementations
> **Tested recipes for bringing Feynman's physical models to life in Manim CE v0.21**

---

## 1. Typography & Palette Standard

### Ukrainian Typography (Zero Glyphs Glitch)
```python
from manim import *

# Canvas & Background setup
config.background_color = "#0E141E"  # Modern dark slate
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30

FONT_NAME = "Segoe UI"  # Standard system font with flawless Ukrainian kerning

# Safe text creation:
title = Text("Власні вектори та розтягування простору", font=FONT_NAME, font_size=28, weight=BOLD, color=WHITE)
```

### Color Palette (3Blue1Brown High-Contrast Scheme)
* Background: `#0E141E` (Dark Slate Navy)
* Card/Box fills: `#141C2B` (Elevated Panel), opacity 0.9
* Accent Primary: `#00D2FC` (Electric Cyan / Target)
* Accent Secondary: `#FF6B8B` (Coral / Heat / Tension)
* Success / Energy: `#2BD980` (Emerald / Life / Signal)
* Warning / Analogy Boundary: `#FFAA00` / `#FFD93D` (Gold / Alert)
* Deep Structure: `#A36BFF` (Royal Purple / Theory / Geometry)

---

## 2. Dynamic Physical Metaphor Patterns

### Pattern A: Growing Bubbles / Waves with `ValueTracker` & `always_redraw`
```python
# Track the expanding radius
r = ValueTracker(0.2)

# Bubble anchored to a point
bubble = always_redraw(lambda: Circle(
    radius=r.get_value(),
    stroke_color="#00D2FC",
    stroke_width=2,
    fill_color="#00D2FC",
    fill_opacity=0.2
).move_to(dot.get_center()))

self.add(bubble)
self.play(r.animate.set_value(2.5), run_time=3.0, rate_func=linear)
```

### Pattern B: The Rubber Sheet Transformation (Eigenvectors in Action)
```python
plane = NumberPlane(
    x_range=[-4, 4, 1],
    y_range=[-3, 3, 1],
    background_line_style={"stroke_color": "#2A384C", "stroke_width": 1}
)
self.add(plane)

# Vector that will stretch without rotating (Eigenvector along [1, 1])
v_eigen = Arrow(plane.c2p(0, 0), plane.c2p(1, 1), buff=0, color="#2BD980", stroke_width=4)
# Generic vector that will rotate
v_other = Arrow(plane.c2p(0, 0), plane.c2p(0, 1), buff=0, color="#FF6B8B", stroke_width=3)

self.play(Create(v_eigen), Create(v_other))

# Diagonal stretch matrix [[2, 0], [0, 1]] or shear
matrix = [[2, 0.5], [0.5, 2]]
self.play(
    plane.animate.apply_matrix(matrix),
    v_eigen.animate.apply_matrix(matrix),
    v_other.animate.apply_matrix(matrix),
    run_time=3.0
)
```

### Pattern C: Rolling Down an Energy Hill (Activation Energy & Catalysis)
```python
# Landscape function: hill with a barrier and a deep valley
hill = axes.plot(lambda x: 2.0 * np.exp(-x**2) - 0.5 * x, x_range=[-2.5, 2.5], color="#4A5568")

# Ball at the top
x_tracker = ValueTracker(-2.0)
ball = always_redraw(lambda: Dot(
    axes.c2p(x_tracker.get_value(), hill.underlying_function(x_tracker.get_value())),
    radius=0.12,
    color="#FFD93D"
))

self.add(hill, ball)
# Push over the activation barrier!
self.play(x_tracker.animate.set_value(0.0), run_time=1.5, rate_func=ease_in_sine)
self.play(x_tracker.animate.set_value(2.0), run_time=1.2, rate_func=ease_out_quad)
```

---

## 3. Rendering Pipeline Cheatsheet

| Target Output | Command | Use Case |
|---|---|---|
| **Fast Preview** (480p, 15fps) | `python -m manim -ql scene.py SceneName` | Rapid drafting & timing checks |
| **Static 1080p Image** | `python -m manim -s -qh scene.py SceneName` | Markdown infographics & cheatsheets |
| **Full Video (1080p, 30fps)** | `python -m manim -qh --format=mp4 scene.py SceneName` | Final video export |
| **High-Quality GIF** | `ffmpeg -y -i video.mp4 -vf "fps=15,scale=720:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" anim.gif` | Embedded animated guides |
