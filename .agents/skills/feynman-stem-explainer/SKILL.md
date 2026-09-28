---
name: feynman-stem-explainer
description: Explains complex STEM concepts (Mathematics, Physics, Chemistry, Biology, Computer Science) with Richard Feynman's legendary clarity, transforming abstract equations and jargon into intuitive physical models accessible to a 10-year-old or an expert. Use this skill whenever the user asks to "explain like Feynman", "explain simply", "поясни як Фейнман", "поясни просто", "поясни як дитині", "педагогіка Фейнмана", "Feynman technique", "explain intuitively", "поясни на пальцях", or when demystifying any difficult scientific or mathematical topic across STEM disciplines.
---

# 🧠 Feynman STEM Explainer: The Architecture of Intuition

> *"I couldn't reduce it to the freshman level. That means we really don't understand it."*  
> — Richard Feynman, after being asked to explain why spin-one-half particles obey Fermi-Dirac statistics

This skill provides a battle-tested pedagogical framework synthesizing **Richard Feynman's explanatory genius** with modern cognitive learning science: **Concreteness Fading (Bruner / CRA)**, **Teaching-With-Analogies (Glynn / TWA)**, and **Johnstone's Chemistry Triangle**.

---

## 🧭 The 5-Stage Feynman Explanatory Protocol

Whenever tasked with explaining a complex STEM topic, execute the following 5 stages in sequence:

```
[ Stage 1: The Feynman Razor ]  ---> Strip jargon; find the single tactile physical anchor
             ↓
[ Stage 2: Concreteness Fading ] ---> Concrete (Enactive) -> Visual (Iconic) -> Formal (Symbolic)
             ↓
[ Stage 3: Structure-Mapping ]   ---> Feature-by-feature mapping + WHERE THE ANALOGY BREAKS DOWN
             ↓
[ Stage 4: Domain Playbook ]    ---> Apply specialized Math / Physics / Chemistry / Biology lever
             ↓
[ Stage 5: The 10-Second Test ]  ---> Interactive thought puzzle or verification game
```

---

### Stage 1: The Feynman Razor (Jargon Deconstruction)

1. **Ban the Magic Labels:**
   - Terminology is not understanding. Ban words like *"homeostasis"*, *"entropy"*, *"eigenvalue"*, *"catalysis"*, *"homology"* until the physical action behind them has been fully described.
   - *Test:* If an explanation relies on a Latin or Greek word to make sense, the explanation has failed. Replace the word with **what particles, forces, or shapes are actually doing**.
2. **The Anchoring Question:**
   - Frame the problem around a tangible everyday mystery or paradox.
   - *Physics:* "Why doesn't a bicycle fall over when moving, but falls when stopped?"
   - *Chemistry:* "Why does a match need a rough strike to burst into flame, but then burns by itself?"
   - *Biology:* "How does a tree pump hundreds of liters of water 100 meters up without a heart?"
   - *Mathematics:* "How do you calculate the area of an oil spill with irregular squiggly borders?"

---

### Stage 2: Concreteness Fading (CRA Sequence)

Follow Jerome Bruner's cognitive gradient (see `references/concrete-fading-cra.md`):
1. **Concrete (Enactive):** Physical, sensory, mechanical actions (pushing, blowing bubbles, rubber bands, coins, gears).
2. **Representational (Iconic):** Visual schematics, diagrams, geometric flowcharts, arrows, color-coded components.
3. **Abstract (Symbolic):** Mathematical equations, chemical formulas, formal notation. **Rule: Introduce symbolic formulas ONLY after the learner can already predict the outcome qualitatively!**

---

### Stage 3: Structure-Mapping & The Analogy Safeguard

Follow the Teaching-With-Analogies (TWA) model (see `references/analogy-engine-twa.md`):
1. **Map Deep Relational Structures:** Do not map superficial traits (e.g. "it's round like a ball"). Map functional dynamics (e.g. "the core pulls inward while momentum pushes outward").
2. **⚠️ The Mandatory Analogy Breakdown Section:**
   - Every great analogy has a breaking point. You **MUST** include a dedicated subsection titled:
     `🔍 Де метафора ламається (Границя аналогії)`
   - State clearly where the everyday object differs from the quantum, chemical, or biological reality to prevent deep misconceptions.

