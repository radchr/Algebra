---
name: marimo
description: Comprehensive implementation engine and best practices for Marimo (v0.25+) reactive Python notebooks and educational web dashboards. Use whenever building, modifying, running, or exporting interactive reactive applications, STEM sandboxes, virtual science labs, or interactive calculators. Covers reactive DAG architecture, UI components (sliders, dropdowns, forms), layout, state management, charting integration (Plotly, Altair, Matplotlib), and web deployment.
---

# 🚀 Marimo: Реактивні дашборди та віртуальні лабораторії для STEM

Цей скіл керує створенням інтерактивних реактивних додатків і веб-дашбордів на базі **Marimo** для вивчення математики, фізики, хімії та біології у 7 класі.

---

## 🧭 Чому саме Marimo для 7 класу?

1. **Реактивність без перезавантаження сторінки:** Коли учень тягне повзунок густини рідини чи швидкості автомобіля, графіки та анімації перераховуються миттєво (за принципом електронних таблиць).
2. **Чистий Python-скрипт (`.py`):** Кожен ноутбук — це звичайний версіонований Python-файл без сміття прихованих JSON-метаданих.
3. **Режим додатку (App Mode):** Можливість показувати учню тільки гарний інтерфейс лабораторії без коду (`marimo run`), або повний інтерактивний редактор (`marimo edit`).
4. **Експорт у WASM / статичний HTML:** Можливість скомпілювати будь-яку лабораторію в один автономний HTML-файл, який відкривається у будь-якому браузері без встановленого Python!

---

## ⚡ Швидкий старт та CLI-команди (через `uv`)

```bash
# Відкрити інтерактивний редактор у браузері:
uv run marimo edit notebooks/physics/archimedes_lab.py

# Запустити як готовий веб-додаток (без показу вихідного коду клітин):
uv run marimo run notebooks/physics/archimedes_lab.py --port 8080

# Експорт у статичний веб-сайт на базі Pyodide / WebAssembly:
uv run marimo export html-wasm notebooks/physics/archimedes_lab.py -o dist/archimedes.html

# Запуск перевірки синтаксису або тестів:
uv run marimo check notebooks/physics/archimedes_lab.py
```

---

## ⚙️ Фундаментальні правила реактивної архітектури Marimo (DAG)

1. **Single Assignment Rule (Правило єдиного визначення):**
   - Змінна з глобальним ім'ям (наприклад `slider_density` або `df`) може бути оголошена **тільки в одній клітинці**.
   - Не можна переприсвоювати одну й ту саму глобальну змінну в різних клітинах.
   - Для локальних тимчасових змінних використовуйте підкреслення на початку: `_temp = x + 1` (Marimo не відстежує змінні з `_` в глобальному DAG).

2. **UI Елементи повертають значення через `.value`:**
   - Створення елемента: `density_slider = mo.ui.slider(start=700, stop=13600, step=50, value=1000, label="Густина рідини, кг/м³")`
   - Читання значення в наступній клітинці: `current_rho = density_slider.value`
   - *Важливо:* Не читайте `.value` у тій же самій клітинці, де елемент створюється. Оголошуйте UI-елемент в одній клітинці, а використовуйте його значення в інших.

3. **Справжній стан через `mo.state`:**
   - Якщо потрібен накопичувальний стан (наприклад, лічильник балів у вікторині, крок симуляції чи історія вимірювань):
   ```python
   get_score, set_score = mo.state(0)
   # Оновлення:
   set_score(lambda prev: prev + 1)
   # Читання:
   current_score = get_score()
   ```

---

## 🧩 Головні UI-компоненти Marimo

