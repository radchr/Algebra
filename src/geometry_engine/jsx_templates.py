"""JSXGraph HTML/JS templates for tactile hands-on manipulatives in Marimo.

Allows embedding dragging points, triangle superposition, and scissors models
reliably using isolated sandboxed iframes.
"""

from __future__ import annotations

import html


def get_scissors_widget_html(box_id: str = "jxgbox_scissors", initial_angle: float = 55.0) -> str:
    """Генерує інтерактивну модель ножиць на JSXGraph з перетягуванням лез."""
    iframe_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/jsxgraph/distrib/jsxgraph.css" />
  <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/jsxgraph/distrib/jsxgraphcore.js"></script>
  <style>
    html, body {{ margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background: #f8fafc; }}
    #{box_id} {{ width: 100%; height: 100%; }}
  </style>
</head>
<body>
  <div id="{box_id}" class="jxgbox"></div>
  <script>
    window.addEventListener('load', function() {{
      var board = JXG.JSXGraph.initBoard('{box_id}', {{
        boundingbox: [-5, 5, 5, -5],
        axis: false,
        showNavigation: false,
        showCopyright: false
      }});
      
      var O = board.create('point', [0, 0], {{name: 'O', fixed: true, size: 4, color: '#0f172a'}});
      var A = board.create('point', [3.5, 2.0], {{name: 'A', size: 6, color: '#2563eb'}});
      var B = board.create('point', [3.5, -2.0], {{name: 'B', size: 6, color: '#2563eb'}});
      
      var A_opp = board.create('point', [
        function() {{ return -A.X(); }},
        function() {{ return -A.Y(); }}
      ], {{name: "A'", size: 3, color: '#94a3b8', fixed: true}});
      
      var B_opp = board.create('point', [
        function() {{ return -B.X(); }},
        function() {{ return -B.Y(); }}
      ], {{name: "B'", size: 3, color: '#94a3b8', fixed: true}});
      
      board.create('line', [A, A_opp], {{straightFirst: true, straightLast: true, strokeColor: '#2563eb', strokeWidth: 3}});
      board.create('line', [B, B_opp], {{straightFirst: true, straightLast: true, strokeColor: '#dc2626', strokeWidth: 3}});
      
      board.create('angle', [B, O, A], {{name: '∠1', radius: 1.2, color: '#2563eb'}});
      board.create('angle', [B_opp, O, A_opp], {{name: '∠3', radius: 1.2, color: '#2563eb'}});
    }});
  </script>
</body>
</html>"""

    escaped_doc = html.escape(iframe_content, quote=True)
    return f"""
    <div style="background: #f8fafc; padding: 12px; border-radius: 12px; border: 1px solid #e2e8f0; max-width: 580px; margin: 0 auto;">
      <iframe srcdoc="{escaped_doc}" style="width: 100%; height: 320px; border: none; border-radius: 8px;"></iframe>
      <p style="text-align: center; font-size: 13px; color: #64748b; margin: 8px 0 0 0;">
        💡 <em>Потягни пальцем або мишкою за синю точку <strong>A</strong> і спостерігай: розкриття протилежних лез завжди однакове!</em>
      </p>
    </div>
    """


def get_triangle_congruence_html(box_id: str = "jxgbox_triangles") -> str:
    """Генерує модель накладання двох трикутників (спосіб накладання за Кисельовим)."""
    iframe_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/jsxgraph/distrib/jsxgraph.css" />
  <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/jsxgraph/distrib/jsxgraphcore.js"></script>
  <style>
    html, body {{ margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background: #f8fafc; }}
    #{box_id} {{ width: 100%; height: 100%; }}
  </style>
</head>
<body>
  <div id="{box_id}" class="jxgbox"></div>
  <script>
    window.addEventListener('load', function() {{
      var board = JXG.JSXGraph.initBoard('{box_id}', {{
        boundingbox: [-4, 5, 8, -3],
        axis: false,
        showNavigation: false,
        showCopyright: false
      }});
      
      // Фіксований еталонний трикутник ABC
      var A = board.create('point', [0, 0], {{name: 'A', fixed: true, color: '#0284c7'}});
      var B = board.create('point', [3, 0], {{name: 'B', fixed: true, color: '#0284c7'}});
      var C = board.create('point', [1.2, 2.5], {{name: 'C', fixed: true, color: '#0284c7'}});
      board.create('polygon', [A, B, C], {{fillColor: '#bae6fd', fillOpacity: 0.5, borders: {{strokeColor: '#0284c7', strokeWidth: 2}}}});
      
      // Рухомий трикутник A1B1C1 (перетягується за A1)
      var A1 = board.create('point', [4.5, -1], {{name: 'A₁', color: '#ea580c', size: 5}});
      var B1 = board.create('point', [function() {{ return A1.X() + 3; }}, function() {{ return A1.Y(); }}], {{name: 'B₁', color: '#ea580c', size: 3}});
      var C1 = board.create('point', [function() {{ return A1.X() + 1.2; }}, function() {{ return A1.Y() + 2.5; }}], {{name: 'C₁', color: '#ea580c', size: 3}});
      board.create('polygon', [A1, B1, C1], {{fillColor: '#fed7aa', fillOpacity: 0.6, borders: {{strokeColor: '#ea580c', strokeWidth: 2.5}}}});
    }});
  </script>
</body>
</html>"""

    escaped_doc = html.escape(iframe_content, quote=True)
    return f"""
    <div style="background: #f8fafc; padding: 12px; border-radius: 12px; border: 1px solid #e2e8f0; max-width: 580px; margin: 0 auto;">
      <iframe srcdoc="{escaped_doc}" style="width: 100%; height: 320px; border: none; border-radius: 8px;"></iframe>
      <p style="text-align: center; font-size: 13px; color: #64748b; margin: 8px 0 0 0;">
        💡 <em>Перетягни помаранчевий трикутник A₁B₁C₁ (за точку A₁) на синій еталон ABC, щоб сумістити їх!</em>
      </p>
    </div>
    """
