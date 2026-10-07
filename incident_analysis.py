import json
from collections import Counter

INPUT_FILE = "data/incidents.json"
OUTPUT_FILE = "output/incident_report.json"


def load_incidents():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def analyze_incidents(incidents):
    total = len(incidents)

    open_incidents = [
        incident for incident in incidents
        if incident["status"].lower() == "open"
    ]

    resolved_incidents = [
        incident for incident in incidents
        if incident["status"].lower() == "resolved"
    ]

    resolution_times = [
        incident["resolution_time_minutes"]
        for incident in incidents
        if incident["resolution_time_minutes"] > 0
    ]

    average_resolution_time = (
        sum(resolution_times) / len(resolution_times)
        if resolution_times
        else 0
    )

    severity_counts = Counter(
        incident["severity"] for incident in incidents
    )

    category_counts = Counter(
        incident["category"] for incident in incidents
    )

    issue_counts = Counter(
        incident["issue"] for incident in incidents
    )

    recurring_issues = {
        issue: count
        for issue, count in issue_counts.items()
        if count > 1
    }

    security_concerns = [
        incident["incident_id"]
        for incident in incidents
        if incident["category"].lower() == "security"
    ]

    compliance_concerns = [
        incident["incident_id"]
        for incident in incidents
        if incident["category"].lower() == "compliance"
    ]

    preventive_actions = []

    if recurring_issues:
        preventive_actions.append(
            "Investigate recurring issues and identify preventive controls "
            "to reduce repeated incidents."
        )

    if security_concerns:
        preventive_actions.append(
            "Review authentication activity and investigate the security "
            "incidents identified in the report."
        )

    if compliance_concerns:
        preventive_actions.append(
            "Review missing access-review evidence and strengthen the "
            "evidence collection and review process."
        )

    dashboard_metrics = {
        "total_issues": total,
        "open_issues": len(open_incidents),
        "resolved_issues": len(resolved_incidents),
        "high_severity_issues": severity_counts.get("High", 0),
        "recurring_issue_types": len(recurring_issues),
        "security_flags": len(security_concerns),
        "compliance_flags": len(compliance_concerns),
        "average_resolution_time_minutes": round(
            average_resolution_time, 2
        )
    }

    return {
        "dashboard_metrics": dashboard_metrics,
        "total_incidents": total,
        "open_incidents": len(open_incidents),
        "resolved_incidents": len(resolved_incidents),
        "average_resolution_time_minutes": round(
            average_resolution_time, 2
        ),
        "severity_counts": dict(severity_counts),
        "category_counts": dict(category_counts),
        "recurring_issues": recurring_issues,
        "security_concerns": security_concerns,
        "compliance_concerns": compliance_concerns,
        "preventive_actions": preventive_actions,
    }


def save_report(results):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)

    print(f"\nReport saved to: {OUTPUT_FILE}")


def main():
    incidents = load_incidents()
    results = analyze_incidents(incidents)

    print("\n=== AI INCIDENT INTELLIGENCE REPORT ===")

    print("\nDashboard Metrics:")

    metrics = results["dashboard_metrics"]

    print(f"  Total Issues: {metrics['total_issues']}")
    print(f"  Open Issues: {metrics['open_issues']}")
    print(f"  Resolved Issues: {metrics['resolved_issues']}")
    print(f"  High Severity Issues: {metrics['high_severity_issues']}")
    print(f"  Recurring Issue Types: {metrics['recurring_issue_types']}")
    print(f"  Security Flags: {metrics['security_flags']}")
    print(f"  Compliance Flags: {metrics['compliance_flags']}")
    print(
        "  Average Resolution Time: "
        f"{metrics['average_resolution_time_minutes']} minutes"
    )

    print("\nSeverity Analysis:")
    for severity, count in results["severity_counts"].items():
        print(f"  {severity}: {count}")

    print("\nCategory Analysis:")
    for category, count in results["category_counts"].items():
        print(f"  {category}: {count}")

    print("\nRecurring Issues:")
    if results["recurring_issues"]:
        for issue, count in results["recurring_issues"].items():
            print(f"  {issue}: {count} occurrences")
    else:
        print("  None identified")

    print("\nPotential Security Concerns:")
    if results["security_concerns"]:
        for incident_id in results["security_concerns"]:
            print(f"  {incident_id} - requires investigation")
    else:
        print("  None identified")

    print("\nPotential Compliance Concerns:")
    if results["compliance_concerns"]:
        for incident_id in results["compliance_concerns"]:
            print(f"  {incident_id} - requires human review")
    else:
        print("  None identified")

    print("\nPreventive Actions:")
    if results["preventive_actions"]:
        for action in results["preventive_actions"]:
            print(f"  - {action}")
    else:
        print("  None identified")

    save_report(results)


if __name__ == "__main__":
    main()