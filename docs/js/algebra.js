/**
 * Algebra Interactive Socratic Solver (Problems 1–29)
 * Based on A. P. Kiselev (1931) aligned with Merzlyak Grade 7
 */

const PROBLEMS_DATA = [
  {
    id: 1,
    title: "Периметр і площа квадрата",
    text: "Сторона квадрата дорівнює $a\\text{ м}$. Виразіть його периметр ($P$), а потім його площу ($S$). Введіть формулу площі або периметра (наприклад, $4a$ або $a^2$):",
    accepted: ["4a", "4*a", "a^2", "a**2", "4a; a^2", "4a, a^2", "p=4a, s=a^2"],
    hint1: "Подумайте: скільки сторін має квадрат і як обчислити площу прямокутної фігури?",
    hint2: "Периметр — це сума чотирьох сторін ($a+a+a+a$). Площа — добуток довжини на ширину ($a \\cdot a$).",
    hint3: "Периметр: $P = 4a\\text{ м}$. Площа: $S = a^2\\text{ м}^2$."
  },
  {
    id: 2,
    title: "Повна поверхня та об'єм куба",
    text: "Якщо ребро куба дорівнює $m\\text{ см}$, як виразити площу його повної поверхні та його об'єм?",
    accepted: ["6m^2", "6*m^2", "m^3", "6m^2; m^3", "6m^2, m^3"],
    hint1: "Скільки однакових квадратних граней має куб? Яка площа однієї грані?",
    hint2: "Площа однієї грані $m^2$. Всього граней 6. Об'єм — добуток трьох вимірів: $m \\cdot m \\cdot m$.",
    hint3: "Площа повної поверхні: $S_{\\text{повн}} = 6m^2\\text{ см}^2$. Об'єм: $V = m^3\\text{ см}^3$."
  },
  {
    id: 3,
    title: "Площа прямокутника зі зменшеною висотою",
    text: "У прямокутника основа дорівнює $x\\text{ м}$, а висота на $d\\text{ м}$ менша від основи. Виразіть його площу:",
    accepted: ["x(x-d)", "x*(x-d)", "x^2-xd", "x^2-dx", "x^2 - xd"],
    hint1: "Спочатку знайдіть висоту прямокутника, віднявши $d$ від основи $x$.",
    hint2: "Висота дорівнює $(x - d)$. Площа — основа помножена на висоту.",
    hint3: "$S = x(x - d) = x^2 - xd\\text{ (м}^2\\text{)}$."
  },
  {
    id: 4,
    title: "Куб зі складеним ребром",
    text: "Ребро куба дорівнює $(m + n)$. Виразіть площу його повної поверхні та об'єм:",
    accepted: ["6(m+n)^2", "6*(m+n)^2", "(m+n)^3", "6(m+n)^2, (m+n)^3"],
    hint1: "Не забудьте взяти ребро в дужки перед піднесенням до степеня!",
    hint2: "Площа однієї грані: $(m + n)^2$. Повна поверхня — це 6 таких граней. Об'єм — ребро в кубі.",
    hint3: "$S_{\\text{повн}} = 6(m + n)^2$, $V = (m + n)^3$."
  },
  {
    id: 5,
    title: "Площа прямокутника (різниця квадратів)",
    text: "Основа прямокутника $2a + b$, а висота $2a - b$. Виразіть площу цього прямокутника:",
    accepted: ["(2a+b)(2a-b)", "(2a + b)(2a - b)", "4a^2-b^2", "4a^2 - b^2"],
    hint1: "Помножте основу на висоту у вигляді добутку двох дужок.",
    hint2: "Це формула різниці квадратів: $(x+y)(x-y) = x^2 - y^2$, де $x = 2a$, $y = b$.",
    hint3: "$S = (2a + b)(2a - b) = (2a)^2 - b^2 = 4a^2 - b^2$."
  },
  {
    id: 6,
    title: "Виміри паралелепіпеда",
    text: "Висота паралелепіпеда $h$, а сторони прямокутної основи $b$ і $c$. Як виразити об'єм ($V$)?",
    accepted: ["bch", "b*c*h", "hbc", "cbh"],
    hint1: "Об'єм прямокутного паралелепіпеда дорівнює добутку трьох його вимірів.",
    hint2: "Перемножте довжину, ширину основи та висоту: $b \\cdot c \\cdot h$.",
    hint3: "$V = bch$ (або $V = S_{\\text{осн}} \\cdot h = bc \\cdot h$)."
  },
  {
    id: 7,
    title: "Алгебраїчний вік",
    text: "Якщо мій вік зараз становить $a$ років, то скільки років мені буде через 5 років?",
    accepted: ["a+5", "a + 5", "5+a"],
    hint1: "З плином часу вік збільшується чи зменшується?",
    hint2: "До поточного віку $a$ додаємо 5 років.",
    hint3: "Через 5 років: $a + 5$. (5 років тому було $a - 5$)."
  },
  {
    id: 8,
    title: "Складене іменоване число (метрична система)",
    text: "Запишіть вираз: скільки грамів міститься у $a\\text{ кг } b\\text{ дг}$ (у підручнику 1931 р. «дг» = декаграм $= 10\\text{ г}$):",
    accepted: ["1000a+10b", "1000a + 10b", "1000*a+10*b"],
    hint1: "Скільки грамів в $1\\text{ кг}$? А в одному декаграмі ($10\\text{ г}$)?",
    hint2: "$1\\text{ кг} = 1000\\text{ г} \\implies 1000a\\text{ г}$. $1\\text{ дг} = 10\\text{ г} \\implies 10b\\text{ г}$.",
    hint3: "Разом: $1000a + 10b\\text{ (г)}$."
  },
  {
    id: 9,
    title: "Лінійний тариф телеграми",
    text: "Базовий тариф $a\\text{ коп.}$, кожне окреме слово коштує $b\\text{ коп.}$ Яка вартість телеграми з $x$ слів?",
    accepted: ["a+bx", "a + bx", "bx+a", "a+b*x"],
    hint1: "Це формула лінійної залежності: постійна плата + плата за кожне слово.",
    hint2: "За $x$ слів сплачують $b \\cdot x$. До цього додається фіксована такса $a$.",
    hint3: "Загальна вартість: $a + bx\\text{ (коп.)}$."
  },
  {
    id: 10,
    title: "Одиниці в десятках",
    text: "Скільки простих одиниць міститься в $x$ десятках?",
    accepted: ["10x", "10*x"],
    hint1: "В одному десятку 10 одиниць. А у двох? А в $x$?",
    hint2: "Помножте кількість десятків $x$ на 10.",
    hint3: "$10 \\cdot x = 10x$ одиниць."
  },
  {
    id: 11,
    title: "Десятковий запис двоцифрового числа",
    text: "Двоцифрове число містить $x$ десятків та $y$ одиниць. Скільки всього одиниць у числі?",
    accepted: ["10x+y", "10x + y", "10*x+y"],
    hint1: "Згадайте: $x$ десятків дають $10x$ одиниць. Скільки ще одиниць треба додати?",
    hint2: "Десятки перетворюємо в одиниці: $10x$, і додаємо прості одиниці $y$.",
    hint3: "$\\overline{xy} = 10x + y$."
  },
  {
    id: 12,
    title: "Десятковий запис трицифрового числа",
    text: "Трицифрове число містить $a$ сотень, $b$ десятків і $c$ одиниць. Запишіть формулу:",
    accepted: ["100a+10b+c", "100a + 10b + c", "100*a+10*b+c"],
    hint1: "Кожна сотня — це 100 одиниць, кожен десяток — 10.",
    hint2: "Додайте сотні ($100a$), десятки ($10b$) та одиниці ($c$).",
    hint3: "$\\overline{abc} = 100a + 10b + c$."
  },
  {
    id: 13,
    title: "Число, кратне 7",
    text: "Як записати у загальному вигляді число, кратне 7 (через ціле число $k$ або $a$)?",
    accepted: ["7k", "7a", "7n", "7*k", "7*a"],
    hint1: "Будь-яке число, що ділиться на 7, можна записати як 7 помножити на ціле число.",
    hint2: "Використайте множник 7 біля змінної: $7k$.",
    hint3: "$7k$, де $k \\in \\mathbb{Z}$ (ціле число)."
  },
  {
    id: 14,
    title: "Парні та непарні числа",
    text: "Якщо $k$ — ціле число, яким є число $2k$ — парним чи непарним?",
    accepted: ["парне", "парним", "четное", "parne"],
    hint1: "Чи ділиться число $2k$ на 2 без остачі?",
    hint2: "Оскільки вираз містить множник 2, він завжди ділиться навпіл.",
    hint3: "$2k$ — завжди **парне** число. А $2k+1$ та $2k-1$ — непарні."
  },
  {
    id: 15,
    title: "Ділення з остачею",
    text: "Число при діленні на 5 дає остачу 2. Запишіть це число у вигляді формули через неповну частку $n$ (або $a$):",
    accepted: ["5n+2", "5n + 2", "5a+2", "5a + 2", "5k+2", "5*n+2"],
    hint1: "Теорема про ділення з остачею: Ділене = Дільник × Неповна частка + Остача.",
    hint2: "Дільник дорівнює 5, остача 2. Помножте 5 на змінну $n$ і додайте 2.",
    hint3: "$N = 5n + 2$, де $n \\in \\mathbb{Z}$."
  },
  {
    id: 16,
    title: "Середня вартість чаю",
    text: "Змішали $a\\text{ кг}$ чаю по $m\\text{ грн}$ і $b\\text{ кг}$ по $n\\text{ грн}$. Запишіть формулу вартості 1 кг суміші:",
    accepted: ["(am+bn)/(a+b)", "(ma+nb)/(a+b)", "(am+bn)/(b+a)"],
    hint1: "Знайдіть загальну вартість усього чаю і поділіть на загальну масу суміші.",
    hint2: "Загальна вартість: $am + bn$. Загальна маса: $a + b$.",
    hint3: "Ціна 1 кг = $\\frac{am + bn}{a + b}\\text{ грн/кг}$."
  },
  {
    id: 17,
    title: "Рівність у коробках",
    text: "У першій коробці $m$ предметів, у другій $n$. Якщо з 1-ї в 2-гу перекласти $p$, стане порівну. Запишіть рівність:",
    accepted: ["m-p=n+p", "m - p = n + p", "n+p=m-p"],
    hint1: "Скільки залишиться в першій коробці? Скільки стане в другій коробці?",
    hint2: "У першій стане $(m - p)$, у другій $(n + p)$. Прирівняйте їх.",
    hint3: "$m - p = n + p$."
  },
  {
    id: 18,
    title: "Нерівність суми цифр",
    text: "Запишіть нерівність: сума цифр ($a+b$) двоцифрового числа менша від самого числа ($10a+b$):",
    accepted: ["a+b<10a+b", "a + b < 10a + b", "10a+b>a+b"],
    hint1: "Використайте знак «<» між сумою цифр та розгорнутим записом числа.",
    hint2: "Ліворуч запишіть $a + b$, праворуч $10a + b$.",
    hint3: "$a + b < 10a + b$ (оскільки $9a > 0$ для будь-якої першої цифри $a \\ge 1$)."
  },
  {
    id: 19,
    title: "Сума квадратів чи квадрат суми?",
    text: "Запишіть алгебраїчними знаками: квадрат суми чисел $x$ і $y$:",
    accepted: ["(x+y)^2", "(x + y)^2", "(x+y)**2"],
    hint1: "Головна дія — піднесення до квадрата всієї суми!",
    hint2: "Візьміть суму $(x + y)$ у дужки та піднесіть до квадрата.",
    hint3: "$(x + y)^2$. (Зверніть увагу: сума квадратів була б $x^2 + y^2$)."
  },
  {
    id: 20,
    title: "Розподільний закон",
    text: "Як називається закон, що виражається формулою $(x + y)z = xz + yz$?",
    accepted: ["розподільний", "дистрибутивність", "дистрибутивний", "розподільчий", "розподільний закон"],
    hint1: "Цей закон показує, як множення «розподіляється» на кожен доданок.",
    hint2: "Українською це «розподільний» закон, латинською — «дистрибутивність».",
    hint3: "**Розподільний закон множення відносно додавання (дистрибутивність)**."
  },
  {
    id: 21,
    title: "Обчислення виразів",
    text: "Обчисліть значення виразу $(a + b)c$ при $a = 20, b = 8, c = 3$:",
    accepted: ["84"],
    hint1: "Спочатку виконайте дію в дужках: $20 + 8$. Потім помножте результат на 3.",
    hint2: "$28 \\cdot 3 = 84$.",
    hint3: "$(20 + 8) \\cdot 3 = 28 \\cdot 3 = \\mathbf{84}$."
  },
  {
    id: 22,
    title: "Числова перевірка тотожності",
    text: "Обчисліть $(a + b)(a - b)$ при $a = 10, b = 2$:",
    accepted: ["96"],
    hint1: "Можна порахувати як $(10 + 2)(10 - 2)$ або за формулою різниці квадратів $10^2 - 2^2$.",
    hint2: "$12 \\cdot 8 = 96$ або $100 - 4 = 96$.",
    hint3: "$(10+2)(10-2) = 12 \\cdot 8 = 100 - 4 = \\mathbf{96}$."
  },
  {
    id: 23,
    title: "Багаторівневі дужки (історична задача)",
    text: "Обчисліть точне значення виразу $x - \\{y + [x + y - (x - y)] + 2\\}$ при $x = 100, y = 20$:",
    accepted: ["38"],
    hint1: "Розкрийте внутрішні дужки: $x + y - (x - y) = 2y = 40$. Потім обчисліть вираз у фігурних дужках.",
    hint2: "У фігурних дужках: $20 + 40 + 2 = 62$. Відніміть це число від 100.",
    hint3: "$100 - 62 = \\mathbf{38}$. (У виданні 1931 р. була помилка зі знаком, що давала 42)."
  },
  {
    id: 24,
    title: "Сума чисел першої сотні (метод Гаусса)",
    text: "Знайдіть суму перших 100 натуральних чисел ($1 + 2 + \\dots + 100$) за формулою $S = \\frac{1}{2}n(n+1)$:",
    accepted: ["5050"],
    hint1: "Підставте $n = 100$ у формулу: $\\frac{1}{2} \\cdot 100 \\cdot 101$.",
    hint2: "$50 \\cdot 101 = 5050$.",
    hint3: "$S_{100} = \\frac{100 \\cdot 101}{2} = 50 \\cdot 101 = \\mathbf{5050}$."
  },
  {
    id: 25,
    title: "Сума десяти квадратів",
    text: "Знайдіть $1^2 + 2^2 + \\dots + 10^2$ за формулою $\\frac{1}{6}n(n+1)(2n+1)$ для $n = 10$:",
    accepted: ["385"],
    hint1: "Підставте $n = 10$: $\\frac{1}{6} \\cdot 10 \\cdot 11 \\cdot 21$.",
    hint2: "Скоротіть 6 і 21 на 3, а потім 10 і 2 на 2: $5 \\cdot 11 \\cdot 7$.",
    hint3: "$55 \\cdot 7 = \\mathbf{385}$."
  },
  {
    id: 26,
    title: "Сума кубів першої сотні (теорема Нікомаха)",
    text: "Сума кубів дорівнює квадрату звичайної суми: $S_3(100) = (S_1(100))^2 = 5050^2$. Чому вона дорівнює?",
    accepted: ["25502500", "25 502 500", "25,502,500"],
    hint1: "Піднесіть число 5050 до квадрата ($5050 \\times 5050$).",
    hint2: "$505 \\times 505 = 255025$. Додайте два нулі в кінці.",
    hint3: "$5050^2 = \\mathbf{25\\,502\\,500}$."
  },
  {
    id: 27,
    title: "Підстановка виразів у добуток",
    text: "У виразі $3ab$ підставте $a = x+y$, а $b = x-y$. Який вираз утвориться?",
    accepted: ["3(x+y)(x-y)", "3(x^2-y^2)", "3x^2-3y^2", "3*(x+y)*(x-y)"],
    hint1: "Просто замініть $a$ на $(x+y)$ та $b$ на $(x-y)$.",
    hint2: "Вийде $3(x + y)(x - y)$. Розкривши різницю квадратів: $3(x^2 - y^2)$.",
    hint3: "$3(x + y)(x - y) = 3(x^2 - y^2) = 3x^2 - 3y^2$."
  },
  {
    id: 28,
    title: "Підстановка у лінійний вираз",
    text: "У вираз $2m + 3n$ підставте $m = ab$ та $n = a - b$:",
    accepted: ["2ab+3(a-b)", "2ab + 3(a - b)", "2ab+3a-3b", "2ab + 3a - 3b"],
    hint1: "Замініть $m$ на $ab$, а $n$ візьміть у дужки: $(a - b)$.",
    hint2: "$2(ab) + 3(a - b)$. Можна також розкрити дужки: $2ab + 3a - 3b$.",
    hint3: "$2ab + 3(a - b) = 2ab + 3a - 3b$."
  },
  {
    id: 29,
    title: "Крок індукції для суми чисел",
    text: "У вираз $\\frac{1}{2}n(n+1)$ підставте $n = k+1$. Який вираз утвориться?",
    accepted: ["1/2(k+1)(k+2)", "1/2*(k+1)*(k+2)", "(k+1)(k+2)/2", "0.5(k+1)(k+2)"],
    hint1: "Перший множник $n$ стане $(k+1)$. А що станеться з $(n+1)$?",
    hint2: "$(n+1)$ перетвориться на $((k+1)+1) = (k+2)$.",
    hint3: "$\\frac{1}{2}(k + 1)(k + 2)$."
  }
];

