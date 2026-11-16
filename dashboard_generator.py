
import json
from pathlib import Path
from html import escape

PROJECT_DIR = Path(__file__).resolve().parent
REPORT_FILE = PROJECT_DIR / "output" / "incident_report.json"
DASHBOARD_FILE = PROJECT_DIR / "output" / "incident_dashboard.html"


def load_report():
    with open(REPORT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def safe(value):
    return escape(str(value))


def generate_dashboard(report):
    metrics = report["dashboard_metrics"]

    severity_colors = {
        "Critical": "#7c3aed",
        "High": "#dc2626",
        "Medium": "#f59e0b",
        "Low": "#16a34a"
    }

    category_colors = [
        "#2563eb", "#0891b2", "#7c3aed",
        "#d97706", "#16a34a"
    ]

    severity_rows = ""
    for severity, count in report["severity_counts"].items():
        color = severity_colors.get(severity, "#64748b")
        severity_rows += f"""
        <tr>
            <td><span class="dot" style="background:{color}"></span>
                {safe(severity)}</td>
            <td><strong>{count}</strong></td>
        </tr>
        """

    category_rows = ""
    for index, (category, count) in enumerate(
        report["category_counts"].items()
    ):
        color = category_colors[index % len(category_colors)]
        category_rows += f"""
        <tr>
            <td><span class="dot" style="background:{color}"></span>
                {safe(category)}</td>
            <td><strong>{count}</strong></td>
        </tr>
        """

    def make_bars(data, colors):
        total = max(sum(data.values()), 1)
        result = ""

        for index, (name, count) in enumerate(data.items()):
            percentage = count / total * 100
            color = colors[index % len(colors)]

            result += f"""
            <div class="bar-item">
                <div class="bar-heading">
                    <span>{safe(name)}</span>
                    <strong>{count}</strong>
                </div>
                <div class="bar-track">
                    <div class="bar-fill"
                         style="width:{percentage:.1f}%;background:{color}">
                    </div>
                </div>
            </div>
            """

        return result

    severity_bars = make_bars(
        report["severity_counts"],
        [severity_colors.get(s, "#64748b")
         for s in report["severity_counts"]]
    )

    category_bars = make_bars(
        report["category_counts"],
        category_colors
    )

    def make_table_rows(data):
        if not data:
            return '<tr><td colspan="2">No records identified</td></tr>'

        return "".join(
            f"<tr><td>{safe(name)}</td><td><strong>{count}</strong></td></tr>"
            for name, count in data.items()
        )

    recurring_rows = make_table_rows(report["recurring_issues"])

    security_rows = "".join(
        f'<li><span class="alert-dot"></span>'
        f'<strong>{safe(incident_id)}</strong> — requires investigation</li>'
        for incident_id in report["security_concerns"]
    ) or "<li>No security concerns identified</li>"

    compliance_rows = "".join(
        f'<li><span class="warning-dot"></span>'
        f'<strong>{safe(incident_id)}</strong> — requires human review</li>'
        for incident_id in report["compliance_concerns"]
    ) or "<li>No compliance concerns identified</li>"

    preventive_rows = "".join(
        f"<li>{safe(action)}</li>"
        for action in report["preventive_actions"]
    ) or "<li>No preventive actions identified</li>"

    cards = [
        ("Total Issues", metrics["total_issues"], "blue"),
        ("Open Issues", metrics["open_issues"], "orange"),
        ("High Severity", metrics["high_severity_issues"], "red"),
        ("Resolved Issues", metrics["resolved_issues"], "green"),
        ("Recurring Types", metrics["recurring_issue_types"], "purple"),
        ("Security Flags", metrics["security_flags"], "red"),
        ("Compliance Flags", metrics["compliance_flags"], "orange"),
        ("Avg Resolution Time",
         f'{metrics["average_resolution_time_minutes"]} min', "blue")
    ]

    metric_cards = "".join(
        f"""
        <div class="metric-card {color}">
            <div class="metric-label">{safe(label)}</div>
            <div class="metric-value">{safe(value)}</div>
        </div>
        """
        for label, value, color in cards
    )

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>AI Incident Intelligence Dashboard</title>

<style>
* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    font-family: "Segoe UI", Arial, sans-serif;
    background: #f2f5f9;
    color: #1e293b;
}}

.header {{
    background: linear-gradient(120deg, #10243d, #1e4165);
    color: white;
    padding: 32px 5%;
}}

.header h1 {{
    margin: 0;
    font-size: 29px;
    letter-spacing: .3px;
}}

.header p {{
    color: #cbd5e1;
    margin: 9px 0 0;
    font-size: 14px;
}}

.header-tag {{
    display: inline-block;
    margin-top: 18px;
    padding: 7px 13px;
    border: 1px solid #45617e;
    border-radius: 20px;
    font-size: 11px;
    color: #dbeafe;
    letter-spacing: .8px;
}}

.container {{
    width: 100%;
    max-width: 1450px;
    margin: 0 auto;
    padding: 28px 40px;
}}
}}

.section-title {{
    font-size: 19px;
    margin: 28px 0 17px;
    color: #142b45;
}}

.metrics {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 17px;
}}

.metric-card {{
    background: white;
    border-radius: 12px;
    padding: 22px;
    border: 1px solid #e5eaf0;
    border-left: 4px solid #2563eb;
    box-shadow: 0 3px 12px rgba(15,23,42,.04);
    transition: transform .2s;
}}

