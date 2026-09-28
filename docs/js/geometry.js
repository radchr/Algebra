/**
 * Interactive Geometry Engine using JSXGraph
 * Topics: Supplementary & Vertical Angles (Kiselev 1931 / Merzlyak 7th Grade)
 */

function initGeometry() {
  if (typeof JXG === "undefined") {
    console.warn("JSXGraph not loaded yet");
    return;
  }

  // 1. Board for Supplementary Angles (Суміжні кути)
  const board1 = JXG.JSXGraph.initBoard('jxg-supplementary', {
    boundingbox: [-5, 4, 5, -2],
    axis: false,
    showNavigation: false,
    showCopyright: false,
    pan: { enabled: false },
    zoom: { enabled: false }
  });

  // Points on horizontal line
  const O = board1.create('point', [0, 0], { name: 'O', fixed: true, size: 4, color: '#0f172a' });
  const A = board1.create('point', [-4, 0], { name: 'A', fixed: true, size: 3, color: '#475569' });
  const B = board1.create('point', [4, 0], { name: 'B', fixed: true, size: 3, color: '#475569' });
  
  // Straight line AB
  board1.create('segment', [A, B], { strokeColor: '#1e293b', strokeWidth: 3 });

  // Movable point C on upper half circle
  const C = board1.create('glider', [
    2.5 * Math.cos(Math.PI / 3),
    2.5 * Math.sin(Math.PI / 3),
    board1.create('circle', [O, 2.8], { visible: false })
  ], {
    name: 'C (рухай мене)',
    size: 6,
    color: '#2563eb',
    fillColor: '#60a5fa'
  });

  // Ray OC
  board1.create('segment', [O, C], { strokeColor: '#2563eb', strokeWidth: 3.5 });

  // Angle AOC (Left)
  const angleAOC = board1.create('angle', [C, O, A], {
    radius: 1.1,
    fillColor: '#93c5fd',
    fillOpacity: 0.4,
    strokeColor: '#1d4ed8',
    strokeWidth: 2,
    name: ''
  });

  // Angle BOC (Right)
  const angleBOC = board1.create('angle', [B, O, C], {
    radius: 1.3,
    fillColor: '#86efac',
    fillOpacity: 0.4,
    strokeColor: '#15803d',
    strokeWidth: 2,
    name: ''
  });

  function updateAngleMetrics() {
    let degAOC = JXG.Math.Geometry.trueAngle(C, O, A);
    if (degAOC > 180) degAOC = 360 - degAOC;
    let degBOC = 180 - degAOC;

    degAOC = Math.round(degAOC);
    degBOC = 180 - degAOC;

    const elAOC = document.getElementById('val-angle-aoc');
    const elBOC = document.getElementById('val-angle-boc');
    const elSum = document.getElementById('val-angle-sum');
    const elType = document.getElementById('angle-type-badge');

    if (elAOC) elAOC.textContent = `${degAOC}°`;
    if (elBOC) elBOC.textContent = `${degBOC}°`;
    if (elSum) elSum.textContent = `${degAOC}° + ${degBOC}° = 180°`;

    if (elType) {
      if (degAOC === 90) {
        elType.innerHTML = "⚖️ Обидва кути <b>прямі</b> (90° + 90°)";
        elType.style.color = "#1d4ed8";
      } else if (degAOC < 90) {
        elType.innerHTML = "📐 ∠AOC <b>гострий</b>, а ∠BOC <b>тупий</b>";
        elType.style.color = "#0f172a";
      } else {
        elType.innerHTML = "📐 ∠AOC <b>тупий</b>, а ∠BOC <b>гострий</b>";
        elType.style.color = "#0f172a";
      }
    }
  }

  C.on('drag', updateAngleMetrics);
  updateAngleMetrics();

  // 2. Mini-Quiz Checkers for Geometry
  window.checkGeomQuiz = function(qNum, correctVal) {
    const input = document.getElementById(`geom-q${qNum}`);
    const fb = document.getElementById(`geom-fb${qNum}`);
    if (!input || !fb) return;

    const val = input.value.trim();
    if (val === String(correctVal)) {
      fb.innerHTML = "✅ <b>Правильно!</b> Сума суміжних кутів завжди 180°, тому 180° - 55° = 125°.";
      fb.className = "feedback-box feedback-success";
      fb.style.display = "block";
    } else {
      fb.innerHTML = "❌ <b>Не зовсім.</b> Згадайте теорему: сума суміжних кутів дорівнює 180°. Відніміть 55° від 180°.";
      fb.className = "feedback-box feedback-error";
      fb.style.display = "block";
    }
  };
}

window.addEventListener("DOMContentLoaded", initGeometry);
