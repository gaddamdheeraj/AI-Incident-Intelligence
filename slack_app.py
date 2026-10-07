import os
import json

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


REPORT_FILE = "output/incident_report.json"


app = App(
    token=os.environ["SLACK_BOT_TOKEN"]
)


def load_report():
    with open(REPORT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def build_slack_summary(report):
    metrics = report["dashboard_metrics"]

    message = (
        "*AI Incident Intelligence Summary*\n\n"
        f"*Total Issues:* {metrics['total_issues']}\n"
        f"*Open Issues:* {metrics['open_issues']}\n"
        f"*Resolved Issues:* {metrics['resolved_issues']}\n"
        f"*High Severity:* {metrics['high_severity_issues']}\n"
        f"*Recurring Issue Types:* {metrics['recurring_issue_types']}\n"
        f"*Security Flags:* {metrics['security_flags']}\n"
        f"*Compliance Flags:* {metrics['compliance_flags']}\n"
        f"*Average Resolution Time:* "
        f"{metrics['average_resolution_time_minutes']} minutes\n\n"
    )

    message += "*Recurring Issues:*\n"

    if report["recurring_issues"]:
        for issue, count in report["recurring_issues"].items():
            message += f"• {issue} — {count} occurrences\n"
    else:
        message += "• None identified\n"

    message += "\n*Security Concerns:*\n"

    if report["security_concerns"]:
        for incident_id in report["security_concerns"]:
            message += (
                f"• {incident_id} — requires investigation\n"
            )
    else:
        message += "• None identified\n"

    message += "\n*Compliance Concerns:*\n"

    if report["compliance_concerns"]:
        for incident_id in report["compliance_concerns"]:
            message += (
                f"• {incident_id} — requires human review\n"
            )
    else:
        message += "• None identified\n"

    message += "\n*Preventive Actions:*\n"

    for action in report["preventive_actions"]:
        message += f"• {action}\n"

    return message


@app.command("/analyze-incidents")
def analyze_incidents_command(ack, respond):
    ack()

    try:
        report = load_report()
        summary = build_slack_summary(report)

        respond(
            response_type="in_channel",
            text=summary
        )

    except Exception as error:
        respond(
            response_type="in_channel",
            text=f"Incident analysis could not be completed: {error}"
        )


if __name__ == "__main__":
    handler = SocketModeHandler(
        app,
        os.environ["SLACK_APP_TOKEN"]
    )

    print("AI Incident Intelligence Slack App is running...")

    handler.start()