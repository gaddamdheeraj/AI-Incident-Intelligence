import json
from pathlib import Path

REPORT_FILE = Path("output/incident_report.json")
DASHBOARD_FILE = Path("output/incident_dashboard.html")


def load_report():
    with open(REPORT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_dashboard(report):
    metrics = report["dashboard_metrics"]

    severity_rows = ""
    for severity, count in report["severity_counts"].items():
        severity_rows += f"""
        <tr>
            <td>{severity}</td>
            <td>{count}</td>
        </tr>
        """

    category_rows = ""
    for category, count in report["category_counts"].items():
        category_rows += f"""
        <tr>
            <td>{category}</td>
            <td>{count}</td>
        </tr>
        """

    recurring_rows = ""
    for issue, count in report["recurring_issues"].items():
        recurring_rows += f"""
        <tr>
            <td>{issue}</td>
            <td>{count}</td>
        </tr>
        """

    if not recurring_rows:
        recurring_rows = """
        <tr>
            <td colspan="2">No recurring issues identified</td>
        </tr>
        """

    security_rows = ""
    for incident_id in report["security_concerns"]:
        security_rows += f"""
        <li>{incident_id} — requires investigation</li>
        """

    if not security_rows:
        security_rows = "<li>No security concerns identified</li>"

    compliance_rows = ""
    for incident_id in report["compliance_concerns"]:
        compliance_rows += f"""
        <li>{incident_id} — requires human review</li>
        """

    if not compliance_rows:
        compliance_rows = "<li>No compliance concerns identified</li>"

    preventive_rows = ""
    for action in report["preventive_actions"]:
        preventive_rows += f"""
        <li>{action}</li>
        """

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Incident Intelligence Dashboard</title>

    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 30px;
            background: #f4f6f8;
            color: #1f2937;
        }}

        h1 {{
            margin-bottom: 5px;
        }}

        .subtitle {{
            color: #6b7280;
            margin-bottom: 25px;
        }}

        .metrics {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 25px;
        }}

        .card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}

        .card h3 {{
            margin: 0 0 10px 0;
            font-size: 14px;
            color: #6b7280;
        }}

        .value {{
            font-size: 30px;
            font-weight: bold;
        }}

        .section-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        th, td {{
            padding: 10px;
            border-bottom: 1px solid #e5e7eb;
            text-align: left;
        }}

        th {{
            background: #f9fafb;
        }}

        ul {{
            padding-left: 20px;
        }}

        li {{
            margin-bottom: 10px;
        }}

        .full {{
            margin-bottom: 20px;
        }}

        @media (max-width: 900px) {{
            .metrics {{
                grid-template-columns: repeat(2, 1fr);
            }}

            .section-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>

<body>

    <h1>AI Incident Intelligence Dashboard</h1>

    <div class="subtitle">
        Operational incident analytics, security and compliance intelligence
    </div>

    <div class="metrics">

        <div class="card">
            <h3>Total Issues</h3>
            <div class="value">{metrics["total_issues"]}</div>
        </div>

        <div class="card">
            <h3>Open Issues</h3>
            <div class="value">{metrics["open_issues"]}</div>
        </div>

        <div class="card">
            <h3>High Severity Issues</h3>
            <div class="value">{metrics["high_severity_issues"]}</div>
        </div>

        <div class="card">
            <h3>Resolved Issues</h3>
            <div class="value">{metrics["resolved_issues"]}</div>
        </div>

        <div class="card">
            <h3>Recurring Issue Types</h3>
            <div class="value">{metrics["recurring_issue_types"]}</div>
        </div>

        <div class="card">
            <h3>Security Flags</h3>
            <div class="value">{metrics["security_flags"]}</div>
        </div>

        <div class="card">
            <h3>Compliance Flags</h3>
            <div class="value">{metrics["compliance_flags"]}</div>
        </div>

        <div class="card">
            <h3>Avg Resolution Time</h3>
            <div class="value">
                {metrics["average_resolution_time_minutes"]} min
            </div>
        </div>

    </div>

    <div class="section-grid">

        <div class="card">
            <h2>Severity Analysis</h2>

            <table>
                <tr>
                    <th>Severity</th>
                    <th>Count</th>
                </tr>

                {severity_rows}
            </table>
        </div>

        <div class="card">
            <h2>Category Analysis</h2>

            <table>
                <tr>
                    <th>Category</th>
                    <th>Count</th>
                </tr>

                {category_rows}
            </table>
        </div>

    </div>

    <div class="section-grid">

        <div class="card">
            <h2>Recurring Issues</h2>

            <table>
                <tr>
                    <th>Issue</th>
                    <th>Occurrences</th>
                </tr>

                {recurring_rows}
            </table>
        </div>

        <div class="card">
            <h2>Security Concerns</h2>

            <ul>
                {security_rows}
            </ul>
        </div>

    </div>

    <div class="section-grid">

        <div class="card">
            <h2>Compliance Concerns</h2>

            <ul>
                {compliance_rows}
            </ul>
        </div>

        <div class="card">
            <h2>Preventive Actions</h2>

            <ul>
                {preventive_rows}
            </ul>
        </div>

    </div>

    <div class="card full">
        <h2>Management Summary</h2>

        <p>
            The dashboard summarizes the current incident dataset and highlights
            recurring issues, security concerns, potential compliance concerns,
            and recommended preventive actions.
        </p>

        <p>
            Compliance and security findings require appropriate human review
            before any formal determination is made.
        </p>
    </div>

</body>
</html>
"""

    with open(DASHBOARD_FILE, "w", encoding="utf-8") as file:
        file.write(html)

    print(f"Dashboard generated: {DASHBOARD_FILE}")


def main():
    report = load_report()
    generate_dashboard(report)


if __name__ == "__main__":
    main()