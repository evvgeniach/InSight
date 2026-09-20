import pandas as pd
import plotly.express as px
from src.charts import COLORS


def _chart_to_html(chart: dict) -> str:
    if not chart or not chart.get("type"):
        return ""
    try:
        df = pd.DataFrame({"label": chart["labels"], "value": chart["values"]})
        title = chart.get("title", "")
        t = chart["type"]
        if t == "bar":
            fig = px.bar(df, x="label", y="value", title=title, color_discrete_sequence=COLORS)
        elif t == "line":
            fig = px.line(df, x="label", y="value", title=title, color_discrete_sequence=COLORS)
        elif t == "doughnut":
            fig = px.pie(df, names="label", values="value", title=title, hole=0.4, color_discrete_sequence=COLORS)
        else:
            return ""
        fig.update_layout(margin=dict(t=40, b=0, l=0, r=0), plot_bgcolor="white", paper_bgcolor="white")
        return fig.to_html(full_html=False, include_plotlyjs=False)
    except Exception:
        return ""


def generate_html_report(messages: list, title: str = "InSight Report") -> str:
    blocks = []
    for msg in messages:
        label = "You" if msg["role"] == "user" else "InSight"
        bg = "#EFF6FF" if msg["role"] == "user" else "#F8FAFC"
        border = "#BFDBFE" if msg["role"] == "user" else "#E2E8F0"
        content = msg["content"].replace("\n", "<br>")

        stats_html = ""
        if msg.get("stats"):
            cards = "".join(
                f'<div style="background:#fff;border:1px solid #E2E8F0;border-radius:8px;padding:.75rem 1.25rem;">'
                f'<div style="font-size:.75rem;color:#6B7280;">{s["label"]}</div>'
                f'<div style="font-size:1.25rem;font-weight:600;">{s["value"]}</div></div>'
                for s in msg["stats"]
            )
            stats_html = f'<div style="display:flex;gap:.75rem;flex-wrap:wrap;margin-top:.75rem;">{cards}</div>'

        chart_html = _chart_to_html(msg.get("chart", {}))
        chart_wrap = f'<div style="margin-top:1rem;">{chart_html}</div>' if chart_html else ""

        blocks.append(
            f'<div style="background:{bg};border:1px solid {border};border-radius:12px;'
            f'padding:1.25rem;margin-bottom:1rem;">'
            f'<div style="font-size:.7rem;font-weight:600;color:#6B7280;text-transform:uppercase;'
            f'letter-spacing:.05em;margin-bottom:.5rem;">{label}</div>'
            f'<div style="color:#111827;line-height:1.6;">{content}</div>'
            f'{stats_html}{chart_wrap}</div>'
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
       background:#fff;color:#111827;padding:2rem;max-width:900px;margin:0 auto}}
  h1{{font-size:1.75rem;font-weight:700;letter-spacing:-.5px;margin-bottom:.25rem}}
  .sub{{color:#6B7280;font-size:.9rem;margin-bottom:2rem}}
  hr{{border:none;border-top:1px solid #E2E8F0;margin:1.5rem 0}}
</style>
</head>
<body>
<h1>{title}</h1>
<div class="sub">Exported from InSight</div>
<hr>
{"".join(blocks)}
</body>
</html>"""
