# AI Incident Intelligence & Compliance Assistant

An AI-powered incident intelligence platform designed to analyze incidents, identify recurring issues, highlight security and compliance risks, and provide actionable insights through an automated dashboard.

## Overview

This project demonstrates how Slack integration, Python automation, Claude Code skills, and dashboard analytics can help teams reduce repetitive incident analysis and improve operational visibility.

## Key Features

- **Slack Integration:** Connect incident workflows with Slack.
- **Incident Analytics:** Analyze incident records and identify recurring issues.
- **Security Insights:** Highlight potential security concerns for investigation.
- **SOX & Compliance Awareness:** Identify incidents that may require compliance review.
- **Automated Job:** Run incident analysis and generate updated reports.
- **Interactive Dashboard:** Present incident metrics and insights in a centralized view.
- **Automated Updates:** Use GitHub Actions to support dashboard update workflows.
- **Testing:** Include sample incident data and automated analysis tests.

## Architecture
Slack
  |
  v
Incident Data
  |
  v
Python Incident Analysis
  |
  v
Automated Job
  |
  v
Metrics and Reports
  |
  v
Dashboard
  |
  v
Operational Insights

## Technology Stack

- Python
- HTML
- GitHub Actions
- Slack integration
- Claude Code skills
- Data analysis and dashboard reporting
- PowerShell automation

## Project Structure

| File or Folder | Purpose |
| `.claude/skills/incident-intelligence/` | Incident intelligence skill |
| `.github/workflows/` | Workflow automation |
| `data/` | Sample incident data |
| `incident_analysis.py` | Incident analysis logic |
| `dashboard_generator.py` | Dashboard generation |
| `index.html` | Dashboard interface |
| `slack_app.py` | Slack integration |
| `run_incident_job.ps1` | Job execution script |
| `test_incident_analysis.py` | Analysis tests |
| `test-incidents.md` | Sample incident scenarios |

## Business Value

- Reduces repetitive manual incident review.
- Helps teams recognize recurring incident patterns.
- Improves visibility into potential security and compliance concerns.
- Supports proactive recommendations to prevent future incidents.
- Makes incident metrics easier for teams to review.

## Running the Project

1. Clone or download this repository.
2. Install the Python dependencies required by the project.
3. Configure the required Slack credentials securely if using Slack features.
4. Review the sample incident data.
5. Run the incident analysis script.
6. Generate or refresh the dashboard using the project scripts.
7. Run the available tests to validate the analysis logic.

Check the project configuration and workflow files for the exact commands and environment requirements.

## Security Considerations

- Store API tokens and credentials in environment variables or GitHub Secrets.
- Never commit passwords, access tokens, or private incident information.
- Treat automated security and compliance findings as recommendations requiring appropriate review.
- Use authorized sample data when demonstrating the project publicly.

## Project Status

Developed as a practical portfolio project exploring incident intelligence, AI-assisted analysis, workflow automation, and operational dashboards.

## Author

**Dheeraj Reddy**

GitHub: [gaddamdheeraj](https://github.com/gaddamdheeraj)

---

*This project is intended for demonstration and learning. Actual compliance and security decisions require appropriate human review.*
