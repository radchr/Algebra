import { createScene, setSvgSummary, unlockAfterPrediction } from "./core.js";

const stage = document.getElementById("motion-stage");
const slider = document.getElementById("motion-slider");
const controls = document.getElementById("motion-control-fieldset");
const output = document.getElementById("motion-value");
const form = document.getElementById("prediction-form");
const feedback = document.getElementById("prediction-feedback");
const missionFeedback = document.getElementById("mission-feedback");
const modeInputs = [...document.querySelectorAll('input[name="trace-mode"]')];

if (stage && slider && controls && output && form && feedback) {
  const scene = createScene(stage);

  const curvePoint = (t) => {
    const p0 = [95, 300];
    const p1 = [320, 25];
    const p2 = [545, 290];
    const u = 1 - t;
    return [
      u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
      u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]
    ];
  };

  const draw = () => {
    scene.clear();
    setSvgSummary(stage, "Слід рухомої точки", "Точка рухається зі сталим або змінним напрямом і залишає слід.");
    const t = Number(slider.value) / 100;
    const mode = modeInputs.find((input) => input.checked)?.value ?? "straight";
    let point;

    if (mode === "straight") {
      const start = [90, 300];
      const end = [550, 95];
      point = [start[0] + (end[0] - start[0]) * t, start[1] + (end[1] - start[1]) * t];
      scene.line(start[0], start[1], end[0], end[1], "svg-guide");
      scene.line(start[0], start[1], point[0], point[1], "svg-trace");
      scene.label(320, 42, "Напрям руху не змінюється", "svg-label");
      scene.label(320, 66, "Інваріант: сталий напрям", "svg-small");
      output.textContent = `пройдений шлях: ${Math.round(t * 100)}%; слід — пряма`;
    } else {
      const points = [];
      for (let index = 0; index <= 80; index += 1) points.push(curvePoint(index / 80));
      scene.polyline(points, "svg-guide");
      const visible = [];
      const steps = Math.max(1, Math.round(t * 80));
      for (let index = 0; index <= steps; index += 1) visible.push(curvePoint(index / 80));
      point = curvePoint(t);
      scene.polyline(visible, "svg-trace");
      scene.label(320, 42, "Напрям руху поступово змінюється", "svg-label");
      scene.label(320, 66, "Тому слід викривляється", "svg-small");
      output.textContent = `пройдений шлях: ${Math.round(t * 100)}%; слід — крива`;
    }

    scene.dot(point[0], point[1], 9, "var(--motion-purple)");
    scene.label(point[0], point[1] - 17, "P", "svg-label");
  };

  unlockAfterPrediction({
    form,
    controls,
    feedback,
    correctValue: "straight",
    success: "Так. Сталий напрям породжує прямолінійний слід.",
    retry: "Перевір дослідом: вирішальним є те, чи змінюється напрям руху."
  });
  slider.addEventListener("input", draw);
  modeInputs.forEach((input) => input.addEventListener("change", draw));
  document.querySelectorAll("[data-mission-answer]").forEach((button) => {
    button.addEventListener("click", () => {
      const correct = button.dataset.missionAnswer === "changing";
      missionFeedback.textContent = correct
        ? "Правильно: вигнутий слід показує, що напрям змінювався."
        : "Спробуй ще: за сталого напряму слід був би прямим.";
    });
  });
  draw();
}
