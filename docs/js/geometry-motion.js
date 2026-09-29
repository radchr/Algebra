(() => {
  "use strict";

  const NS = "http://www.w3.org/2000/svg";
  const stage = document.getElementById("motion-stage");
  const slider = document.getElementById("motion-slider");
  const valueBox = document.getElementById("motion-value");
  const playButton = document.getElementById("motion-play");
  const demo = document.body.dataset.demo;

  if (!stage || !slider || !demo) return;

  const make = (name, attrs = {}, text = "") => {
    const node = document.createElementNS(NS, name);
    Object.entries(attrs).forEach(([key, value]) => node.setAttribute(key, value));
    if (text) node.textContent = text;
    stage.appendChild(node);
    return node;
  };

  const pointAt = (cx, cy, radius, degrees) => {
    const radians = (degrees * Math.PI) / 180;
    return [cx + radius * Math.cos(radians), cy - radius * Math.sin(radians)];
  };

  const line = (x1, y1, x2, y2, className = "svg-line") =>
    make("line", { x1, y1, x2, y2, class: className });

  const ray = (cx, cy, degrees, radius = 165, className = "svg-line") => {
    const [x, y] = pointAt(cx, cy, radius, degrees);
    return line(cx, cy, x, y, className);
  };

  const label = (x, y, text, className = "svg-label", anchor = "middle") =>
    make("text", { x, y, class: className, "text-anchor": anchor }, text);

  const dot = (x, y, radius = 5, fill = "#172033") =>
    make("circle", { cx: x, cy: y, r: radius, fill });

  const arcPath = (cx, cy, radius, startDegrees, endDegrees, className) => {
    let span = endDegrees - startDegrees;
    while (span < 0) span += 360;
    if (span >= 359.9) {
      return make("circle", { cx, cy, r: radius, class: className });
    }
    const [sx, sy] = pointAt(cx, cy, radius, startDegrees);
    const [ex, ey] = pointAt(cx, cy, radius, endDegrees);
    const largeArc = span > 180 ? 1 : 0;
    return make("path", {
      d: `M ${sx} ${sy} A ${radius} ${radius} 0 ${largeArc} 0 ${ex} ${ey}`,
      class: className
    });
  };

  const circle = (cx, cy, radius, className = "svg-line") =>
    make("circle", { cx, cy, r: radius, class: className, fill: "none" });

  const clear = () => stage.replaceChildren();

  const endpointLabel = (cx, cy, degrees, text, radius = 185) => {
    const [x, y] = pointAt(cx, cy, radius, degrees);
    label(x, y + 5, text);
  };

  const drawAngleRotation = (degrees) => {
    clear();
    const cx = 320;
    const cy = 220;
    ray(cx, cy, 0, 190, "svg-line svg-ray-blue");
    ray(cx, cy, degrees, 190, "svg-line svg-ray-purple");
    arcPath(cx, cy, 72, 0, degrees, "svg-angle-purple");
    dot(cx, cy);
    endpointLabel(cx, cy, 0, "A", 212);
    endpointLabel(cx, cy, degrees, "B", 212);
    label(cx - 13, cy + 24, "O");
    label(320, 34, "Поверни промінь OB", "svg-label");
    label(320, 57, "Довжина променів не змінює кут", "svg-small");

    let type = "гострий";
    if (degrees === 0) type = "нульовий";
    else if (degrees === 360) type = "повний";
    else if (degrees === 90) type = "прямий";
    else if (degrees === 180) type = "розгорнутий";
    else if (degrees > 90 && degrees < 180) type = "тупий";
    else if (degrees > 180 && degrees < 360) type = "більший за розгорнутий";
    valueBox.textContent = `${degrees}° - ${type} кут`;
  };

  const drawCentralAngleArc = (degrees) => {
    clear();
    const radius = 92;
    const first = { x: 185, y: 220, start: 10 };
    const second = { x: 455, y: 220, start: 145 };

    [first, second].forEach((center, index) => {
      circle(center.x, center.y, radius, "svg-line");
      ray(center.x, center.y, center.start, radius, "svg-line svg-ray-blue");
      ray(center.x, center.y, center.start + degrees, radius, "svg-line svg-ray-blue");
      arcPath(
        center.x,
        center.y,
        radius,
        center.start,
        center.start + degrees,
        "svg-angle-green"
      );
      arcPath(
        center.x,
        center.y,
        35,
        center.start,
        center.start + degrees,
        "svg-angle-purple"
      );
      dot(center.x, center.y);
      label(center.x, center.y + 25, index === 0 ? "O₁" : "O₂", "svg-label");
      label(center.x, 360, `кут ${degrees}°`, "svg-small");
    });

    label(320, 34, "Два рівні кола і два рівні центральні кути", "svg-label");
    label(320, 58, "Зелені дуги теж рівні", "svg-small");
    valueBox.textContent = `кути: ${degrees}° = ${degrees}°; дуги рівні`;
  };

  const drawAdjacentAngles = (degrees) => {
    clear();
    const cx = 320;
    const cy = 230;
    line(100, cy, 540, cy, "svg-line");
    ray(cx, cy, degrees, 185, "svg-line svg-ray-purple");
    arcPath(cx, cy, 62, 0, degrees, "svg-angle-blue");
    arcPath(cx, cy, 88, degrees, 180, "svg-angle-green");
    dot(cx, cy);
    endpointLabel(cx, cy, 180, "A", 220);
    endpointLabel(cx, cy, 0, "B", 220);
    endpointLabel(cx, cy, degrees, "C", 210);
    label(cx - 12, cy + 25, "O");
    label(320, 34, "Спільний промінь ділить розгорнутий кут", "svg-label");
    label(320, 58, "Одна частина зростає рівно настільки, наскільки інша зменшується", "svg-small");
    valueBox.textContent = `${degrees}° + ${180 - degrees}° = 180°`;
  };

  const drawVerticalHalfTurn = (rotation) => {
    clear();
    const cx = 320;
    const cy = 215;
    const start = 18;
    const end = 78;

    line(...pointAt(cx, cy, 205, start + 180), ...pointAt(cx, cy, 205, start), "svg-line");
    line(...pointAt(cx, cy, 205, end + 180), ...pointAt(cx, cy, 205, end), "svg-line");
    arcPath(cx, cy, 67, start, end, "svg-angle-blue");
    ray(cx, cy, start + rotation, 160, "svg-line svg-ray-purple svg-dashed");
    ray(cx, cy, end + rotation, 160, "svg-line svg-ray-purple svg-dashed");
    arcPath(cx, cy, 88, start + rotation, end + rotation, "svg-angle-purple");
    dot(cx, cy);
    label(cx - 12, cy + 25, "O");
    label(320, 34, "Фіолетова копія повертається навколо O", "svg-label");
    label(320, 58, "За 180° вона суміститься з протилежним кутом", "svg-small");

    const remaining = 180 - rotation;
    valueBox.textContent = rotation === 180
      ? "180° - кути сумістилися"
      : `поворот ${rotation}°; залишилося ${remaining}°`;
  };

  const drawAdjacentBisectors = (degrees) => {
    clear();
    const cx = 320;
    const cy = 230;
    const firstBisector = degrees / 2;
    const secondBisector = (degrees + 180) / 2;
    line(95, cy, 545, cy, "svg-line");
    ray(cx, cy, degrees, 180, "svg-line svg-ray-purple");
    ray(cx, cy, firstBisector, 170, "svg-line svg-ray-blue");
    ray(cx, cy, secondBisector, 170, "svg-line svg-ray-green");
    arcPath(cx, cy, 64, firstBisector, secondBisector, "svg-angle-red");
    dot(cx, cy);
    label(320, 34, "Бісектриси ділять суміжні кути навпіл", "svg-label");
    label(320, 58, "Половина від 180° завжди дорівнює 90°", "svg-small");
    label(cx + 14, cy - 80, "90°", "svg-label");
    valueBox.textContent = `${degrees / 2}° + ${(180 - degrees) / 2}° = 90°`;
  };

  const drawVerticalBisectors = (degrees) => {
    clear();
    const cx = 320;
    const cy = 220;
    const bisector = degrees / 2;
    line(95, cy, 545, cy, "svg-line");
    line(
      ...pointAt(cx, cy, 205, degrees + 180),
      ...pointAt(cx, cy, 205, degrees),
      "svg-line"
    );
    ray(cx, cy, bisector, 190, "svg-line svg-ray-blue");
    ray(cx, cy, bisector + 180, 190, "svg-line svg-ray-blue");
    arcPath(cx, cy, 64, 0, degrees, "svg-angle-purple");
    arcPath(cx, cy, 64, 180, 180 + degrees, "svg-angle-purple");
    dot(cx, cy);
    label(320, 34, "Поворот на 180° переносить і кут, і його бісектрису", "svg-label");
    label(320, 58, "Два сині промені є частинами однієї прямої", "svg-small");
    valueBox.textContent = `напрями: ${bisector}° і ${bisector + 180}°; різниця 180°`;
  };

  const renderers = {
    "angle-rotation": drawAngleRotation,
    "central-angle-arc": drawCentralAngleArc,
    "adjacent-angles": drawAdjacentAngles,
    "vertical-half-turn": drawVerticalHalfTurn,
    "adjacent-bisectors": drawAdjacentBisectors,
    "vertical-bisectors": drawVerticalBisectors
  };

  const render = () => {
    const value = Number(slider.value);
    renderers[demo]?.(value);
    slider.setAttribute("aria-valuetext", `${value} градусів`);
  };

  let animationFrame = null;
  const playHalfTurn = () => {
    if (animationFrame) cancelAnimationFrame(animationFrame);
    slider.value = "0";
    const started = performance.now();
    const duration = 1800;
    const tick = (now) => {
      const progress = Math.min((now - started) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      slider.value = String(Math.round(180 * eased));
      render();
      if (progress < 1) animationFrame = requestAnimationFrame(tick);
      else animationFrame = null;
    };
    animationFrame = requestAnimationFrame(tick);
  };

  slider.addEventListener("input", render);
  playButton?.addEventListener("click", playHalfTurn);
  render();
})();
