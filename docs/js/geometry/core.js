const NS = "http://www.w3.org/2000/svg";

export const createScene = (stage) => {
  const make = (name, attrs = {}, text = "") => {
    const node = document.createElementNS(NS, name);
    Object.entries(attrs).forEach(([key, value]) => node.setAttribute(key, value));
    if (text) node.textContent = text;
    stage.appendChild(node);
    return node;
  };

  const clear = () => stage.replaceChildren();
  const line = (x1, y1, x2, y2, className = "svg-line") =>
    make("line", { x1, y1, x2, y2, class: className });
  const circle = (cx, cy, radius, className = "svg-line") =>
    make("circle", { cx, cy, r: radius, class: className, fill: "none" });
  const dot = (x, y, radius = 6, fill = "var(--motion-ink)") =>
    make("circle", { cx: x, cy: y, r: radius, fill });
  const label = (x, y, value, className = "svg-label", anchor = "middle") =>
    make("text", { x, y, class: className, "text-anchor": anchor }, value);
  const path = (d, className) => make("path", { d, class: className });
  const polyline = (points, className) =>
    make("polyline", { points: points.map(([x, y]) => `${x},${y}`).join(" "), class: className });

  return { stage, make, clear, line, circle, dot, label, path, polyline };
};

export const pointAt = (cx, cy, radius, degrees) => {
  const radians = (degrees * Math.PI) / 180;
  return [cx + radius * Math.cos(radians), cy - radius * Math.sin(radians)];
};

export const arcPath = (cx, cy, radius, startDegrees, endDegrees) => {
  let span = endDegrees - startDegrees;
  while (span < 0) span += 360;
  if (span >= 359.9) {
    return `M ${cx + radius} ${cy} A ${radius} ${radius} 0 1 0 ${cx - radius} ${cy} A ${radius} ${radius} 0 1 0 ${cx + radius} ${cy}`;
  }
  const [sx, sy] = pointAt(cx, cy, radius, startDegrees);
  const [ex, ey] = pointAt(cx, cy, radius, endDegrees);
  return `M ${sx} ${sy} A ${radius} ${radius} 0 ${span > 180 ? 1 : 0} 0 ${ex} ${ey}`;
};

export const setSvgSummary = (stage, title, description) => {
  const titleNode = document.createElementNS(NS, "title");
  titleNode.textContent = title;
  const descNode = document.createElementNS(NS, "desc");
  descNode.textContent = description;
  stage.append(titleNode, descNode);
};

export const unlockAfterPrediction = ({ form, controls, feedback, correctValue, success, retry }) => {
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const selected = new FormData(form).get("prediction");
    if (!selected) {
      feedback.textContent = "Спочатку обери свій прогноз.";
      return;
    }
    controls.disabled = false;
    feedback.textContent = selected === correctValue ? success : retry;
    controls.querySelector("input, button")?.focus();
  });
};
