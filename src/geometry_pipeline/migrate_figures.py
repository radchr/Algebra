"""Extract the reviewed TikZ pilot figures and create the seven introduction figures."""

from __future__ import annotations

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MANUAL_SECTION = PROJECT_ROOT / "book_geometry/sections/section_01_angles.tex"
OUTPUT_DIR = PROJECT_ROOT / "book_geometry/figures"

ANGLE_FIGURE_GROUPS: list[tuple[int, ...]] = [
    (8,),
    (9,),
    (10,),
    (11,),
    (12,),
    (13,),
    (14, 15),
    (16,),
    (17,),
    (18,),
    (19,),
    (20,),
    (21,),
    (22,),
    (23,),
    (24,),
    (25,),
    (26,),
    (27,),
]

INTRO_FIGURES = {
    1: r"""\begin{tikzpicture}[scale=1.0,>=Stealth]
  \draw[dashed] (-3.4,0) -- (-2.7,0);
  \draw[<->,very thick,color=primaryblue] (-2.7,0) -- (2.7,0);
  \draw[dashed] (2.7,0) -- (3.4,0);
  \fill (-1.6,0) circle (1.8pt) node[above] {$A$};
  \fill (1.7,0) circle (1.8pt) node[above] {$B$};
  \node[below] at (0,0) {$a$};
\end{tikzpicture}""",
    2: r"""\begin{tikzpicture}[scale=1.0]
  \draw[very thick,color=primaryblue] (-2.2,0) -- (2.2,0);
  \fill (-2.2,0) circle (2pt) node[above] {$C$};
  \fill (2.2,0) circle (2pt) node[above] {$D$};
\end{tikzpicture}""",
    3: r"""\begin{tikzpicture}[scale=1.0,>=Stealth]
  \fill (-2.2,0) circle (2pt) node[above] {$A$};
  \draw[->,very thick,color=primaryblue] (-2.2,0) -- (2.8,0);
\end{tikzpicture}""",
    4: r"""\begin{tikzpicture}[scale=0.95]
  \draw[very thick,color=primaryblue] (-3.2,0.5) -- (-0.4,0.5);
  \fill (-3.2,0.5) circle (2pt) node[above] {$A$};
  \fill (-0.4,0.5) circle (2pt) node[above] {$B$};
  \draw[very thick,color=feynmangreen] (0.6,0.5) -- (3.4,0.5);
  \fill (0.6,0.5) circle (2pt) node[above] {$C$};
  \fill (3.4,0.5) circle (2pt) node[above] {$D$};
  \draw[dashed] (-3.2,-0.35) -- (-0.4,-0.35);
  \draw[dashed] (0.6,-0.35) -- (3.4,-0.35);
  \node at (0.1,-0.35) {$AB=CD$};
\end{tikzpicture}""",
    5: r"""\begin{tikzpicture}[scale=0.9]
  \draw[very thick] (-4,1.2) -- (-2.2,1.2) node[midway,above] {$AB$};
  \draw[very thick] (-1.4,1.2) -- (0.2,1.2) node[midway,above] {$CD$};
  \draw[very thick] (1.0,1.2) -- (2.4,1.2) node[midway,above] {$EF$};
  \draw[very thick,color=primaryblue] (-4,-0.2) -- (2.4,-0.2);
  \foreach \x/\name in {-4/M,-2.2/N,-0.6/P,0.8/Q} {
    \fill (\x,-0.2) circle (2pt) node[below] {$\name$};
  }
  \node[above] at (-3.1,-0.2) {$AB$};
  \node[above] at (-1.4,-0.2) {$CD$};
  \node[above] at (0.1,-0.2) {$EF$};
\end{tikzpicture}""",
    6: r"""\begin{tikzpicture}[scale=1.0]
  \coordinate (O) at (0,0);
  \draw[thick] (O) circle (2.2);
  \coordinate (A) at (0:2.2);
  \coordinate (B) at (48:2.2);
  \coordinate (C) at (90:2.2);
  \coordinate (D) at (180:2.2);
  \coordinate (E) at (235:2.2);
  \coordinate (F) at (340:2.2);
  \fill[feynmangreen,opacity=.16] (O) -- (A) arc (0:48:2.2) -- cycle;
  \fill[mediapurple,opacity=.14] (E) arc (235:340:2.2) -- cycle;
  \draw[thick] (D) -- (A);
  \draw[thick] (O) -- (B);
  \draw[thick] (O) -- (C);
  \draw[thick] (E) -- (F);
  \draw[dashed] ($(E)!-.35!(F)$) -- ($(E)!1.35!(F)$);
  \fill (O) circle (2pt) node[below left] {$O$};
  \foreach \p in {A,B,C,D,E,F} {\fill (\p) circle (1.6pt) node[above right] {$\p$};}
  \node at (1.1,0.55) {сектор};
  \node at (0,-1.75) {сегмент};
\end{tikzpicture}""",
    7: r"""\begin{tikzpicture}[scale=1.0]
  \draw[thick] (0,0) circle (2.2);
  \coordinate (M) at (170:2.2);
  \coordinate (N) at (105:2.2);
  \coordinate (P) at (35:2.2);
  \draw[very thick,color=primaryblue] (M) arc (170:105:2.2);
  \draw[very thick,color=feynmangreen] (N) arc (105:35:2.2);
  \foreach \p/\name in {M/M,N/N,P/P} {
    \fill (\p) circle (2pt) node[above] {$\name$};
  }
  \fill (0,0) circle (2pt) node[below] {$O$};
  \node at (0,2.65) {$\overset{\frown}{MP}=\overset{\frown}{MN}+\overset{\frown}{NP}$};
\end{tikzpicture}""",
}


def _clean_tikz(block: str) -> str:
    lines = [line for line in block.splitlines() if r"\textbf{Рис." not in line]
    return "\n".join(lines).strip() + "\n"


def migrate_figures() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for number, source in INTRO_FIGURES.items():
        (OUTPUT_DIR / f"fig-{number:03d}.tex").write_text(source + "\n", encoding="utf-8")

    manual = MANUAL_SECTION.read_text(encoding="utf-8")
    blocks = re.findall(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", manual, flags=re.DOTALL)
    source_blocks = blocks[: len(ANGLE_FIGURE_GROUPS)]
    if len(source_blocks) != len(ANGLE_FIGURE_GROUPS):
        raise ValueError("The manual reference no longer contains the expected figure set")

    for numbers, block in zip(ANGLE_FIGURE_GROUPS, source_blocks, strict=True):
        name = "fig-014-015.tex" if numbers == (14, 15) else f"fig-{numbers[0]:03d}.tex"
        header = "% Extracted from the reviewed manual pilot; edit the source reference first.\n"
        (OUTPUT_DIR / name).write_text(header + _clean_tikz(block), encoding="utf-8")
    return 27


def main() -> int:
    count = migrate_figures()
    print(f"Prepared {count} vector figures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