// State
let currentProbIndex = 0;
let solvedProblems = JSON.parse(localStorage.getItem("kiselev_solved_algebra") || "[]");

function initSolver() {
  renderSelector();
  loadProblem(currentProbIndex);
  updateStats();
}

function renderSelector() {
  const container = document.getElementById("prob-selector");
  if (!container) return;
  container.innerHTML = "";
  
  PROBLEMS_DATA.forEach((prob, idx) => {
    const btn = document.createElement("button");
    btn.className = "prob-btn";
    btn.textContent = prob.id;
    if (idx === currentProbIndex) btn.classList.add("active");
    if (solvedProblems.includes(prob.id)) btn.classList.add("solved");
    btn.onclick = () => loadProblem(idx);
    container.appendChild(btn);
  });
}

function loadProblem(index) {
  currentProbIndex = index;
  const prob = PROBLEMS_DATA[index];
  
  document.getElementById("prob-badge").textContent = `Задача ${prob.id} з 29`;
  document.getElementById("prob-title").textContent = prob.title;
  document.getElementById("prob-statement").innerHTML = prob.text;
  
  // Clear input & feedback
  const input = document.getElementById("ans-input");
  input.value = "";
  input.focus();
  
  const fb = document.getElementById("feedback-box");
  fb.style.display = "none";
  fb.className = "feedback-box";
  
  // Setup hints
  document.getElementById("hint-1-text").innerHTML = prob.hint1;
  document.getElementById("hint-2-text").innerHTML = prob.hint2;
  document.getElementById("hint-3-text").innerHTML = prob.hint3;
  
  // Hide hint bodies
  for (let s = 1; s <= 3; s++) {
    document.getElementById(`hint-body-${s}`).style.display = "none";
  }
  
  renderSelector();
  
  // Re-render KaTeX in dynamically inserted elements
  if (window.renderMathInElement) {
    renderMathInElement(document.getElementById("problem-view-area"), {
      delimiters: [
        {left: '$$', right: '$$', display: true},
        {left: '$', right: '$', display: false}
      ],
      throwOnError: false
    });
  }
}

