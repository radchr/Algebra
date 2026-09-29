import { arcPath, createScene, pointAt, setSvgSummary, unlockAfterPrediction } from "./core.js";

const stage = document.getElementById("motion-stage");
const slider = document.getElementById("motion-slider");
const controls = document.getElementById("motion-control-fieldset");
const output = document.getElementById("motion-value");
const form = document.getElementById("prediction-form");
const feedback = document.getElementById("prediction-feedback");
const missionFeedback = document.getElementById("mission-feedback");

if (stage && slider && controls && output && form && feedback) {
  const scene = createScene(stage);
  const angleSize = 55;

  const drawAngle = (cx, cy, orientation, className, arcClass) => {
    const first = pointAt(cx, cy, 135, orientation);
    const second = pointAt(cx, cy, 135, orientation + angleSize);
    scene.line(cx, cy, first[0], first[1], className);
    scene.line(cx, cy, second[0], second[1], className);
    scene.path(arcPath(cx, cy, 52, orientation, orientation + angleSize), arcClass);
    scene.dot(cx, cy, 6, className.includes("svg-copy") ? "var(--motion-purple)" : "var(--motion-blue)");
  };

  const draw = () => {
    scene.clear();
    setSvgSummary(stage, "Суміщення рівних кутів", "Напівпрозора копія кута переноситься і повертається без зміни величини.");
    const progress = Number(slider.value) / 100;
    const start = { x: 150, y: 285, orientation: 105 };
    const target = { x: 455, y: 245, orientation: 15 };
    const current = {
      x: start.x + (target.x - start.x) * progress,
      y: start.y + (target.y - start.y) * progress,
      orientation: start.orientation + (target.orientation - start.orientation) * progress
    };
    drawAngle(target.x, target.y, target.orientation, "svg-target", "svg-angle-blue");
    drawAngle(current.x, current.y, current.orientation, "svg-copy svg-dashed", "svg-angle-purple");
    scene.label(320, 42, "Кут переноситься і повертається як жорстка фігура", "svg-label");
    scene.label(320, 66, "Інваріант: величина кута 55°", "svg-small");
    scene.label(target.x, target.y + 30, "еталон", "svg-small");
    output.textContent = progress === 1
      ? "кути сумістилися; 55° = 55°"
      : `шлях до суміщення: ${Math.round(progress * 100)}%; кут = 55°`;
  };

  unlockAfterPrediction({
    form,
    controls,
    feedback,
    correctValue: "position",
    success: "Так. Положення змінюється, але величина кута зберігається.",
    retry: "Перевір: жорсткий рух змінює місце й напрям, але не розкриття кута."
  });
  slider.addEventListener("input", draw);
  document.querySelectorAll("[data-angle]").forEach((button) => {
    button.addEventListener("click", () => {
      const value = Number(button.dataset.angle);
      missionFeedback.textContent = value === angleSize
        ? "Правильно: лише кут 55° можна точно сумістити з еталоном."
        : `Кут ${value}° не суміститься: жорсткий рух не змінює його величини.`;
    });
  });
  draw();
}
