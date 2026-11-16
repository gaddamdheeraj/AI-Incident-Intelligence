
import json
from pathlib import Path
from html import escape

PROJECT_DIR = Path(__file__).resolve().parent
REPORT_FILE = PROJECT_DIR / "output" / "incident_report.json"
INCIDENTS_FILE = PROJECT_DIR / "data" / "incidents.json"
DASHBOARD_FILE = PROJECT_DIR / "output" / "incident_dashboard.html"


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def safe(value):
    return escape(str(value))


def generate_dashboard(report, incidents):

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

    # Severity distribution table
    severity_rows = ""

    for severity, count in report["severity_counts"].items():
        color = severity_colors.get(severity, "#64748b")

        severity_rows += f"""
        <tr>
            <td>
                <span class="dot" style="background:{color}"></span>
                {safe(severity)}
            </td>
            <td><strong>{count}</strong></td>
        </tr>
        """

    # Category distribution table
    category_rows = ""

    for index, (category, count) in enumerate(
        report["category_counts"].items()
    ):
        color = category_colors[index % len(category_colors)]

        category_rows += f"""
        <tr>
            <td>
                <span class="dot" style="background:{color}"></span>
                {safe(category)}
            </td>
            <td><strong>{count}</strong></td>
        </tr>
        """

    # Distribution bars
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
        [
            severity_colors.get(s, "#64748b")
            for s in report["severity_counts"]
        ]
    )

    category_bars = make_bars(
        report["category_counts"],
        category_colors
    )

    # Recurring issues
    def make_table_rows(data):
        if not data:
            return '<tr><td colspan="2">No records identified</td></tr>'

        return "".join(
            f"<tr><td>{safe(name)}</td>"
            f"<td><strong>{count}</strong></td></tr>"
            for name, count in data.items()
        )

    recurring_rows = make_table_rows(report["recurring_issues"])

    # Recent incidents: latest five records in the JSON file
    recent_incident_rows = ""

    recent_incidents = incidents[-5:]

    if recent_incidents:
        for incident in reversed(recent_incidents):

            severity = str(incident.get("severity", "Unknown"))
            status = str(incident.get("status", "Unknown"))

            severity_class = {
                "Critical": "critical",
                "High": "high",
                "Medium": "medium",
                "Low": "low"
            }.get(severity, "neutral")

            status_class = {
                "Open": "status-open",
                "Resolved": "status-resolved",
                "In Progress": "status-progress"
            }.get(status, "status-neutral")

            recent_incident_rows += f"""
            <tr>
                <td><strong>{safe(incident.get("incident_id", "N/A"))}</strong></td>
                <td>
                    <span class="severity-badge {severity_class}">
                        {safe(severity)}
                    </span>
                </td>
                <td>{safe(incident.get("category", "N/A"))}</td>
                <td>{safe(incident.get("issue", "N/A"))}</td>
                <td>
                    <span class="status-badge {status_class}">
                        {safe(status)}
                    </span>
                </td>
            </tr>
            """
    else:
        recent_incident_rows = """
        <tr>
            <td colspan="5">No incidents available</td>
        </tr>
        """

    # Security concerns
    security_rows = "".join(
        f"""
        <li>
            <span class="status-dot danger"></span>
            <strong>{safe(incident_id)}</strong>
            <span class="review-label">Requires investigation</span>
        </li>
        """
        for incident_id in report["security_concerns"]
    ) or "<li>No security concerns identified</li>"

    # Compliance concerns
    compliance_rows = "".join(
        f"""
        <li>
            <span class="status-dot warning"></span>
            <strong>{safe(incident_id)}</strong>
            <span class="review-label">Requires human review</span>
        </li>
        """
        for incident_id in report["compliance_concerns"]
    ) or "<li>No compliance concerns identified</li>"

    # Preventive actions
    preventive_rows = "".join(
        f"<li>{safe(action)}</li>"
        for action in report["preventive_actions"]
    ) or "<li>No preventive actions identified</li>"

    # KPI cards
    cards = [
        ("Total Issues", metrics["total_issues"], "blue", "TI"),
        ("Open Issues", metrics["open_issues"], "orange", "OI"),
        ("High Severity", metrics["high_severity_issues"], "red", "HS"),
        ("Resolved Issues", metrics["resolved_issues"], "green", "RI"),
        ("Recurring Types", metrics["recurring_issue_types"], "purple", "RT"),
        ("Security Flags", metrics["security_flags"], "red", "SF"),
        ("Compliance Flags", metrics["compliance_flags"], "orange", "CF"),
        (
            "Avg Resolution Time",
            f'{metrics["average_resolution_time_minutes"]} min',
            "blue",
            "AT"
        )
    ]

    metric_cards = "".join(
        f"""
        <article class="metric-card">
            <div class="metric-top">
                <span class="metric-icon {color}">{icon}</span>
                <span class="metric-label">{safe(label)}</span>
            </div>
            <div class="metric-value">{safe(value)}</div>
        </article>
        """
        for label, value, color, icon in cards
    )

    # HTML dashboard
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>AI Incident Intelligence | Command Center</title>

