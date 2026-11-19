# AI Incident Intelligence & Compliance Assistant

An automated incident intelligence solution that captures operational incidents from Slack, analyzes security and compliance risks, generates management insights, and publishes a live dashboard.

**Live Dashboard:** https://gaddamdheeraj.github.io/AI-Incident-Intelligence/

**GitHub Repository:** https://github.com/gaddamdheeraj/AI-Incident-Intelligence

## 1. Business Problem

Organizations receive many operational incident reports through communication platforms. Manually reviewing incidents, identifying recurring issues, tracking security concerns, and preparing management reports takes time.

This project automates incident collection, analysis, reporting, and dashboard publishing to improve operational visibility and reduce repetitive work.

## 2. Key Features

- Slack-based incident capture.
- Incident validation and duplicate prevention.
- Automated severity and category analysis.
- Identification of recurring incident patterns.
- Potential security and compliance flags.
- JSON-based incident intelligence reports.
- Interactive HTML management dashboard.
- Automatic GitHub Pages dashboard publishing.
- Claude Incident Intelligence Skill for additional analytical insights.

## 3. Architecture

```text
Slack Channel
     |
     v
Python Slack Bolt Application
     |
     v
Incident Validation & Parsing
     |
     v
data/incidents.json
     |
     v
Incident Analysis Engine
     |
     v
output/incident_report.json
     |
     v
Dashboard Generator
     |
     v
index.html
     |
     v
Git Commit & Push
     |
     v
GitHub Pages Live Dashboard
     |
     v
Slack Confirmation
```

## 4. Technology Stack

| Component | Technology |
|---|---|
| Programming | Python |
| Slack integration | Slack Bolt, Socket Mode |
| Data storage | JSON |
| Analysis | Python |
| Dashboard | HTML, CSS, JavaScript |
| Automation | PowerShell |
| Version control | Git, GitHub |
| Hosting | GitHub Pages |
| AI analysis skill | Claude Skill |

## 5. Slack Incident Format

Send incidents in the configured Slack channel using this format:

```text
INCIDENT-015 | High | Security | Open | Suspicious login activity detected
```

Supported severity values:
- Low
- Medium
- High
- Critical

Supported statuses:
- Open
- Resolved

The application validates incoming records, rejects duplicate incident IDs, stores valid incidents, and triggers the reporting workflow.

## 6. Automated Workflow

1. The Slack application listens for incident messages.
2. It validates the incident format and required fields.
3. Valid incidents are stored in the JSON data file.
4. The Python analysis engine calculates incident metrics.
5. The dashboard generator creates an updated HTML dashboard.
6. The generated dashboard is copied to `index.html`.
7. Git publishes the updated dashboard to GitHub Pages.
8. Slack receives a confirmation message.

**Note:** The Slack listener runs locally and must remain active to capture new messages. The published dashboard remains accessible when the listener is stopped.

## 7. Claude Incident Intelligence Skill

A separate Claude Skill analyzes incident records and produces structured intelligence, including:

- Incident summaries.
- Severity and category analysis.
- Recurring issue patterns.
- Potential security concerns.
- Potential compliance concerns.
- Operational risks.
- Preventive recommendations.
- Management summaries.

**Current implementation:** The Claude Skill has been tested separately using the incident dataset. It is not automatically invoked by the Slack application.

## ## 8. Project Structure

```text
AI-Incident-Intelligence/
|
|-- .claude/
|   |-- skills/
|       |-- incident-intelligence/
|           |-- SKILL.md
|
|-- .github/
|   |-- workflows/
|       |-- dashboard.yml
|
|-- data/
|   |-- incidents.json
|
|-- output/
|   |-- incident_report.json
|   |-- incident_job.log
|   |-- incident_dashboard.html
|
|-- dashboard_generator.py
|-- incident_analysis.py
|-- run_incident_job.ps1
|-- slack_app.py
|-- test_incident_analysis.py
|-- README.md
|-- index.html
```

## 9. Setup and Execution

### Prerequisites

- Python 3
- Git
- Slack application with required bot and app permissions
- GitHub repository configured for GitHub Pages

### Install dependencies

```powershell
python -m pip install slack-bolt python-dotenv
```

### Configure environment variables

Create a `.env` file in the project root:

```text
SLACK_BOT_TOKEN=your_bot_token
SLACK_APP_TOKEN=your_app_token
```

Never commit `.env` or expose actual tokens.

### Start the Slack application

```powershell
python slack_app.py
```

Keep the application running to receive Slack incidents.

### Run the analysis job manually

```powershell
.\run_incident_job.ps1
```

## 10. Security and Reliability

- Credentials are stored in environment variables.
- `.env` is excluded through `.gitignore`.
- Raw incident data is not intentionally published to GitHub.
- Duplicate incident IDs are rejected.
- Incident fields are validated before processing.
- Security and compliance indicators are treated as potential concerns requiring human review, not proof of a breach or violation.

## 11. Current Limitations and Future Enhancements

Current limitations:
- The Slack listener depends on a locally running application.
- Incident data is stored in a JSON file.
- Claude Skill analysis is separate from the automated Slack workflow.

Potential enhancements:
- Deploy the Slack listener to a persistent cloud environment.
- Integrate Claude analysis into the automated workflow.
- Introduce a database for scalable incident storage.
- Add role-based access and authentication to the dashboard.
- Introduce time-based incident trend analytics when reliable timestamps are available.
- Add notifications for critical incidents.

## 12. Project Outcome

The solution demonstrates an end-to-end incident reporting workflow connecting Slack, Python automation, structured incident analysis, dashboard generation, GitHub publishing, and AI-assisted analytical reporting.

The goal is to improve incident visibility, reduce repetitive reporting work, and help teams identify operational risks proactively.