| Компонент | Приклад використання | Призначення |
|---|---|---|
| `mo.ui.slider` | `mo.ui.slider(1, 100, step=1, value=50, label="Швидкість (км/год)")` | Плавна зміна параметрів |
| `mo.ui.dropdown` | `mo.ui.dropdown({"Вода": 1000, "Олія": 900, "Ртуть": 13600}, value="Вода")` | Вибір речовини чи режиму |
| `mo.ui.number` | `mo.ui.number(start=0, stop=100, step=0.1, value=10.5)` | Точне числове введення |
| `mo.ui.radio` | `mo.ui.radio(options=["Тверде", "Рідке", "Газоподібне"], value="Рідке")` | Агрегатний стан речовини |
| `mo.ui.checkbox` | `mo.ui.checkbox(label="Враховувати опір повітря", value=False)` | Вмикання/вимикання сил |
| `mo.ui.button` | `mo.ui.button(label="🧪 Змішати реагенти", on_click=lambda: ...)` | Тригер події чи скидання |
| `mo.ui.tabs` | `mo.ui.tabs({"Теорія": tab1, "Експеримент": tab2, "Тест": tab3})` | Структурування уроку |

---

## 🧱 Компонування та оформлення (Layout & UX)

Для учнів 7 класу інтерфейс має бути охайним, барвистим та інтуїтивно зрозумілим:

```python
import marimo as mo

# Банер з інструкцією або підказкою
banner = mo.callout(
    mo.md("💡 **Експеримент:** Збільшуй густину рідини і спостерігай, як виштовхувальна сила піднімає кульку на поверхню!"),
    kind="info"
)

# Панель приладів (метрики результатів)
stat_box = mo.hstack([
    mo.stat(value=f"{f_arch:.2f} Н", label="Сила Архімеда"),
    mo.stat(value=f"{f_grav:.2f} Н", label="Сила тяжіння"),
    mo.stat(value="Плаває" if f_arch >= f_grav else "Тоне", label="Стан тіла")
], justify="space-around")

# Розміщення: сайдбар з керуванням + робоча зона з графіками
app_layout = mo.hstack([
    mo.vstack([slider_mass, slider_volume, dropdown_liquid], gap=1.5),
    mo.vstack([banner, stat_box, dynamic_plot], gap=2)
], widths=[1, 3])
```

---

## 🔬 Канонічний шаблон: Інтерактивна лабораторія (7 клас Фізика — Сила Архімеда)

```python
import marimo

app = marimo.App(width="medium")

@app.cell
def imports():
    import marimo as mo
    import plotly.graph_objects as go
    return mo, go

@app.cell
def header(mo):
    mo.md(r"""
    # 🌊 Віртуальна лабораторія: Закон Архімеда та плавання тіл
    ### 7 клас • Фізика
    
    > **Закон Архімеда:** На тіло, занурене в рідину або газ, діє виштовхувальна сила, яка дорівнює вазі витісненої рідини:
    > $$F_A = \rho_{\text{р}} \cdot g \cdot V_{\text{зан}}$$
    """)
    return

@app.cell
def controls(mo):
    liquid_select = mo.ui.dropdown(
        options={
            "Вода (1000 кг/м³)": 1000,
            "Олія (900 кг/м³)": 900,
            "Солона вода (1030 кг/м³)": 1030,
            "Ртуть (13600 кг/м³)": 13600
        },
        value="Вода (1000 кг/м³)",
        label="Рідина в мензурці:"
    )
    
    volume_slider = mo.ui.slider(
        start=0.1, stop=2.0, step=0.1, value=0.5,
        label="Об'єм тіла V (дм³ або літрів):"
    )
    
    mass_slider = mo.ui.slider(
        start=0.1, stop=3.0, step=0.1, value=0.6,
        label="Маса тіла m (кг):"
    )
    
    controls_view = mo.vstack([
        mo.md("### ⚙️ Налаштування експерименту"),
        liquid_select,
        volume_slider,
        mass_slider
    ], gap=1.5)
    
    return controls_view, liquid_select, mass_slider, volume_slider

@app.cell
def physics_engine(liquid_select, mass_slider, volume_slider):
    g = 9.8  # м/с²
    rho_liquid = liquid_select.value
    v_total_m3 = volume_slider.value * 0.001  # переведення з дм³ у м³
    m_body = mass_slider.value
    
    # Сила тяжіння
    f_grav = m_body * g
    
    # Максимальна сила Архімеда (при повному зануренні)
    f_arch_max = rho_liquid * g * v_total_m3
    
    # Визначення рівноваги
    if f_arch_max < f_grav:
        status = "🔴 Тіло тоне (лежить на дні)"
        status_color = "danger"
        f_arch_actual = f_arch_max
        submerged_ratio = 1.0
    elif abs(f_arch_max - f_grav) < 0.01:
        status = "🟡 Тіло зависло у товщі рідини"
        status_color = "warn"
        f_arch_actual = f_grav
        submerged_ratio = 1.0
    else:
        status = "🟢 Тіло плаває на поверхні"
        status_color = "success"
        f_arch_actual = f_grav
        submerged_ratio = f_grav / f_arch_max
        
    return f_arch_actual, f_grav, status, status_color, submerged_ratio

@app.cell
def visualizer(f_arch_actual, f_grav, go, mo, status, status_color, submerged_ratio):
    # Побудова наочного графіка сил
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=["Сила тяжіння (F_тяж)", "Сила Архімеда (F_А)"],
        y=[f_grav, f_arch_actual],
        marker_color=["#E74C3C", "#3498DB"],
        text=[f"{f_grav:.2f} Н", f"{f_arch_actual:.2f} Н"],
        textposition="auto"
    ))
    
    fig.update_layout(
        title="Порівняння діючих сил",
        yaxis_title="Сила, Ньютони (Н)",
        template="plotly_dark",
        height=320,
        margin=dict(l=40, r=40, t=50, b=40)
    )
    
    results_card = mo.vstack([
        mo.callout(mo.md(f"### {status}\nЗанурена частина: **{submerged_ratio*100:.1f}%**"), kind=status_color),
        mo.ui.plotly(fig)
    ])
    
    return fig, results_card

@app.cell
def layout(controls_view, mo, results_card):
    mo.hstack([controls_view, results_card], widths=[1, 1], gap=2)
```

