import os
import subprocess

import pypdfium2 as pdfium

SCRATCH_DIR = (
    r"C:\Users\taxco\.gemini\antigravity\brain\33bf9318-001d-4b23-a552-53b42b3e3d9d\scratch"
)
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROJECT_ROOT = r"c:\Users\taxco\Dev\Algebra"
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

HTML_SHELL = """<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="utf-8">
<title>{title}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
<style>
  @page {{
    size: A4;
    margin: 14mm 16mm 16mm 16mm;
  }}
  * {{
    box-sizing: border-box;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    line-height: 1.5;
    font-size: 13px;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
  }}
  .doc-header {{
    border-bottom: 2px solid #2563eb;
    padding-bottom: 10px;
    margin-bottom: 16px;
  }}
  .badge-tag {{
    display: inline-block;
    padding: 3px 8px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-radius: 4px;
    margin-bottom: 5px;
  }}
  .badge-primary {{ background: #eff6ff; color: #1d4ed8; }}
  .badge-orig {{ background: #fef3c7; color: #92400e; }}
  .badge-sympy {{ background: #dcfce7; color: #166534; }}
  .badge-pedagogy {{ background: #f3e8ff; color: #6b21a8; }}
  .badge-warn {{ background: #fee2e2; color: #991b1b; }}

  h1 {{
    font-size: 20px;
    font-weight: 800;
    color: #0f172a;
    margin: 2px 0 4px 0;
  }}
  .subtitle {{
    font-size: 13.5px;
    color: #3b82f6;
    font-weight: 600;
    margin-bottom: 4px;
  }}
  .meta-box {{
    font-size: 11.5px;
    color: #64748b;
    background: #f8fafc;
    border-left: 3px solid #3b82f6;
    padding: 5px 8px;
    border-radius: 0 4px 4px 0;
  }}
  .section-banner {{
    background: linear-gradient(135deg, #1e3a8a, #2563eb);
    color: #ffffff;
    padding: 8px 12px;
    border-radius: 5px;
    margin: 14px 0 12px 0;
  }}
  .section-banner h2 {{
    margin: 0;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.3px;
  }}
  .section-banner p {{
    margin: 2px 0 0 0;
    font-size: 11.5px;
    opacity: 0.9;
  }}
  .problem-card {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 9px 12px;
    margin-bottom: 10px;
    page-break-inside: avoid;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
  }}
  .problem-header {{
    display: flex;
    align-items: baseline;
    gap: 8px;
  }}
  .problem-num {{
    font-weight: 800;
    font-size: 14px;
    color: #1d4ed8;
    min-width: 26px;
  }}
  .problem-text {{
    font-size: 13px;
    color: #1e293b;
    flex: 1;
  }}
  .sub-list {{
    margin: 6px 0 2px 24px;
    padding: 0;
    list-style-type: none;
  }}
  .sub-list li {{
    margin-bottom: 3px;
    font-size: 12.8px;
  }}
  .sub-list-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4px 16px;
    margin: 6px 0 2px 24px;
    padding: 0;
    list-style-type: none;
  }}
  .sub-list-grid li {{
    font-size: 12.8px;
  }}
  .sub-list-grid-3 {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 4px 12px;
    margin: 6px 0 2px 24px;
    padding: 0;
    list-style-type: none;
  }}
  .sub-list-grid-3 li {{
    font-size: 12.8px;
  }}
  .didactic-box {{
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-left: 4px solid #16a34a;
    padding: 9px 12px;
    margin: 12px 0;
    border-radius: 0 6px 6px 0;
    page-break-inside: avoid;
  }}
  .didactic-box-title {{
    font-weight: 700;
    color: #15803d;
    font-size: 12.5px;
    margin-bottom: 3px;
  }}
  .didactic-box p {{
    margin: 0;
    font-size: 12px;
    color: #166534;
  }}
  .sol-container {{
    border-top: 1px dashed #cbd5e1;
    margin-top: 7px;
    padding-top: 7px;
  }}
  .sol-meta-row {{
    display: flex;
    gap: 8px;
    margin-bottom: 4px;
    align-items: baseline;
    font-size: 12.5px;
  }}
  .sol-meta-label {{
    font-weight: 700;
    min-width: 170px;
    font-size: 11.5px;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }}
  .sol-meta-val {{
    flex: 1;
  }}
  .pedagogy-details {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 5px;
    padding: 7px 10px;
    margin-top: 6px;
    font-size: 12px;
    color: #334155;
    line-height: 1.45;
  }}
  .pedagogy-title {{
    font-weight: 700;
    color: #475569;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 2px;
  }}
  .katex {{ font-size: 1.05em; }}
  .formula-block {{
    display: block;
    margin: 4px 0;
    text-align: center;
  }}
</style>
</head>
<body>
{body}
<script>
  renderMathInElement(document.body, {{
    delimiters: [
      {{left: '$$', right: '$$', display: true}},
      {{left: '$', right: '$', display: false}}
    ],
    throwOnError: false
  }});
</script>
</body>
</html>
"""