.metric-card:hover {{
    transform: translateY(-3px);
}}

.metric-label {{
    color: #64748b;
    font-size: 13px;
    font-weight: 600;
}}

.metric-value {{
    font-size: 30px;
    font-weight: 750;
    margin-top: 13px;
    color: #142b45;
}}

.blue {{ border-left-color: #2563eb; }}
.orange {{ border-left-color: #f59e0b; }}
.red {{ border-left-color: #dc2626; }}
.green {{ border-left-color: #16a34a; }}
.purple {{ border-left-color: #7c3aed; }}

.section-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 20px;
}}

.panel {{
    background: white;
    padding: 23px;
    border-radius: 12px;
    border: 1px solid #e5eaf0;
    box-shadow: 0 3px 12px rgba(15,23,42,.04);
}}

.panel h2 {{
    font-size: 17px;
    color: #142b45;
    margin: 0 0 22px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th, td {{
    text-align: left;
    padding: 13px 10px;
    border-bottom: 1px solid #edf0f4;
    font-size: 13px;
}}

th {{
    color: #64748b;
    background: #f8fafc;
    font-weight: 600;
}}

.dot {{
    width: 9px;
    height: 9px;
    display: inline-block;
    border-radius: 50%;
    margin-right: 8px;
}}

.bar-item {{
    margin-bottom: 19px;
}}

.bar-heading {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
    font-size: 13px;
}}

.bar-track {{
    height: 9px;
    background: #edf1f5;
    border-radius: 20px;
    overflow: hidden;
}}

.bar-fill {{
    height: 100%;
    border-radius: 20px;
}}

ul {{
    padding-left: 20px;
    margin: 0;
}}

li {{
    margin-bottom: 15px;
    line-height: 1.6;
    font-size: 13px;
    color: #475569;
}}

.alert-dot, .warning-dot {{
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 8px;
}}

.alert-dot {{ background: #dc2626; }}
.warning-dot {{ background: #f59e0b; }}

.summary {{
    background: #142b45;
    color: white;
    border-radius: 12px;
    padding: 25px;
    margin-top: 20px;
}}

.summary h2 {{
    margin-top: 0;
}}

.summary p {{
    color: #d5e0ed;
    font-size: 13px;
    line-height: 1.8;
}}

.footer {{
    text-align: center;
    padding: 25px;
    color: #94a3b8;
    font-size: 12px;
}}

@media (max-width: 900px) {{
    .metrics {{
        grid-template-columns: repeat(2, 1fr);
    }}

    .section-grid {{
        grid-template-columns: 1fr;
    }}
}}

@media (max-width: 500px) {{
    .metrics {{
        grid-template-columns: 1fr;
    }}

    .header h1 {{
        font-size: 23px;
    }}
}}
</style>
</head>

<body>

<header class="header">
    <h1>AI Incident Intelligence</h1>
    <p>Security, Compliance & Operational Analytics Command Center</p>
    <div class="header-tag">
        INCIDENT MONITORING &bull; RISK VISIBILITY &bull; INTELLIGENCE
    </div>
</header>

<main class="container">

    <h2 class="section-title">Executive Overview</h2>

    <section class="metrics">
        {metric_cards}
    </section>

    <h2 class="section-title">Incident Analytics</h2>

    <section class="section-grid">

        <div class="panel">
            <h2>Severity Distribution</h2>
            {severity_bars}
        </div>

        <div class="panel">
            <h2>Category Distribution</h2>
            {category_bars}
        </div>

    </section>

    <section class="section-grid">

        <div class="panel">
            <h2>Severity Analysis</h2>
            <table>
                <tr><th>Severity</th><th>Count</th></tr>
                {severity_rows}
            </table>
        </div>

        <div class="panel">
            <h2>Category Analysis</h2>
            <table>
                <tr><th>Category</th><th>Count</th></tr>
                {category_rows}
            </table>
        </div>

    </section>

    <h2 class="section-title">Risk & Intelligence</h2>

    <section class="section-grid">

        <div class="panel">
            <h2>Recurring Issues</h2>
            <table>
                <tr><th>Issue</th><th>Occurrences</th></tr>
                {recurring_rows}
            </table>
        </div>

        <div class="panel">
            <h2>Security Concerns</h2>
            <ul>{security_rows}</ul>
        </div>

    </section>

    <section class="section-grid">

        <div class="panel">
            <h2>Compliance Concerns</h2>
            <ul>{compliance_rows}</ul>
        </div>

        <div class="panel">
            <h2>Preventive Actions</h2>
            <ul>{preventive_rows}</ul>
        </div>

    </section>

    <section class="summary">
        <h2>Management Summary</h2>
        <p>
            This dashboard summarizes the current incident dataset,
            highlighting incident severity, recurring patterns,
            potential security concerns and potential compliance concerns.
        </p>
        <p>
            Security and compliance findings are indicators for investigation.
            They are not formal compliance determinations and require
            appropriate human review.
        </p>
    </section>

</main>

<footer class="footer">
    AI Incident Intelligence & Compliance Assistant
    &bull; Operational Analytics Dashboard
</footer>

</body>
</html>
"""

    DASHBOARD_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(DASHBOARD_FILE, "w", encoding="utf-8") as file:
        file.write(html)

    print(f"Dashboard generated: {DASHBOARD_FILE}")


def main():
    report = load_report()
    generate_dashboard(report)


if __name__ == "__main__":
    main()