---

### Stage 4: Domain-Specific Execution Playbooks

Consult `references/stem-domain-playbooks.md` to trigger discipline-specific levers:

* **📐 Mathematics (Geometry & Transformation First):**
  - Explain *why* the mathematical tool was invented (who was stuck on what problem?).
  - Turn symbolic algebra into spatial transformations (stretching, rotating, folding, projecting).
  - Test extreme cases ($0, 1, \infty, -1$) to verify sanity.

* **🧲 Physics (Atoms in Motion & Gedankens):**
  - Ground in Feynman's principle: all phenomena arise from little particles jiggling, attracting, and repelling.
  - Put the reader inside the physical system via thought experiments (*"Imagine you are an electron..."*).
  - Energy and momentum as indestructible gold coins being swapped between bank accounts.

* **🧪 Chemistry (Johnstone's Triangle & Electron Drama):**
  - Bridge the 3 levels: Macro observation (color, fizz, heat) $\longleftrightarrow$ Sub-micro particulate (electron exchange) $\longleftrightarrow$ Symbolic equation.
  - Frame reactions as dramatic struggles of atoms seeking stable electron shells (electronegativity = greed).
  - Landscape of energetic hills (activation energy) and valleys (stable products).

* **🧬 Biology (Nanomachines & Scale Navigation):**
  - Strip the Latin names; explain the cellular machinery mechanically (rotary motors, zip lines, 3D printers, barcode readers).
  - Maintain strict evolutionary logic: never say *"the cell does X in order to Y"* (avoid teleology); explain how random variation and selection built the mechanism.
  - Zoom continuously across scales: Organism $\longleftrightarrow$ Organ $\longleftrightarrow$ Cell $\longleftrightarrow$ Molecule.

---

### Stage 5: The Feynman Verification Loop

End every explanation with an interactive challenge:
1. **The 10-Second Child Test:** A summary that any 10-year-old could recite on the playground to sound like a genius.
2. **Interactive Puzzle / Thought Game:** A riddle or practical question (e.g., *"What happens if we double the pressure?"*, *"Which of these 3 objects has the same topology?"*).

---

## 📋 Standard Output Structure for Explanations

When writing an explanation using this skill, structure your output with these clear, vibrant sections:

```markdown
# [🎨 Приваблива назва з метафорою Фейнмана]
> **«Цитата або парадокс Фейнмана»**

## ☕ 1. Таємниця, яку ми розгадаємо (Без підручникового туману)
[Парадокс або спостереження з реального життя, яке ламає шаблон]

## 🛠️ 2. Уяви собі... (Метафора та фізична модель)
[Конкретна відчутна дія: мильні бульбашки, шестерні, шеренга людей, мотузка]

## 🗺️ 3. Як це насправді влаштовано (Схема та механізм)
[Крок за кроком: що насправді рухається, штовхає чи притягує]

## 🔍 4. Де метафора ламається (Чесність ученого)
[Де закінчується побутове порівняння і починається точна наука]

## 📐 5. Формула, яка тепер має сенс (Символьний рівень)
[Формула або рівняння, де кожна літера розшифрована через фізичну дію]

## 🎯 6. Перевір себе за 10 секунд (Загадка Фейнмана)
[Коротка весела загадка на перевірку інтуїції]
```

---

## ⚡ Style & Voice Guidelines

* **Tone:** Warm, playful, passionate, intellectually honest, direct ("you" and "I").
* **Sensory Words:** Use verbs of physical action: *зіштовхуються, роздмухуються, липнуть, пружинять, зриваються, перетікають*.
* **Zero Condescension:** Treat the learner as a brilliant, curious peer who simply hasn't seen the physical picture yet.
* **Acknowledge the Mystery:** If science doesn't know the ultimate "why" (e.g. why mass bends spacetime, why quantum entanglement happens), say it openly! *"Nobody knows why, but that's what makes nature so darn exciting!"*.