def generate_problems_html():
    body = """
<div class="doc-header">
  <span class="badge-tag badge-primary">Задачник Кисельова • 7 клас • МОН України</span>
  <h1>А. П. Кисельов — Задачі та вправи до елементів алгебри</h1>
  <div class="subtitle">Розділ I. Алгебраїчні вирази та буквені позначення (§§ 1–5)</div>
  <div class="meta-box">
    <strong>Адаптація та переклад:</strong> Сучасна українська математична термінологія за програмою 7 класу (НУШ / стандарти МОН України).<br>
    <strong>Джерело:</strong> 4-е видання підручника (1931 р.), стор. 7–9 оригіналу (задачі 1–29).
  </div>
</div>

<div class="section-banner">
  <h2>§§ 1–5. Позначення чисел буквами. Складання та читання алгебраїчних виразів</h2>
  <p>Формування навичок переходу від словесних описів до символьних формул, використання буквених змінних, порядок дій та дужки.</p>
</div>

<!-- Задача 1 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">1.</div>
    <div class="problem-text">Сторона квадрата дорівнює $a\\text{ м}$. Виразіть його периметр, а потім його площу.</div>
  </div>
</div>

<!-- Задача 2 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">2.</div>
    <div class="problem-text">Якщо ребро куба дорівнює $m\\text{ см}$, як виразити площу його повної поверхні та його об'єм?</div>
  </div>
</div>

<!-- Задача 3 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">3.</div>
    <div class="problem-text">У прямокутника основа дорівнює $x\\text{ м}$, а висота на $d\\text{ м}$ менша від основи. Виразіть площу цього прямокутника.</div>
  </div>
</div>

<!-- Задача 4 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">4.</div>
    <div class="problem-text">Ребро куба дорівнює $m + n$. Виразіть площу його повної поверхні, а потім його об'єм.</div>
  </div>
</div>

<!-- Задача 5 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">5.</div>
    <div class="problem-text">Основа прямокутника дорівнює $2a + b$, а його висота становить $2a - b$. Як виразити площу цього прямокутника?</div>
  </div>
</div>

<!-- Задача 6 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">6.</div>
    <div class="problem-text">Висота прямокутного паралелепіпеда дорівнює $h$, а сторони прямокутника, що лежить в його основі, дорівнюють $b$ і $c$ (величини $h, b, c$ виражені в однакових лінійних одиницях). Як за допомогою цих величин виразити:</div>
  </div>
  <ul class="sub-list-grid">
    <li><strong>1)</strong> периметр основи;</li>
    <li><strong>2)</strong> площу основи;</li>
    <li><strong>3)</strong> площу повної поверхні паралелепіпеда;</li>
    <li><strong>4)</strong> його об'єм?</li>
  </ul>
</div>

<!-- Задача 7 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">7.</div>
    <div class="problem-text">Якщо мій вік зараз становить $a$ років, то як виразити мій вік через 5 років? Яким був мій вік 5 років тому?</div>
  </div>
</div>

<!-- Задача 8 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">8.</div>
    <div class="problem-text">Запишіть алгебраїчний вираз, який показує, скільки грамів міститься у складеному іменованому числі $a\\text{ кг } b\\text{ дг}$.<br>
    <small style="color:#64748b;"><em>Довідка:</em> в історичному підручнику «дг» позначало декаграм ($1\\text{ дг} = 10\\text{ г}$, оскільки $1\\text{ кг} = 1000\\text{ г}$).</small></div>
  </div>
</div>

<!-- Задача 9 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">9.</div>
    <div class="problem-text">Вартість відправлення телеграми зазвичай обчислюється так: до фіксованого базового тарифу $a\\text{ коп.}$ додається плата за кожне окреме слово по $b\\text{ коп.}$ Яка вартість телеграми, що містить $x$ слів?</div>
  </div>
</div>

<!-- Задача 10 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">10.</div>
    <div class="problem-text">Скільки одиниць міститься в $x$ десятках?</div>
  </div>
</div>

<!-- Задача 11 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">11.</div>
    <div class="problem-text">Деяке двоцифрове число містить $x$ десятків та $y$ одиниць. Скільки всього одиниць у цьому числі?</div>
  </div>
</div>

<!-- Задача 12 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">12.</div>
    <div class="problem-text">У трицифровому числі є $a$ сотень, $b$ десятків і $c$ одиниць. Якою формулою можна виразити загальну кількість одиниць, що міститься в цьому числі?</div>
  </div>
</div>

<!-- Задача 13 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">13.</div>
    <div class="problem-text">Як записати у загальному вигляді число, кратне 7?</div>
  </div>
</div>

<!-- Задача 14 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">14.</div>
    <div class="problem-text">Якщо $k$ — деяке ціле число, то які з наведених чисел будуть парними, а які непарними:
      $$2k, \\quad 2k + 1, \\quad 2k - 1?$$
    </div>
  </div>
</div>

<!-- Задача 15 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">15.</div>
    <div class="problem-text">Деяке ціле число під час ділення на 5 дає остачу 2. Запишіть це число у вигляді алгебраїчної формули.</div>
  </div>
</div>

<!-- Задача 16 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">16.</div>
    <div class="problem-text">Змішали два сорти чаю: першого сорту взяли $a\\text{ кг}$, а другого — $b\\text{ кг}$. Один кілограм першого сорту коштує $m\\text{ грн}$, а другого сорту — $n\\text{ грн}$. Виразіть ціну одного кілограма утвореної суміші.</div>
  </div>
</div>

<!-- Задача 17 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">17.</div>
    <div class="problem-text">В одній коробці лежить $m$ ручок (пер для письма), а в іншій — $n$ ручок. Якщо з першої коробки перекласти в другу $p$ ручок, то в обох коробках стане порівну. Запишіть це твердження за допомогою знаків «$-$», «$+$» та «$=$».</div>
  </div>
</div>

<!-- Задача 18 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">18.</div>
    <div class="problem-text">Запишіть за допомогою знака нерівності твердження про те, що сума цифр натурального двоцифрового числа, яке містить $a$ десятків і $b$ одиниць, менша від самого цього числа.</div>
  </div>
</div>

<!-- Задача 19 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">19.</div>
    <div class="problem-text">Запишіть за допомогою загальноприйнятих алгебраїчних знаків:</div>
  </div>
  <ul class="sub-list-grid">
    <li><strong>1)</strong> суму квадратів чисел $x$ і $y$;</li>
    <li><strong>2)</strong> квадрат суми цих самих чисел;</li>
    <li><strong>3)</strong> добуток квадратів цих чисел;</li>
    <li><strong>4)</strong> квадрат їхнього добутку;</li>
    <li><strong>5)</strong> добуток суми чисел $a$ і $b$ на їхню різницю;</li>
    <li><strong>6)</strong> частку від ділення суми чисел $m$ і $n$ на їхню різницю (двома способами: через знак «$:$» та через риску дробу).</li>
  </ul>
</div>

<!-- Задача 20 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">20.</div>
    <div class="problem-text">Сформулюйте словесно математичні закони, правила та властивості, які виражаються такими формулами:</div>
  </div>
  <ul class="sub-list-grid-3">
    <li><strong>1)</strong> $ab = ba$</li>
    <li><strong>2)</strong> $(x + y)z = xz + yz$</li>
    <li><strong>3)</strong> $(a + b)(a - b) = a^2 - b^2$</li>
    <li><strong>4)</strong> $\\frac{a}{b} = \\frac{am}{bm}$</li>
    <li><strong>5)</strong> $\\frac{a}{m} + \\frac{b}{m} = \\frac{a + b}{m}$</li>
    <li><strong>6)</strong> $(ab)^2 = a^2 b^2$</li>
  </ul>
</div>

<!-- Задача 21 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">21.</div>
    <div class="problem-text">Обчисліть значення виразів при $a = 20$, $b = 8$ і $c = 3$:</div>
  </div>
  <ul class="sub-list-grid-3">
    <li><strong>1)</strong> $(a + b)c$</li>
    <li><strong>2)</strong> $a + bc$</li>
    <li><strong>3)</strong> $(a + b)a - b$</li>
    <li><strong>4)</strong> $(a + b)(a - b)$</li>
    <li><strong>5)</strong> $(a + b) : c$</li>
    <li><strong>6)</strong> $\\frac{a + b}{b + c}$</li>
    <li><strong>7)</strong> $a^2 + b^2$</li>
    <li><strong>8)</strong> $(a + b)^2$</li>
    <li><strong>9)</strong> $a^2 + b^3$</li>
  </ul>
</div>

<!-- Дидактична вставка -->
<div class="didactic-box">
  <div class="didactic-box-title">📖 Зауваження щодо вживання дужок та черговості дій (з підручника А. П. Кисельова)</div>
  <p>Для уникнення зайвого записування дужок у математиці прийнято такий загальний порядок: якщо вираз не містить дужок, то дії виконуються за старшинством: спочатку дії вищого ступеня — піднесення до степеня та добування кореня, потім дії середнього ступеня — множення та ділення, і зрештою дії нижчого ступеня — додавання та віднімання. Дужки вказують на необхідність відступити від цього стандартного порядку.</p>
</div>

<!-- Задача 22 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">22.</div>
    <div class="problem-text">Перевірте правильність таких числових тотожностей при $a = 10$ та $b = 2$:</div>
  </div>
  <ul class="sub-list">
    <li><strong>1)</strong> $(a + b)^2 = a^2 + 2ab + b^2$</li>
    <li><strong>2)</strong> $(a - b)^2 = a^2 - 2ab + b^2$</li>
    <li><strong>3)</strong> $(a + b)(a - b) = a^2 - b^2$</li>
  </ul>
</div>

<!-- Задача 23 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">23.</div>
    <div class="problem-text">Обчисліть значення виразів при $x = 100$ та $y = 20$:</div>
  </div>
  <ul class="sub-list">
    <li><strong>1)</strong> $x - \\{y + [x + y - (x - y)] + 2\\}$</li>
    <li><strong>2)</strong> $xy + [x^2 - (x - y)^2]$</li>
  </ul>
</div>

<!-- Задача 24 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">24.</div>
    <div class="problem-text">Сума чисел натурального ряду від $1$ до $n$ включно виражається формулою:
      $$1 + 2 + 3 + \\dots + n = \\frac{1}{2}n(n + 1).$$
      Перевірте цю формулу для $n = 2$, потім для $n = 3$ і для $n = 4$. Знайдіть за цією формулою суму перших 100 натуральних чисел.
    </div>
  </div>
</div>

<!-- Задача 25 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">25.</div>
    <div class="problem-text">Сума квадратів чисел натурального ряду від $1$ до $n$ включно виражається формулою:
      $$1^2 + 2^2 + 3^2 + \\dots + n^2 = \\frac{1}{6}n(n + 1)(2n + 1).$$
      Перевірте цю формулу для $n = 2, 3, 4$. Обчисліть за нею суму квадратів перших 10 чисел: $1^2 + 2^2 + 3^2 + \\dots + 10^2$.
    </div>
  </div>
</div>

<!-- Задача 26 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">26.</div>
    <div class="problem-text">Сума кубів чисел натурального ряду від $1$ до $n$ включно виражається формулою:
      $$1^3 + 2^3 + 3^3 + \\dots + n^3 = \\frac{1}{4}n^2(n + 1)^2.$$
      Перевірте формулу для $n = 1, 2, 3, 4$. Знайдіть суму кубів перших 100 натуральних чисел.
    </div>
  </div>
</div>

<!-- Задача 27 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">27.</div>
    <div class="problem-text">Запишіть вираз, який утвориться, якщо в добутку $3ab$ підставити замість $a$ суму $x + y$, а замість $b$ — різницю $x - y$.</div>
  </div>
</div>

<!-- Задача 28 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">28.</div>
    <div class="problem-text">У вираз $2m + 3n$ підставте замість $m$ добуток $ab$, а замість $n$ — різницю $a - b$.</div>
  </div>
</div>

<!-- Задача 29 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">29.</div>
    <div class="problem-text">У вираз $\\frac{1}{2}n(n + 1)$ підставте замість $n$ суму $k + 1$.</div>
  </div>
</div>
"""
    return HTML_SHELL.format(title="А. П. Кисельов — Задачі 1–29 (Український переклад)", body=body)


