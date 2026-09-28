---
name: p5js
description: Implementation engine and best practices for p5.js interactive canvas simulations, physics engines, particle systems, and gamified educational STEM models for 7th graders. Use when creating tactile, interactive browser simulations (gravity, collisions, molecular diffusion, levers, light reflection) running standalone in HTML or embedded in Marimo.
---

# 🎨 p5.js: Інтерактивні фізико-хімічні симуляції та науковий кодинг

Цей скіл керує розробкою тактильних, інтерактивних 2D/3D симуляцій на базі **p5.js** для наочного вивчення природничих наук (фізика, хімія, біологія, математика) учнями 7 класу.

---

## 🧭 Чому p5.js незамінний для 7 класу?

1. **Тактильність (Enactive Phase за Брунером):** Дитина може схопити мишкою вантаж на важелі, потягнути пружину, розігнати молекулу або змінити кут падіння променя світла в реальному часі на 60 FPS.
2. **Миттєвий зворотний зв'язок:** Будь-яка зміна маси чи температури одразу відображається у поведінці частинок на екрані.
3. **Автономність:** Працює у будь-якому браузері (комп'ютер, планшет, смартфон) через один HTML-файл або вбудовується всередину Marimo-ноутбука.

---

## 📐 Режими роботи: Global Mode проти Instance Mode

- **Для автономних HTML-сторінок:** використовується класичний **Global Mode** (`function setup()`, `function draw()`).
- **Для вбудовування в Marimo / Generative UI:** **ЗАВЖДИ** використовується **Instance Mode** (`new p5((p) => { ... }, container)`), щоб уникнути конфліктів у глобальному просторі імен `window`.

### Шаблон автономного HTML (з Tailwind CSS та адаптивним канвасом):

```html
<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Інтерактивна симуляція</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
</head>
<body class="bg-slate-900 text-slate-100 flex flex-col items-center justify-center min-h-screen p-4">
  <div class="max-w-3xl w-full bg-slate-800 p-6 rounded-2xl shadow-2xl border border-slate-700">
    <h1 class="text-2xl font-bold text-cyan-400 mb-2" id="sim-title">Назва симуляції</h1>
    <p class="text-slate-300 text-sm mb-4" id="sim-desc">Опис завдання або інструкція для експерименту.</p>
    
    <div id="canvas-container" class="relative rounded-xl overflow-hidden border border-slate-700 mx-auto"></div>

    <div class="mt-4 flex flex-wrap gap-4 items-center justify-between" id="ui-panel">
      <!-- Додаткові контролери HTML -->
    </div>
  </div>

  <script>
    const sketch = (p) => {
      p.setup = () => {
        const container = document.getElementById('canvas-container');
        const c = p.createCanvas(container.offsetWidth || 640, 400);
        c.parent('canvas-container');
      };

      p.draw = () => {
        p.background(24, 28, 38);
        // логіка анімації
      };

      p.windowResized = () => {
        const container = document.getElementById('canvas-container');
        p.resizeCanvas(container.offsetWidth, 400);
      };
    };

    new p5(sketch);
  </script>
</body>
</html>
```

---

## ⚙️ Фізичний рушій у p5.js (Вектори, Сили, Зіткнення)

Для учнів 7 класу рух описується за законами класичної механіки:
$$\vec{v} = \vec{v}_0 + \vec{a} \cdot \Delta t, \quad \vec{x} = \vec{x}_0 + \vec{v} \cdot \Delta t$$

```javascript
class PhysicalParticle {
  constructor(p, x, y, mass) {
    this.p = p;
    this.pos = p.createVector(x, y);
    this.vel = p.createVector(0, 0);
    this.acc = p.createVector(0, 0);
    this.mass = mass;
    this.radius = Math.sqrt(mass) * 12;
    this.color = '#38bdf8';
  }

  applyForce(force) {
    // Другий закон Ньютона: a = F / m
    let f = p5.Vector.div(force, this.mass);
    this.acc.add(f);
  }

  update() {
    this.vel.add(this.acc);
    this.pos.add(this.vel);
    this.acc.mult(0); // Скидання прискорення після кожного такту
  }

  checkBoundaries(width, height, damping = 0.85) {
    if (this.pos.x + this.radius > width) {
      this.pos.x = width - this.radius;
      this.vel.x *= -damping;
    } else if (this.pos.x - this.radius < 0) {
      this.pos.x = this.radius;
      this.vel.x *= -damping;
    }

    if (this.pos.y + this.radius > height) {
      this.pos.y = height - this.radius;
      this.vel.y *= -damping;
    } else if (this.pos.y - this.radius < 0) {
      this.pos.y = this.radius;
      this.vel.y *= -damping;
    }
  }

  display() {
    this.p.fill(this.color);
    this.p.noStroke();
    this.p.circle(this.pos.x, this.pos.y, this.radius * 2);
  }
}
```

---

## 🧪 7 Клас: Готові концептуальні симуляції

### 1. Фізика: Важіль Архімеда (Правило моментів сил: $F_1 \cdot d_1 = F_2 \cdot d_2$)
- **Інтерактив:** Дошка на опорі. Учень мишкою може перетягувати гирки різної маси (1 кг, 2 кг, 5 кг) на різні позначки лінійки ліворуч і праворуч.
- **Візуальний ефект:** Важіль нахиляється під дією сумарного обертального моменту. З'являються кольорові стрілки сил з підписаними значеннями моментів ($M = F \cdot d$). Коли досягнуто рівноваги — спалахує зелене світло!

### 2. Фізика/Хімія: Броунівський рух і дифузія в теплій та холодній воді
- **Інтерактив:** Посудина з 200 дрібними молекулами води (швидкі сині кульки) та 1 великою молекулою пилку (велика жовта куля).
- **Повзунок температури ($T$):** Збільшення $T$ збільшує середню швидкість хаотичного руху часток.
- **Ефект:** Траєкторія руху пилку залишає світний неоновий слід, показуючи випадкові блукання.

### 3. Хімія: Будова атома (Планетарна модель Резерфорда-Бора)
- **Інтерактив:** Клік по елементах від Гідрогену (H, $Z=1$) до Оксигену (O, $Z=8$).
- **Візуалізація:** Ядро з протонами й нейтронами та енергетичні рівні з рухомими електронами. Учень наочно бачить правило: перший рівень — максимум 2 електрони, другий — до 8.

### 4. Біологія: Дифузія та осмос через напівпроникну клітинну мембрану
- **Інтерактив:** Мембрана з порами розділяє екран навпіл. Дрібні молекули води проходять крізь пори, а великі молекули солі/цукру блокуються.

---

## 🎨 Дизайн-код та візуальний стиль для дитини
1. **Неоновий темний стиль (Modern Sci-Fi Lab):**
   - Фон: темно-синій або графітовий `#0F172A`.
   - Частки: яскраві неонові кольори (`#38BDF8` блакитний, `#FACC15` бурштиновий, `#4ADE80` смарагдовий, `#F87171` корал).
   - Ефект світіння частинок:
     ```javascript
     p.drawingContext.shadowBlur = 12;
     p.drawingContext.shadowColor = 'rgba(56, 189, 248, 0.6)';
     ```
2. **Тактильний Drag-and-Drop:**
   - Курсор змінюється на `cursor(HAND)` при наведенні на рухомий об'єкт.
   - Об'єкт збільшується або підсвічується при захопленні.

---

## 🎯 Чеклист симуляції
- [ ] Працює плавно на 60 FPS без лагів пам'яті.
- [ ] Очищення холста в `draw()` (`p.background()`).
- [ ] Усі сили мають коректні розмірності та напрямки стрілок.
- [ ] Є кнопка "Скинути симуляцію" (Reset) або пауза.
- [ ] Адаптується під розмір екрана через `windowResized()`.