---

## 🌐 Двостороння інтеграція: `mo.ui.anywidget` (JavaScript ⟷ Python)

Для складних інтерактивних моделей, де дитина перетягує об'єкти мишкою на Canvas (p5.js або D3.js) і координати мають передаватися назад у Python (наприклад, у SymPy для розв'язання рівняння рівноваги):

```python
import anywidget
import traitlets
import marimo as mo

class InteractiveLeverWidget(anywidget.AnyWidget):
    # Двосторонній синхронізований стан між JS та Python
    lever_angle = traitlets.Float(0.0).tag(sync=True)
    mass_left = traitlets.Float(1.0).tag(sync=True)

    _esm = """
    function render({ model, el }) {
        const container = document.createElement("div");
        container.style.cssText = "width: 100%; height: 200px; background: #0f172a; border-radius: 12px; display: flex; align-items: center; justify-content: center;";
        
        const info = document.createElement("div");
        info.style.color = "#38bdf8";
        
        function update() {
            info.innerHTML = `Кут нахилу важеля: <b>${model.get("lever_angle").toFixed(1)}°</b>`;
        }
        
        model.on("change:lever_angle", update);
        update();
        container.appendChild(info);
        el.appendChild(container);
    }
    export default { render };
    """

# Огортання у реактивний Marimo UI:
lever_ui = mo.ui.anywidget(InteractiveLeverWidget())
```

### Групування через `mo.ui.form` (Зниження когнітивного навантаження)

Коли учень налаштовує складний дослід (3-4 повзунки), живий перерахунок під час руху повзунка створює зорове мерехтіння і заважає зосередитися. Використовуйте `.form()`:

```python
experiment_form = mo.ui.form(
    element=mo.vstack([density_slider, volume_slider, temperature_slider]),
    submit_button_label="🚀 Провести дослід (Запустити)"
)
```

---

## 🎯 Чеклист якості дашборду перед демонстрацією учню
- [ ] Немає повторних оголошень глобальних змінних (Single Assignment).
- [ ] Кожен повзунок має розмірність у підписі (наприклад, "м/с", "кг", "см²").
- [ ] Є чіткий висновок або підсумок (що саме сталося і чому).
- [ ] Застосовані дружні кольори, текст пояснює явище просто без нагромадження псевдонаукових ярликів.
- [ ] Перевірено запуск через `uv run marimo run <file>.py`.