<style>
* {{
    box-sizing: border-box;
}}

:root {{
    --navy: #142b45;
    --blue: #2563eb;
    --background: #f5f7fb;
    --surface: #ffffff;
    --text: #172b45;
    --muted: #718096;
    --border: #e5eaf1;
}}

body {{
    margin: 0;
    font-family: "Segoe UI", Arial, sans-serif;
    background: var(--background);
    color: var(--text);
}}

.app {{
    display: flex;
    min-height: 100vh;
}}

.sidebar {{
    width: 250px;
    flex-shrink: 0;
    background: var(--navy);
    color: white;
    padding: 28px 18px;
    display: flex;
    flex-direction: column;
}}

.brand {{
    padding: 0 12px 28px;
    border-bottom: 1px solid #ffffff20;
}}

.brand-mark {{
    width: 38px;
    height: 38px;
    background: #2563eb;
    border-radius: 10px;
    display: grid;
    place-items: center;
    font-weight: 800;
    margin-bottom: 14px;
}}

.brand h1 {{
    font-size: 17px;
    line-height: 1.4;
    margin: 0;
}}

.brand p {{
    font-size: 11px;
    color: #b9c8d9;
    margin: 7px 0 0;
    line-height: 1.5;
}}

.nav-label {{
    color: #8fa5bd;
    font-size: 10px;
    letter-spacing: 1.2px;
    font-weight: 700;
    padding: 26px 12px 10px;
}}

.nav-link {{
    display: block;
    padding: 12px;
    margin: 3px 0;
    border-radius: 7px;
    color: #d6e0ec;
    font-size: 13px;
    text-decoration: none;
}}

.nav-link:hover,
.nav-link.active {{
    background: #ffffff18;
    color: white;
}}

.sidebar-note {{
    margin-top: auto;
    border-top: 1px solid #ffffff20;
    padding: 18px 10px 0;
    color: #b9c8d9;
    font-size: 11px;
    line-height: 1.7;
}}

.main {{
    flex: 1;
    min-width: 0;
}}

.topbar {{
    height: 70px;
    padding: 0 36px;
    background: white;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
}}

.topbar-title {{
    font-size: 14px;
    font-weight: 700;
}}

.live-status {{
    font-size: 11px;
    color: #15803d;
    background: #ecfdf3;
    border: 1px solid #bbf7d0;
    border-radius: 20px;
    padding: 7px 12px;
}}

.live-status span {{
    display: inline-block;
    width: 7px;
    height: 7px;
    background: #16a34a;
    border-radius: 50%;
    margin-right: 6px;
}}

.content {{
    width: 100%;
    max-width: 1500px;
    margin: 0 auto;
    padding: 32px 36px 50px;
}}

.page-heading {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 20px;
    margin-bottom: 28px;
}}

.page-heading h2 {{
    margin: 0;
    font-size: 25px;
    letter-spacing: -.5px;
}}

.page-heading p {{
    color: var(--muted);
    margin: 8px 0 0;
    font-size: 13px;
}}

.section-title {{
    font-size: 15px;
    font-weight: 700;
    margin: 30px 0 15px;
}}

.metrics {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 16px;
}}

.metric-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 11px;
    padding: 19px;
    box-shadow: 0 2px 7px rgba(15, 23, 42, .025);
}}

.metric-top {{
    display: flex;
    align-items: center;
    gap: 10px;
}}

.metric-icon {{
    width: 32px;
    height: 32px;
    display: grid;
    place-items: center;
    border-radius: 8px;
    font-size: 11px;
    font-weight: 800;
}}