function checkCurrentAnswer() {
  const prob = PROBLEMS_DATA[currentProbIndex];
  const input = document.getElementById("ans-input");
  const userRaw = input.value.trim().toLowerCase().replace(/\\s+/g, "");
  const fb = document.getElementById("feedback-box");
  
  if (!userRaw) {
    fb.textContent = "Будь ласка, введіть вашу відповідь.";
    fb.className = "feedback-box feedback-error";
    fb.style.display = "block";
    return;
  }
  
  const isCorrect = prob.accepted.some(acc => {
    const accNorm = acc.toLowerCase().replace(/\\s+/g, "");
    return userRaw === accNorm;
  });
  
  if (isCorrect) {
    fb.innerHTML = "🎉 <strong>Чудово! Відповідь абсолютно правильна!</strong>";
    fb.className = "feedback-box feedback-success";
    fb.style.display = "block";
    
    if (!solvedProblems.includes(prob.id)) {
      solvedProblems.push(prob.id);
      localStorage.setItem("kiselev_solved_algebra", JSON.stringify(solvedProblems));
      renderSelector();
      updateStats();
    }
  } else {
    fb.innerHTML = "🤔 <strong>Спробуйте ще раз!</strong> Якщо виникли труднощі, скористайтеся підказками нижче.";
    fb.className = "feedback-box feedback-error";
    fb.style.display = "block";
    
    // Automatically reveal Hint 1 on mistake
    document.getElementById("hint-body-1").style.display = "block";
  }
}

function toggleHint(step) {
  const el = document.getElementById(`hint-body-${step}`);
  el.style.display = el.style.display === "block" ? "none" : "block";
}

function nextProblem() {
  if (currentProbIndex < PROBLEMS_DATA.length - 1) {
    loadProblem(currentProbIndex + 1);
  }
}

function prevProblem() {
  if (currentProbIndex > 0) {
    loadProblem(currentProbIndex - 1);
  }
}

function updateStats() {
  const statEl = document.getElementById("solved-count");
  if (statEl) {
    statEl.textContent = `${solvedProblems.length} / 29`;
  }
}

window.addEventListener("DOMContentLoaded", initSolver);
