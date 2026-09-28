---
name: d3js
description: Implementation engine and best practices for D3.js v7 interactive scientific and mathematical visualizations. Use whenever creating dynamic SVG graphs, interactive coordinate planes, function plotters (y=kx+b), periodic tables, food web networks, or phase transition diagrams for 7th grade STEM education. Covers scales, axes, drag/zoom behaviors, force simulations, transitions, and responsive SVG design.
---

# 📊 D3.js (v7): Інтерактивні графіки та наукові візуалізації

Цей скіл керує розробкою точних, динамічних SVG-візуалізацій на базі **D3.js v7** для вивчення математики, фізики, хімії та біології у 7 класі.

---

## 🧭 Чому саме D3.js для 7 класу?

1. **Математична точність SVG:** На відміну від Canvas, SVG будується з векторних геометричних примітивів (`<line>`, `<circle>`, `<path>`), які зберігають кришталеву чіткість за будь-якого масштабування.
2. **Динамічні маніпулятори (Draggable Handles):** Можливість безпосередньо рухати точки графіка мишкою (наприклад, змінювати кутовий коефіцієнт $k$ у прямій $y = kx + b$) і бачити миттєвий перерахунок рівняння.
3. **Силові симуляції (Force-directed Graphs):** Ідеально підходить для харчових ланцюгів у біології, зв'язків між атомами в молекулах та класифікаційних дерев.

---

## 📐 Канонічний шаблон D3.js (Margin Convention & Responsive SVG)

Завжди дотримуйтесь правила відступів D3 (`margin convention`) та використовуйте `viewBox` для повної адаптивності:

```html
<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <title>D3 STEM Visualization</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://d3js.org/d3.v7.min.js"></script>
</head>
<body class="bg-slate-950 text-slate-100 flex flex-col items-center justify-center min-h-screen p-6">
  <div class="w-full max-w-4xl bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
    <div class="flex justify-between items-center mb-4">
      <div>
        <h2 class="text-xl font-bold text-sky-400" id="chart-title">Лінійна функція y = kx + b</h2>
        <p class="text-sm text-slate-400">Перетягуй кольорові точки прямої, щоб побачити зміну нахилу і зсуву</p>
      </div>
      <div id="equation-badge" class="px-4 py-2 bg-slate-800 border border-slate-700 rounded-xl font-mono text-emerald-400 font-bold text-lg">
        y = 2.0x + 1.0
      </div>
    </div>

    <div id="chart-container" class="w-full aspect-[16/9] relative"></div>
  </div>

  <script>
    const container = document.getElementById("chart-container");
    const width = 800;
    const height = 450;
    const margin = { top: 20, right: 30, bottom: 40, left: 50 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const svg = d3.select("#chart-container")
      .append("svg")
      .attr("viewBox", `0 0 ${width} ${height}`)
      .attr("preserveAspectRatio", "xMidYMid meet")
      .classed("w-full h-full", true);

    const g = svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);
  </script>
</body>
</html>
```

---

## 🧮 7 Клас: Математичні та наукові інтерактивні модулі

### 1. Алгебра: Дослідник лінійної функції ($y = kx + b$)

- **Когнітивна проблема 7 класу:** Учень часто плутає роль коефіцієнтів $k$ (кут нахилу) та $b$ (точка перетину з віссю $Oy$).
- **Інтерактивне рішення D3:**
  - Точка перетину $(0, b)$ позначена яскравим помаранчевим кружечком. Її можна тягнути вертикально — пряма паралельно піднімається або опускається.
  - Друга точка на відстані $\Delta x = 1$ позначена блакитним. Її перетягування обертає пряму.
  - Поруч автоматично малюється прямокутний "трикутник нахилу" зі стрілками: зміна $\Delta y$, зміна $\Delta x$, та розрахунок $k = \frac{\Delta y}{\Delta x}$.

```javascript
// Шкали координат
const xScale = d3.scaleLinear().domain([-10, 10]).range([0, innerWidth]);
const yScale = d3.scaleLinear().domain([-10, 10]).range([innerHeight, 0]);

// Сітка координат (Grid)
g.append("g")
  .attr("class", "grid text-slate-800")
  .call(d3.axisBottom(xScale).ticks(20).tickSize(-innerHeight).tickFormat(""));
g.append("g")
  .attr("class", "grid text-slate-800")
  .call(d3.axisLeft(yScale).ticks(20).tickSize(-innerWidth).tickFormat(""));

// Осі координат із стрілками
const xAxis = d3.axisBottom(xScale).ticks(10);
const yAxis = d3.axisLeft(yScale).ticks(10);
g.append("g").attr("transform", `translate(0,${yScale(0)})`).call(xAxis).attr("color", "#64748b");
g.append("g").attr("transform", `translate(${xScale(0)},0)`).call(yAxis).attr("color", "#64748b");

// Лінія функції
const line = g.append("line")
  .attr("stroke", "#38bdf8")
  .attr("stroke-width", 3);

function updatePlot(k, b) {
  const x1 = -10, y1 = k * x1 + b;
  const x2 = 10, y2 = k * x2 + b;

  line
    .attr("x1", xScale(x1))
    .attr("y1", yScale(y1))
    .attr("x2", xScale(x2))
    .attr("y2", yScale(y2));

  d3.select("#equation-badge").text(
    `y = ${k.toFixed(1)}x ${b >= 0 ? '+ ' + b.toFixed(1) : '- ' + Math.abs(b).toFixed(1)}`
  );
}
```

### 2. Фізика: Графік нагрівання та плавлення льоду (Теплові явища)
- Графік залежності температури від часу $T(t)$.
- Ділянки:
  1. Нагрівання льоду (підйом до $0^\circ\text{C}$).
  2. Плавлення льоду (горизонтальна планка при $0^\circ\text{C}$ — температура не росте, доки не розтане весь лід!).
  3. Нагрівання води ($0 \to 100^\circ\text{C}$).
  4. Кипіння (планка при $100^\circ\text{C}$).
- При наведенні курсору на горизонтальну полицю з'являється анімована підказка: *"Куди дівається тепло? Вся енергія йде на руйнування кристалічної ґратки, а не на ріст температури!"*.

### 3. Біологія: Харчова мережа лісу (Force-directed Graph `d3.forceSimulation`)
- Вузли (Nodes): Рослини (продуценти), травоїдні (зайці, миші), хижаки (лисиці, вовки, сови).
- Зв'язки (Links): Стрілки напрямку передачі біомаси й енергії.
- Інтерактивність: Клік на рослину підсвічує всіх тварин, які загинуть або постраждають, якщо цю ланку знищити (системне мислення!).

---

## 🎨 Стандарти оформлення для 7 класу
1. **Зрозумілі підписи осей:** Завжди писати величини і розмірності українською мовою: "Час руху, $t$ (с)", "Шлях, $s$ (м)", "Маса, $m$ (кг)".
2. **Контрастні маркери:** Діаметр інтерактивних рухомих точок не менше `r = 8px` з обведенням `stroke-width: 2px`, щоб у них було легко поцілити мишкою чи пальцем.
3. **Анімовані переходи (Transitions):** При оновленні параметрів значення не повинні "стрибати" миттєво: використовуйте `.transition().duration(400)`.

---

## 🎯 Чеклист готовності графіка
- [ ] Осі підписані з позначенням одиниць вимірювання (СІ).
- [ ] Графік масштабується під будь-який екран завдяки `viewBox`.
- [ ] Рухомі маркери мають очевидний стан наведення (`cursor: grab` / `cursor: grabbing`).
- [ ] Формули оновлюються синхронно з рухом ліній.