.metric-icon.blue {{ background: #eff6ff; color: #2563eb; }}
.metric-icon.orange {{ background: #fff7ed; color: #d97706; }}
.metric-icon.red {{ background: #fef2f2; color: #dc2626; }}
.metric-icon.green {{ background: #f0fdf4; color: #16a34a; }}
.metric-icon.purple {{ background: #f5f3ff; color: #7c3aed; }}

.metric-label {{
    color: #64748b;
    font-size: 12px;
    font-weight: 600;
}}

.metric-value {{
    font-size: 27px;
    font-weight: 750;
    letter-spacing: -.5px;
    margin-top: 16px;
}}

.section-grid {{
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 18px;
    margin-bottom: 18px;
}}

.panel {{
    background: white;
    border: 1px solid var(--border);
    border-radius: 11px;
    padding: 22px;
    box-shadow: 0 2px 7px rgba(15, 23, 42, .025);
    min-width: 0;
}}

.panel h3 {{
    margin: 0 0 22px;
    font-size: 14px;
}}

.bar-item {{
    margin-bottom: 20px;
}}

.bar-item:last-child {{
    margin-bottom: 0;
}}

.bar-heading {{
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    margin-bottom: 9px;
}}

.bar-heading strong {{
    color: #334155;
}}

.bar-track {{
    height: 8px;
    background: #edf1f6;
    border-radius: 20px;
    overflow: hidden;
}}

.bar-fill {{
    height: 100%;
    border-radius: 20px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th, td {{
    text-align: left;
    padding: 12px 10px;
    border-bottom: 1px solid #edf0f4;
    font-size: 12px;
}}

th {{
    background: #f8fafc;
    color: #64748b;
    font-weight: 600;
}}

.dot {{
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 8px;
}}

ul {{
    padding-left: 0;
    margin: 0;
    list-style: none;
}}

li {{
    padding: 12px 0;
    border-bottom: 1px solid #edf0f4;
    color: #475569;
    font-size: 12px;
    line-height: 1.6;
}}

li:last-child {{
    border-bottom: 0;
}}

.status-dot {{
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 9px;
}}

.danger {{ background: #dc2626; }}
.warning {{ background: #f59e0b; }}

.review-label {{
    display: block;
    color: #94a3b8;
    font-size: 11px;
    padding-left: 18px;
}}

.severity-badge,
.status-badge {{
    display: inline-block;
    padding: 4px 8px;
    border-radius: 5px;
    font-size: 11px;
    font-weight: 600;
}}

.critical {{ background: #f5f3ff; color: #7c3aed; }}
.high {{ background: #fef2f2; color: #dc2626; }}
.medium {{ background: #fff7ed; color: #c2410c; }}
.low {{ background: #f0fdf4; color: #15803d; }}
.neutral {{ background: #f1f5f9; color: #64748b; }}

.status-open {{ background: #fef2f2; color: #dc2626; }}
.status-resolved {{ background: #f0fdf4; color: #15803d; }}
.status-progress {{ background: #eff6ff; color: #2563eb; }}
.status-neutral {{ background: #f1f5f9; color: #64748b; }}

.recent-panel {{
    overflow-x: auto;
}}

.recent-panel table {{
    min-width: 650px;
}}

.summary {{
    background: white;
    border: 1px solid var(--border);
    border-left: 4px solid var(--blue);
    border-radius: 10px;
    padding: 22px;
    margin-top: 20px;
}}

.summary h3 {{
    margin: 0 0 12px;
    font-size: 14px;
}}

.summary p {{
    color: #64748b;
    font-size: 12px;
    line-height: 1.8;
    margin: 7px 0;
}}

.footer {{
    text-align: center;
    padding: 24px;
    color: #94a3b8;
    font-size: 11px;
}}

@media (max-width: 1050px) {{
    .sidebar {{
        width: 205px;
    }}

    .content {{
        padding: 26px 22px;
    }}

    .metrics {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }}
}}

@media (max-width: 700px) {{
    .app {{
        display: block;
    }}

    .sidebar {{
        width: 100%;
        padding: 15px;
    }}

    .brand {{
        padding-bottom: 12px;
    }}

    .nav-label,
    .sidebar-note {{
        display: none;
    }}

    .nav-link {{
        display: inline-block;
        padding: 9px;
    }}

    .topbar {{
        padding: 0 18px;
    }}

    .content {{
        padding: 22px 15px;
    }}

    .page-heading {{
        display: block;
    }}

    .section-grid {{
        grid-template-columns: 1fr;
    }}

    .metrics {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 10px;
    }}

    .metric-card {{
        padding: 14px;
    }}

    .metric-value {{
        font-size: 23px;
    }}
}}

@media (max-width: 390px) {{
    .metrics {{
        grid-template-columns: 1fr;
    }}
}}
</style>
</head>

<body>
<div class="app">

<aside class="sidebar">
    <div class="brand">
        <div class="brand-mark">AI</div>
        <h1>Incident Intelligence</h1>
        <p>Security, Compliance & Operations</p>
    </div>

    <div class="nav-label">WORKSPACE</div>
    <a class="nav-link active" href="#overview">Executive Overview</a>
    <a class="nav-link" href="#analytics">Incident Analytics</a>
    <a class="nav-link" href="#recent">Recent Incidents</a>
    <a class="nav-link" href="#risks">Risk Intelligence</a>
    <a class="nav-link" href="#actions">Preventive Actions</a>

    <div class="sidebar-note">
        AI Incident Intelligence<br>
        Operational Command Center<br><br>
        Security and compliance findings require human review.
    </div>
</aside>

<div class="main">

    <header class="topbar">
        <div class="topbar-title">Incident Operations Workspace</div>
        <div class="live-status"><span></span>Dashboard Generated</div>
    </header>

    <main class="content">

        <div class="page-heading">
            <div>
                <h2>Executive Overview</h2>
                <p>Monitor operational incidents, recurring issues and organizational risk.</p>
            </div>
        </div>

        <section id="overview">
            <div class="metrics">
                {metric_cards}
            </div>
        </section>

        <section id="analytics">
            <h2 class="section-title">Incident Analytics</h2>

            <div class="section-grid">
                <article class="panel">
                    <h3>Severity Distribution</h3>
                    {severity_bars}
                </article>

                <article class="panel">
                    <h3>Category Distribution</h3>
                    {category_bars}
                </article>
            </div>

            <div class="section-grid">
                <article class="panel">
                    <h3>Severity Analysis</h3>
                    <table>
                        <tr><th>Severity</th><th>Count</th></tr>
                        {severity_rows}
                    </table>
                </article>

                <article class="panel">
                    <h3>Category Analysis</h3>
                    <table>
                        <tr><th>Category</th><th>Count</th></tr>
                        {category_rows}
                    </table>
                </article>
            </div>
        </section>

        <section id="recent">
            <h2 class="section-title">Recent Incidents</h2>

            <article class="panel recent-panel">
                <table>
                    <tr>
                        <th>Incident ID</th>
                        <th>Severity</th>
                        <th>Category</th>
                        <th>Issue</th>
                        <th>Status</th>
                    </tr>
                    {recent_incident_rows}
                </table>
            </article>
        </section>

        <section id="risks">
            <h2 class="section-title">Risk & Intelligence</h2>

            <div class="section-grid">
                <article class="panel">
                    <h3>Recurring Issues</h3>
                    <table>
                        <tr><th>Issue</th><th>Occurrences</th></tr>
                        {recurring_rows}
                    </table>
                </article>

                <article class="panel">
                    <h3>Security Concerns</h3>
                    <ul>{security_rows}</ul>
                </article>
            </div>

            <div class="section-grid">
                <article class="panel">
                    <h3>Compliance Concerns</h3>
                    <ul>{compliance_rows}</ul>
                </article>

                <article class="panel" id="actions">
                    <h3>Preventive Actions</h3>
                    <ul>{preventive_rows}</ul>
                </article>
            </div>
        </section>

        <section class="summary">
            <h3>Management Summary</h3>
            <p>
                This dashboard summarizes the current incident dataset,
                highlighting severity, recurring patterns, potential security
                concerns and potential compliance concerns.
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
        &bull; Operational Analytics Command Center
    </footer>

</div>
</div>
</body>
</html>
"""

    DASHBOARD_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(DASHBOARD_FILE, "w", encoding="utf-8") as file:
        file.write(html)

    print(f"Dashboard generated: {DASHBOARD_FILE}")


def main():
    report = load_json(REPORT_FILE)
    incidents = load_json(INCIDENTS_FILE)
    generate_dashboard(report, incidents)


if __name__ == "__main__":
    main()