def generate_answers_html():
    body = """
<div class="doc-header">
  <span class="badge-tag badge-sympy">Повний розбір • Верифікація SymPy • 7 клас</span>
  <h1>А. П. Кисельов — Відповіді та покрокові розв'язання</h1>
  <div class="subtitle">Розділ I. Алгебраїчні вирази та буквені позначення (§§ 1–5, Задачі 1–29)</div>
  <div class="meta-box">
    <strong>Математичне ядро:</strong> Кожен результат верифіковано системою комп'ютерної алгебри <code>SymPy</code>.<br>
    <strong>Історичний коментар:</strong> Звірено з оригінальним розділом «Ответы» (стор. 94 видання 1931 р.) з виправленням виявлених опечаток.
  </div>
</div>

<!-- Задача 1 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">1.</div>
    <div class="problem-text"><strong>Умова:</strong> Сторона квадрата дорівнює $a\\text{ м}$. Виразити його периметр і площу.</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">$4a;\\; a^2$</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Сучасний запис</span></span>
      <span class="sol-meta-val">$P = 4a\\text{ (м)},\\quad S = a^2\\text{ (м}^2\\text{)}$</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Покрокове обґрунтування</div>
      Квадрат має 4 рівні сторони довжиною $a$. За означенням периметра: $P = a + a + a + a = 4a\\text{ м}$.<br>
      Площа квадрата дорівнює добутку двох його вимірів: $S = a \\cdot a = a^2\\text{ м}^2$.
    </div>
  </div>
</div>

<!-- Задача 2 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">2.</div>
    <div class="problem-text"><strong>Умова:</strong> Ребро куба дорівнює $m\\text{ см}$. Виразити площу повної поверхні та об'єм.</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">$6m^2;\\; m^3$</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Сучасний запис</span></span>
      <span class="sol-meta-val">$S_{\\text{повн}} = 6m^2\\text{ (см}^2\\text{)},\\quad V = m^3\\text{ (см}^3\\text{)}$</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Покрокове обґрунтування</div>
      Куб обмежений 6 рівними квадратними гранями. Площа однієї грані $S_1 = m \\cdot m = m^2$. Тоді площа всієї поверхні: $S_{\\text{повн}} = 6m^2\\text{ см}^2$.<br>
      Об'єм прямокутного паралелепіпеда з рівними вимірами (куба): $V = m \\cdot m \\cdot m = m^3\\text{ см}^3$.
    </div>
  </div>
</div>

<!-- Задача 3 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">3.</div>
    <div class="problem-text"><strong>Умова:</strong> Основа прямокутника $x\\text{ м}$, висота на $d\\text{ м}$ менша від основи. Виразити площу.</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">$x(x - d)$</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Сучасний запис</span></span>
      <span class="sol-meta-val">$S = x(x - d)\\text{ (м}^2\\text{)} \\quad \\text{або} \\quad S = x^2 - xd\\text{ (м}^2\\text{)}$</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Покрокове обґрунтування</div>
      Висота прямокутника становить $(x - d)\\text{ м}$ (з природною умовою $x > d$). Площа прямокутника є добутком основи на висоту: $S = x \\cdot (x - d) = x(x - d)\\text{ м}^2$.
    </div>
  </div>
</div>

<!-- Задача 4 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">4.</div>
    <div class="problem-text"><strong>Умова:</strong> Ребро куба дорівнює $m + n$. Виразити площу повної поверхні та об'єм.</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">$6(m + n)^2,\\; (m + n)^3$</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Сучасний запис</span></span>
      <span class="sol-meta-val">$S_{\\text{повн}} = 6(m + n)^2,\\quad V = (m + n)^3$</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Покрокове обґрунтування</div>
      Оскільки довжина ребра задана складеним виразом $(m + n)$, його обов'язково беруть у дужки перед піднесенням до степеня. Площа однієї грані: $(m + n)^2$. Повна поверхня (6 граней): $6(m + n)^2$. Об'єм: $(m + n)^3$.
    </div>
  </div>
</div>

<!-- Задача 5 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">5.</div>
    <div class="problem-text"><strong>Умова:</strong> Основа прямокутника $2a + b$, висота $2a - b$. Виразити площу.</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">$(2a + b)(2a - b)$</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Сучасний запис</span></span>
      <span class="sol-meta-val">$S = (2a + b)(2a - b) = 4a^2 - b^2$</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Покрокове обґрунтування</div>
      Площа прямокутника: $S = (2a + b)(2a - b)$. У 7 класі цей вираз розглядається також через формулу скороченого множення (різниця квадратів): $(2a)^2 - b^2 = 4a^2 - b^2$. Обидва записи є тотожно рівними.
    </div>
  </div>
</div>

<!-- Задача 6 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">6.</div>
    <div class="problem-text"><strong>Умова:</strong> Паралелепіпед з висотою $h$ та сторонами прямокутної основи $b$ і $c$. Знайти: 1) $P_{\\text{осн}}$, 2) $S_{\\text{осн}}$, 3) $S_{\\text{повн}}$, 4) $V$.</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">1) $2b + 2c$; 2) $bc$; 3) $2bc + 2ah + 2bh$ <span class="badge-tag badge-warn" style="font-size:10px;">опечатка</span>; 4) $abh$ <span class="badge-tag badge-warn" style="font-size:10px;">опечатка</span></span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Виправлена відповідь</span></span>
      <span class="sol-meta-val">1) $2(b + c)$; 2) $bc$; 3) $2bc + 2bh + 2ch = 2(bc + bh + ch)$; 4) $bch$</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Дидактичний аналіз друкарської помилки 1931 року</div>
      В умові задачі чітко зафіксовано сторони основи $b$ і $c$ та висоту $h$. Проте у виданні 1931 р. у пункті 3) надруковано $2bc + 2ah + 2bh$, а в пункті 4) надруковано $abh$. Складач помилково використав літеру $a$ замість $c$. Справжній об'єм паралелепіпеда зі сторонами $b, c$ і висотою $h$ дорівнює $V = b \\cdot c \\cdot h = bch$.
    </div>
  </div>
</div>

<!-- Задача 7 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">7.</div>
    <div class="problem-text"><strong>Умова:</strong> Вік зараз $a$ років. Який вік через 5 років? Який вік був 5 років тому?</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">$a + 5;\\; a - 5$</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Сучасний запис</span></span>
      <span class="sol-meta-val">Через 5 років: $a + 5$; 5 років тому: $a - 5$ (при $a > 5$)</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Покрокове обґрунтування</div>
      З плином часу вік збільшується додаванням років: $a + 5$. У минулому вік був меншим на відповідну кількість років: $a - 5$.
    </div>
  </div>
</div>

<!-- Задача 8 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">8.</div>
    <div class="problem-text"><strong>Умова:</strong> Скільки грамів міститься у складеному іменованому числі $a\\text{ кг } b\\text{ дг}$?</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">$1000a + 10b$</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Сучасний запис</span></span>
      <span class="sol-meta-val">$1000a + 10b\\text{ (г)}$</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Історична метрологічна довідка</div>
      В $1\\text{ кг}$ міститься $1000\\text{ г}$, отже в $a\\text{ кг}$ маємо $1000a\\text{ г}$.<br>
      У 1930-х роках скорочення «дг» застосовувалося до <em>декаграма</em> ($1\\text{ декаграм} = 10\\text{ г}$), тому $b\\text{ дг} = 10b\\text{ г}$. Загальна кількість грамів: $1000a + 10b$.<br>
      <em>Примітка:</em> у сучасній міжнародній системі SI дециграм позначається «дг» ($0{,}1\\text{ г}$), а декаграм — «даг» ($10\\text{ г}$). Відповідь Кисельова однозначно підтверджує використання декаграма.
    </div>
  </div>
</div>

<!-- Задача 9 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">9.</div>
    <div class="problem-text"><strong>Умова:</strong> Тариф телеграми: фіксована такса $a\\text{ коп.}$, за кожне слово $b\\text{ коп.}$ Вартість телеграми з $x$ слів?</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">$a + bx$</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Сучасний запис</span></span>
      <span class="sol-meta-val">$a + bx\\text{ (коп.)}$</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Педагогічний коментар (лінійна модель)</div>
      Це класична практична модель лінійної функції $y = kx + b$. Постійна частина становить $a$, змінна залежить від обсягу слів: $b \\cdot x$. Загальна сума: $a + bx$.
    </div>
  </div>
</div>

<!-- Задача 10 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">10.</div>
    <div class="problem-text"><strong>Умова:</strong> Скільки одиниць міститься в $x$ десятках?</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">$10x$</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Сучасний запис</span></span>
      <span class="sol-meta-val">$10x$</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Покрокове обґрунтування</div>
      Один десяток містить 10 одиниць. Відповідно, $x$ десятків містять у $x$ разів більше одиниць: $10 \\cdot x = 10x$.
    </div>
  </div>
</div>

<!-- Задача 11 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">11.</div>
    <div class="problem-text"><strong>Умова:</strong> Двоцифрове число має $x$ десятків і $y$ одиниць. Скільки всього одиниць у числі?</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">$10x + y$</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Сучасний запис</span></span>
      <span class="sol-meta-val">$\\overline{xy} = 10x + y$</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Покрокове обґрунтування</div>
      Позиційний десятковий запис: цифра $x$ на місці десятків позначає $10x$ простих одиниць, а цифра $y$ на місці одиниць позначає $y$ одиниць. Разом: $10x + y$.
    </div>
  </div>
</div>

<!-- Задача 12 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">12.</div>
    <div class="problem-text"><strong>Умова:</strong> Трицифрове число містить $a$ сотень, $b$ десятків і $c$ одиниць. Виразити формулою.</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">$100a + 10b + c$</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Сучасний запис</span></span>
      <span class="sol-meta-val">$\\overline{abc} = 100a + 10b + c$</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Покрокове обґрунтування</div>
      Кожна сотня містить 100 одиниць ($100a$), кожен десяток — 10 одиниць ($10b$), та ще $c$ одиниць. Загальна кількість: $100a + 10b + c$.
    </div>
  </div>
</div>

<!-- Задача 13 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">13.</div>
    <div class="problem-text"><strong>Умова:</strong> Як записати у загальному вигляді число, кратне 7?</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">$7a$ (подразумевая под $a$ любое целое число)</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Сучасний запис</span></span>
      <span class="sol-meta-val">$7k, \\quad k \\in \\mathbb{Z}$</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Покрокове обґрунтування</div>
      Число ділиться на 7 без остачі тоді й тільки тоді, коли воно є результатом множення 7 на будь-яке ціле число $k$ (або $a, n$).
    </div>
  </div>
</div>

<!-- Задача 14 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">14.</div>
    <div class="problem-text"><strong>Умова:</strong> Якщо $k \\in \\mathbb{Z}$, які з чисел $2k,\\; 2k+1,\\; 2k-1$ парні, а які непарні?</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">Четное, нечетное, нечетное</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Сучасний запис</span></span>
      <span class="sol-meta-val">$2k$ — парне; $\\quad 2k + 1$ — непарне; $\\quad 2k - 1$ — непарне</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Покрокове обґрунтування</div>
      Вираз $2k$ містить множник 2, отже, обов'язково ділиться на 2 без остачі — воно є парним.<br>
      Додавання чи віднімання одиниці від парного числа змінює парність на протилежну: $2k+1$ та $2k-1$ є непарними числами.
    </div>
  </div>
</div>

<!-- Задача 15 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">15.</div>
    <div class="problem-text"><strong>Умова:</strong> Число при діленні на 5 дає остачу 2. Записати його формулою.</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">$5a + 2$ (где $a$ любое целое число)</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Сучасний запис</span></span>
      <span class="sol-meta-val">$5n + 2, \\quad n \\in \\mathbb{Z}$</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Покрокове обґрунтування</div>
      За теоремою про ділення з остачею (ділене = дільник $\\times$ неповна частка + остача): число $N = 5n + 2$, де неповна частка $n$ — довільне ціле число, а остача $0 \\le 2 < 5$.
    </div>
  </div>
</div>

<!-- Задача 16 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">16.</div>
    <div class="problem-text"><strong>Умова:</strong> Чай: $a\\text{ кг}$ по $m\\text{ грн}$, $b\\text{ кг}$ по $n\\text{ грн}$. Виразити ціну 1 кг суміші.</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">$\\frac{ma + nh}{a + b}$ <span class="badge-tag badge-warn" style="font-size:10px;">опечатка: nh замість nb</span></span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Виправлена відповідь</span></span>
      <span class="sol-meta-val">$\\frac{ma + nb}{a + b}\\text{ (або } \\frac{am + bn}{a + b}\\text{) грн/кг}$</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Покрокове обґрунтування та виправлення опечатки</div>
      Вартість першого сорту: $ma$ (або $am$). Вартість другого сорту: $nb$ (або $bn$). Загальна вартість: $am + bn$.<br>
      Загальна вага суміші: $a + b\\text{ кг}$. Ціна одного кілограма: $\\frac{am + bn}{a + b}$.<br>
      <em>Коментар:</em> у збірнику 1931 р. буква $b$ в чисельнику помилково була набрана як $h$.
    </div>
  </div>
</div>

<!-- Задача 17 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">17.</div>
    <div class="problem-text"><strong>Умова:</strong> В одній коробці $m$ пер, у другій $n$. Якщо з першої перекласти в другу $p$, стане порівну. Записати за допомогою $-, +, =$.</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">$m - p = n + p$</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Сучасний запис</span></span>
      <span class="sol-meta-val">$m - p = n + p$</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Покрокове обґрунтування</div>
      Після перекладання $p$ предметів у першій коробці залишається $m - p$, а в другій стає $n + p$. Умова рівності дає рівняння зв'язку: $m - p = n + p$ (звідки $m - n = 2p$).
    </div>
  </div>
</div>

<!-- Задача 18 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">18.</div>
    <div class="problem-text"><strong>Умова:</strong> Сума цифр двоцифрового числа з $a$ десятків і $b$ одиниць менша від самого числа. Записати нерівність.</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">$a + b < 10a + b$</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Сучасний запис</span></span>
      <span class="sol-meta-val">$a + b < 10a + b$</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Математичне доведення</div>
      Сума цифр: $a + b$. Число: $10a + b$. Запишемо різницю: $(10a + b) - (a + b) = 9a$. Оскільки для двоцифрового числа перша цифра $a \\ge 1$, то $9a > 0$, отже, нерівність $a + b < 10a + b$ завжди строга й істинна.
    </div>
  </div>
</div>

<!-- Задача 19 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">19.</div>
    <div class="problem-text"><strong>Умова:</strong> Записати знаками: 1) суму квадратів $x$ і $y$; 2) квадрат суми; 3) добуток квадратів; 4) квадрат добутку; 5) добуток суми $a$ і $b$ на різницю; 6) частку від ділення суми $m$ і $n$ на різницю.</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">1) $x^2 + y^2$; 2) $(x + y)^2$; 3) $x^2y^2$; 4) $(xy)^2$; 5) $(a+b)(a-b)$; 6) $(m+n):(m-n)$ або $\\frac{m+n}{m-n}$</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Сучасний запис</span></span>
      <span class="sol-meta-val">1) $x^2 + y^2$; 2) $(x + y)^2$; 3) $x^2y^2$; 4) $(xy)^2$; 5) $(a+b)(a-b)$; 6) $(m+n):(m-n)$ та $\\frac{m+n}{m-n}$</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Дидактичне розрізнення понять</div>
      Найважливіший акцент 7 класу — відчувати різницю між <em>сумою квадратів</em> $x^2 + y^2$ (головна дія — додавання) та <em>квадратом суми</em> $(x+y)^2$ (головна дія — піднесення до квадрата).
    </div>
  </div>
</div>

<!-- Задача 20 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">20.</div>
    <div class="problem-text"><strong>Умова:</strong> Словесно сформулювати закони: 1) $ab=ba$; 2) $(x+y)z=xz+yz$; 3) $(a+b)(a-b)=a^2-b^2$; 4) $\\frac{a}{b}=\\frac{am}{bm}$; 5) $\\frac{a}{m}+\\frac{b}{m}=\\frac{a+b}{m}$; 6) $(ab)^2=a^2b^2$.</div>
  </div>
  <div class="sol-container">
    <div class="pedagogy-details" style="background:#ffffff; border:none; padding:0;">
      <p><strong>1) Переставний закон множення (комутативність):</strong> від зміни порядку співмножників добуток не змінюється.</p>
      <p><strong>2) Розподільний закон множення відносно додавання (дистрибутивність):</strong> щоб помножити суму на число, можна помножити на це число кожний доданок окремо й одержані результати додати.</p>
      <p><strong>3) Формула скороченого множення (різниця квадратів):</strong> добуток суми двох чисел на їхню різницю дорівнює різниці квадратів цих чисел.</p>
      <p><strong>4) Основна властивість дробу (частки):</strong> якщо чисельник і знаменник дробу помножити на одне й те саме відмінне від нуля число, то значення дробу не зміниться.</p>
      <p><strong>5) Правило додавання дробів з однаковими знаменниками:</strong> щоб додати дроби з однаковими знаменниками, додають їхні чисельники, а знаменник залишають без змін.</p>
      <p><strong>6) Піднесення добутку до степеня:</strong> щоб піднести добуток до квадрата (степеня), можна піднести до цього степеня кожен співмножник окремо й результати перемножити.</p>
    </div>
  </div>
</div>

<!-- Задача 21 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">21.</div>
    <div class="problem-text"><strong>Умова:</strong> Обчислити вирази при $a = 20, b = 8, c = 3$.</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">1) 84; 2) 44; 3) 552; 4) 336; 5) $9\\frac{1}{3}$; 6) $2\\frac{6}{11}$; 7) 464; 8) 784; 9) 912</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Покрокові розрахунки для всіх 9 пунктів</div>
      <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 4px 16px;">
        <div><strong>1)</strong> $(20 + 8) \\cdot 3 = 28 \\cdot 3 = \\mathbf{84}$</div>
        <div><strong>2)</strong> $20 + 8 \\cdot 3 = 20 + 24 = \\mathbf{44}$</div>
        <div><strong>3)</strong> $(20 + 8) \\cdot 20 - 8 = 28 \\cdot 20 - 8 = 560 - 8 = \\mathbf{552}$</div>
        <div><strong>4)</strong> $(20 + 8)(20 - 8) = 28 \\cdot 12 = \\mathbf{336}$</div>
        <div><strong>5)</strong> $(20 + 8) : 3 = 28 : 3 = \\frac{28}{3} = \\mathbf{9\\frac{1}{3}}$</div>
        <div><strong>6)</strong> $\\frac{20 + 8}{8 + 3} = \\frac{28}{11} = \\mathbf{2\\frac{6}{11}}$</div>
        <div><strong>7)</strong> $20^2 + 8^2 = 400 + 64 = \\mathbf{464}$</div>
        <div><strong>8)</strong> $(20 + 8)^2 = 28^2 = \\mathbf{784}$</div>
        <div><strong>9)</strong> $20^2 + 8^3 = 400 + 512 = \\mathbf{912}$</div>
      </div>
      <div style="margin-top:6px; font-size:11.5px; color:#64748b;"><em>Примітка:</em> у виданні 1931 р. пункт 8 був помилково пронумерований другою цифрою 7.</div>
    </div>
  </div>
</div>

<!-- Задача 22 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">22.</div>
    <div class="problem-text"><strong>Умова:</strong> Перевірити числові рівності при $a = 10, b = 2$.</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">Без ответа (самостійна перевірка учнем)</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Повний розбір</span></span>
      <span class="sol-meta-val">Усі 3 тотожності перевірено — рівності виконуються</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Покрокова числова підстановка</div>
      <p><strong>1)</strong> Ліва частина: $(10 + 2)^2 = 12^2 = 144$. Права: $10^2 + 2 \\cdot 10 \\cdot 2 + 2^2 = 100 + 40 + 4 = 144$. Оскільки $144 = 144$, рівність істинна.</p>
      <p><strong>2)</strong> Ліва частина: $(10 - 2)^2 = 8^2 = 64$. Права: $10^2 - 2 \\cdot 10 \\cdot 2 + 2^2 = 100 - 40 + 4 = 64$. Оскільки $64 = 64$, рівність істинна.</p>
      <p><strong>3)</strong> Ліва частина: $(10 + 2)(10 - 2) = 12 \\cdot 8 = 96$. Права: $10^2 - 2^2 = 100 - 4 = 96$. Оскільки $96 = 96$, рівність істинна.</p>
    </div>
  </div>
</div>

<!-- Задача 23 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">23.</div>
    <div class="problem-text"><strong>Умова:</strong> Обчислити вирази при $x = 100, y = 20$: 1) $x - \\{y + [x + y - (x - y)] + 2\\}$; 2) $xy + [x^2 - (x - y)^2]$.</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">1) 42 <span class="badge-tag badge-warn" style="font-size:10px;">історична помилка знака</span>; 2) 5600</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Точний розрахунок</span></span>
      <span class="sol-meta-val">1) $\\mathbf{38}$; 2) $\\mathbf{5600}$</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Детальний розбір помилки знака в 1931 році</div>
      <p><strong>Пункт 1:</strong> Розкриваємо дужки зсередини:<br>
      • Внутрішні круглі дужки: $x - y = 100 - 20 = 80$.<br>
      • Квадратні дужки: $x + y - (x - y) = 100 + 20 - 80 = 40$ (або тотожно $x + y - x + y = 2y = 40$).<br>
      • Фігурні дужки: $y + 40 + 2 = 20 + 40 + 2 = 62$.<br>
      • Весь вираз: $x - 62 = 100 - 62 = \\mathbf{38}$.<br>
      <em>Чому в збірнику надруковано 42?</em> Якщо учень (чи складач) помилково розкриває знак «мінус» перед фігурними дужками і не змінює знак біля двійки: $100 - 60 + 2 = 42$. Це еталонна помилка на розкриття дужок!</p>
      <p><strong>Пункт 2:</strong> $x = 100, y = 20$.<br>
      • $xy = 100 \\cdot 20 = 2000$.<br>
      • $(x - y)^2 = 80^2 = 6400$.<br>
      • $x^2 - (x - y)^2 = 10000 - 6400 = 3600$.<br>
      • Разом: $2000 + 3600 = \\mathbf{5600}$.</p>
    </div>
  </div>
</div>

<!-- Задача 24 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">24.</div>
    <div class="problem-text"><strong>Умова:</strong> Формула суми $S_n = 1 + 2 + \\dots + n = \\frac{1}{2}n(n+1)$. Перевірити для $n = 2, 3, 4$ та знайти $S_{100}$.</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">Сумма сотни первых натуральных чисел равна 5050</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Повний розбір</span></span>
      <span class="sol-meta-val">Для $n=2$: 3; для $n=3$: 6; для $n=4$: 10; для $n=100$: $\\mathbf{5050}$</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Покрокове обчислення (метод Гаусса)</div>
      • При $n = 2$: $1 + 2 = 3$; за формулою: $\\frac{1}{2} \\cdot 2 \\cdot 3 = 3$ (вірно).<br>
      • При $n = 3$: $1 + 2 + 3 = 6$; за формулою: $\\frac{1}{2} \\cdot 3 \\cdot 4 = 6$ (вірно).<br>
      • При $n = 4$: $1 + 2 + 3 + 4 = 10$; за формулою: $\\frac{1}{2} \\cdot 4 \\cdot 5 = 10$ (вірно).<br>
      • При $n = 100$: $S_{100} = \\frac{1}{2} \\cdot 100 \\cdot 101 = 50 \\cdot 101 = \\mathbf{5050}$.
    </div>
  </div>
</div>

<!-- Задача 25 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">25.</div>
    <div class="problem-text"><strong>Умова:</strong> Сума квадратів $S_2(n) = \\frac{1}{6}n(n+1)(2n+1)$. Перевірити для $n = 2, 3, 4$ та знайти суму до $10^2$.</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">$1^2 + 2^2 + 3^2 + \\dots + 10^2 = 385$</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Повний розбір</span></span>
      <span class="sol-meta-val">Для $n=2$: 5; для $n=3$: 14; для $n=4$: 30; для $n=10$: $\\mathbf{385}$</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Покрокове обчислення</div>
      • При $n = 2$: $1^2 + 2^2 = 1 + 4 = 5$; за формулою: $\\frac{1}{6} \\cdot 2 \\cdot 3 \\cdot 5 = \\frac{30}{6} = 5$.<br>
      • При $n = 3$: $1 + 4 + 9 = 14$; за формулою: $\\frac{1}{6} \\cdot 3 \\cdot 4 \\cdot 7 = \\frac{84}{6} = 14$.<br>
      • При $n = 4$: $1 + 4 + 9 + 16 = 30$; за формулою: $\\frac{1}{6} \\cdot 4 \\cdot 5 \\cdot 9 = \\frac{180}{6} = 30$.<br>
      • При $n = 10$: $S_2(10) = \\frac{1}{6} \\cdot 10 \\cdot 11 \\cdot 21 = \\frac{2310}{6} = \\mathbf{385}$.
    </div>
  </div>
</div>

<!-- Задача 26 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">26.</div>
    <div class="problem-text"><strong>Умова:</strong> Сума кубів $S_3(n) = \\frac{1}{4}n^2(n+1)^2$. Перевірити для $n = 1, 2, 3, 4$ та знайти суму до $100^3$.</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">$1^3 + 2^3 + 3^3 + \\dots + 100^3 = 25\\,502\\,500$</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Повний розбір</span></span>
      <span class="sol-meta-val">Для $n=1$: 1; $n=2$: 9; $n=3$: 36; $n=4$: 100; для $n=100$: $\\mathbf{25\\,502\\,500}$</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Магічний зв'язок: теорема Нікомаха</div>
      Зверніть увагу: $\\frac{1}{4}n^2(n+1)^2 = \\left[\\frac{1}{2}n(n+1)\\right]^2 = (S_1(n))^2$. Сума кубів перших $n$ чисел завжди дорівнює квадрату їхньої звичайної суми!<br>
      • $1^3 = 1 = 1^2$;<br>
      • $1^3 + 2^3 = 9 = 3^2 = (1+2)^2$;<br>
      • $1^3 + 2^3 + 3^3 = 36 = 6^2 = (1+2+3)^2$;<br>
      • $1^3 + 2^3 + 3^3 + 4^3 = 100 = 10^2 = (1+2+3+4)^2$;<br>
      • Для $n = 100$: $S_3(100) = (S_1(100))^2 = 5050^2 = \\mathbf{25\\,502\\,500}$.
    </div>
  </div>
</div>

<!-- Задача 27 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">27.</div>
    <div class="problem-text"><strong>Умова:</strong> У виразі $3ab$ підставити замість $a$ суму $x + y$, а замість $b$ — різницю $x - y$.</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">$3(x + y)(x - y)$</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Сучасний запис</span></span>
      <span class="sol-meta-val">$3(x + y)(x - y) = 3(x^2 - y^2) = 3x^2 - 3y^2$</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Покрокове обґрунтування</div>
      Підставляємо складені вирази в дужках: $3 \\cdot (x + y) \\cdot (x - y) = 3(x + y)(x - y)$. Розкривши різницю квадратів: $3(x^2 - y^2) = 3x^2 - 3y^2$.
    </div>
  </div>
</div>

<!-- Задача 28 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">28.</div>
    <div class="problem-text"><strong>Умова:</strong> У вираз $2m + 3n$ підставити замість $m$ добуток $ab$, а замість $n$ — різницю $a - b$.</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">$2(ab) + 3(a - b)$</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Сучасний запис</span></span>
      <span class="sol-meta-val">$2ab + 3(a - b) \\quad \\text{або} \\quad 2ab + 3a - 3b$</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Покрокове обґрунтування</div>
      Замінюючи $m$ на $ab$ та $n$ на $(a - b)$, отримуємо $2(ab) + 3(a - b) = 2ab + 3(a - b)$. Після розкриття дужок за дистрибутивним законом: $2ab + 3a - 3b$.
    </div>
  </div>
</div>

<!-- Задача 29 -->
<div class="problem-card">
  <div class="problem-header">
    <div class="problem-num">29.</div>
    <div class="problem-text"><strong>Умова:</strong> У вираз $\\frac{1}{2}n(n + 1)$ підставити замість $n$ суму $k + 1$.</div>
  </div>
  <div class="sol-container">
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-orig">Оригінал (1931)</span></span>
      <span class="sol-meta-val">$\\frac{1}{2}(k + 1)(k + 1 + 1)$</span>
    </div>
    <div class="sol-meta-row">
      <span class="sol-meta-label"><span class="badge-tag badge-sympy">Сучасний запис</span></span>
      <span class="sol-meta-val">$\\frac{1}{2}(k + 1)(k + 2)$</span>
    </div>
    <div class="pedagogy-details">
      <div class="pedagogy-title">Покрокове обґрунтування та зв'язок з математичною індукцією</div>
      Підставляємо $(k + 1)$ замість $n$: перший множник стає $(k + 1)$, другий множник $(n + 1)$ стає $((k + 1) + 1) = (k + 2)$.<br>
      Отримуємо: $\\frac{1}{2}(k + 1)(k + 2)$.<br>
      <em>Педагогічне значення:</em> це класичний крок індукційного переходу $k \\to k+1$ для формули суми перших натуральних чисел!
    </div>
  </div>
</div>
"""
    return HTML_SHELL.format(title="А. П. Кисельов — Відповіді та розв'язання (1–29)", body=body)


