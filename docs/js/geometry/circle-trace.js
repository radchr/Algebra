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
  const cx = 320;
  const cy = 220;
  const radius = 135;

  const draw = () => {
    scene.clear();
    setSvgSummary(stage, "Коло як слід точки", "Точка A рухається на сталій відстані від нерухомого центра O.");
    const degrees = Number(slider.value);
    const [x, y] = pointAt(cx, cy, radius, degrees);
    scene.circle(cx, cy, radius, "svg-guide");
    scene.path(arcPath(cx, cy, radius, 0, degrees), "svg-trace");
    scene.line(cx, cy, x, y, "svg-line svg-ray-blue");
    scene.dot(cx, cy);
    scene.dot(x, y, 9, "var(--motion-purple)");
    scene.label(cx - 15, cy + 25, "O", "svg-label");
    scene.label(x, y - 16, "A", "svg-label");
    scene.label((cx + x) / 2, (cy + y) / 2 - 11, "r", "svg-label");
    scene.label(320, 42, "OA = r залишається незмінною", "svg-label");
    scene.label(320, 66, "Інваріант: відстань до центра", "svg-small");
    output.textContent = `${degrees}°; OA = r = ${radius} умовних одиниць`;
  };

  unlockAfterPrediction({
    form,
    controls,
    feedback,
    correctValue: "circle",
    success: "Так. Стала відстань до центра породжує коло.",
    retry: "Перевір рухом: усі положення точки мають однакову відстань до O."
  });
  slider.addEventListener("input", draw);
  document.querySelectorAll("[data-radius]").forEach((button) => {
    button.addEventListener("click", () => {
      const correct = Number(button.dataset.radius) === radius;
      missionFeedback.textContent = correct
        ? "Правильно: точка належить колу, бо її відстань до O дорівнює r."
        : "Ні. Для точки кола відстань до центра має точно дорівнювати r.";
    });
  });
  draw();
}
