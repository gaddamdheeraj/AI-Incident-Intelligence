import unittest

from incident_analysis import analyze_incidents


class TestIncidentAnalysis(unittest.TestCase):

    def test_total_and_status_counts(self):
        incidents = [
            {
                "incident_id": "TEST-001",
                "severity": "High",
                "category": "Application",
                "issue": "Test issue",
                "status": "Open",
                "description": "Test incident",
                "resolution_time_minutes": 0
            },
            {
                "incident_id": "TEST-002",
                "severity": "Low",
                "category": "Infrastructure",
                "issue": "Another issue",
                "status": "Resolved",
                "description": "Test incident",
                "resolution_time_minutes": 20
            }
        ]

        result = analyze_incidents(incidents)

        self.assertEqual(result["total_incidents"], 2)
        self.assertEqual(result["open_incidents"], 1)
        self.assertEqual(result["resolved_incidents"], 1)

    def test_recurring_issue_detection(self):
        incidents = [
            {
                "incident_id": "TEST-001",
                "severity": "Medium",
                "category": "Application",
                "issue": "API timeout",
                "status": "Resolved",
                "description": "API timeout occurred",
                "resolution_time_minutes": 10
            },
            {
                "incident_id": "TEST-002",
                "severity": "High",
                "category": "Application",
                "issue": "API timeout",
                "status": "Resolved",
                "description": "API timeout occurred again",
                "resolution_time_minutes": 20
            }
        ]

        result = analyze_incidents(incidents)

        self.assertEqual(
            result["recurring_issues"]["API timeout"],
            2
        )

    def test_security_and_compliance_detection(self):
        incidents = [
            {
                "incident_id": "TEST-SEC",
                "severity": "High",
                "category": "Security",
                "issue": "Failed login attempts",
                "status": "Open",
                "description": "Multiple failed logins",
                "resolution_time_minutes": 0
            },
            {
                "incident_id": "TEST-COMP",
                "severity": "High",
                "category": "Compliance",
                "issue": "Evidence missing",
                "status": "Open",
                "description": "Required evidence is missing",
                "resolution_time_minutes": 0
            }
        ]

        result = analyze_incidents(incidents)

        self.assertIn("TEST-SEC", result["security_concerns"])
        self.assertIn("TEST-COMP", result["compliance_concerns"])

    def test_average_resolution_time(self):
        incidents = [
            {
                "incident_id": "TEST-001",
                "severity": "Low",
                "category": "Application",
                "issue": "Issue A",
                "status": "Resolved",
                "description": "Test",
                "resolution_time_minutes": 20
            },
            {
                "incident_id": "TEST-002",
                "severity": "Medium",
                "category": "Application",
                "issue": "Issue B",
                "status": "Resolved",
                "description": "Test",
                "resolution_time_minutes": 40
            }
        ]

        result = analyze_incidents(incidents)

        self.assertEqual(
            result["average_resolution_time_minutes"],
            30
        )


if __name__ == "__main__":
    unittest.main()