def main():
    print("Generating HTML files...")
    problems_html = generate_problems_html()
    answers_html = generate_answers_html()

    prob_html_file = os.path.join(SCRATCH_DIR, "zadachi_1_29.html")
    ans_html_file = os.path.join(SCRATCH_DIR, "vidpovidi_1_29.html")

    with open(prob_html_file, "w", encoding="utf-8") as f:
        f.write(problems_html)

    with open(ans_html_file, "w", encoding="utf-8") as f:
        f.write(answers_html)

    # Output paths: both in project root and in data/
    prob_pdf_root = os.path.join(PROJECT_ROOT, "zadachi_1_29_ukr.pdf")
    ans_pdf_root = os.path.join(PROJECT_ROOT, "vidpovidi_1_29_ukr.pdf")
    prob_pdf_data = os.path.join(DATA_DIR, "zadachi_1_29_ukr.pdf")
    ans_pdf_data = os.path.join(DATA_DIR, "vidpovidi_1_29_ukr.pdf")

    print("Compiling Problems PDF via Chrome headless...")
    cmd1 = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--virtual-time-budget=4000",
        "--no-pdf-header-footer",
        f"--print-to-pdf={prob_pdf_root}",
        prob_html_file,
    ]
    subprocess.run(cmd1, check=True)

    print("Compiling Answers PDF via Chrome headless...")
    cmd2 = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--virtual-time-budget=4000",
        "--no-pdf-header-footer",
        f"--print-to-pdf={ans_pdf_root}",
        ans_html_file,
    ]
    subprocess.run(cmd2, check=True)

    # Copy to data/ folder as well
    import shutil

    shutil.copyfile(prob_pdf_root, prob_pdf_data)
    shutil.copyfile(ans_pdf_root, ans_pdf_data)

    print(f"Problems PDF generated: {prob_pdf_root} ({os.path.getsize(prob_pdf_root)} bytes)")
    print(f"Answers PDF generated: {ans_pdf_root} ({os.path.getsize(ans_pdf_root)} bytes)")

    # Render pages to PNG to inspect
    pdf1 = pdfium.PdfDocument(prob_pdf_root)
    print(f"Problems PDF page count: {len(pdf1)}")
    for i in range(len(pdf1)):
        img = pdf1[i].render(scale=2).to_pil()
        out_img = os.path.join(SCRATCH_DIR, f"zadachi_page_{i + 1}.png")
        img.save(out_img)
        print(f"Rendered {out_img}")

    pdf2 = pdfium.PdfDocument(ans_pdf_root)
    print(f"Answers PDF page count: {len(pdf2)}")
    for i in range(min(5, len(pdf2))):
        img = pdf2[i].render(scale=2).to_pil()
        out_img = os.path.join(SCRATCH_DIR, f"vidpovidi_page_{i + 1}.png")
        img.save(out_img)
        print(f"Rendered {out_img}")


if __name__ == "__main__":
    main()
