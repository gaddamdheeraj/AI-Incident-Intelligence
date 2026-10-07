*---*

*name: incident-intelligence*

*description: Analyze structured operational incidents to identify severity patterns, recurring issues, potential security or compliance concerns, trends, and preventive actions. Use this skill when reviewing incident data or generating an incident intelligence report.*

*---*



*# Incident Intelligence Skill*



*## Purpose*



*Analyze operational incident data and produce a concise business intelligence report that helps teams identify recurring problems, security concerns, compliance concerns, and preventive actions.*



*## Input*



*Accept incident records containing, when available:*



*- Incident ID*

*- Severity*

*- Category*

*- Issue*

*- Status*

*- Description*

*- Resolution Time*



*## Analysis Rules*



*1. Count the total number of incidents.*

*2. Count incidents by severity.*

*3. Count incidents by category.*

*4. Identify recurring issues by comparing issue descriptions and issue types.*

*5. Identify potential security concerns when incidents involve security-related activity.*

*6. Identify potential compliance concerns when incidents indicate missing evidence, access review problems, control failures, or similar compliance-related conditions.*

*7. Calculate the average resolution time using incidents with a numeric resolution time greater than zero.*

*8. Identify open incidents that may require attention.*

*9. Recommend preventive actions based only on the supplied incident data.*

*10. Do not invent incidents, metrics, causes, business impact, or remediation results.*



*## Compliance and Security Handling*



*Use cautious language.*



*For example:*



*- "Potential security concern — requires investigation."*

*- "Potential compliance concern — requires human review."*



*Do not state that an incident is definitively a SOX violation, security breach, or compliance violation unless the input explicitly establishes that fact.*



*## Output Format*



*Return the analysis using these sections:*



*### Incident Summary*



*- Total incidents*

*- Open incidents*

*- Resolved incidents*

*- Average resolution time*



*### Severity Analysis*



*List the incident count for each severity.*



*### Category Analysis*



*List the incident count for each category.*



*### Recurring Issues*



*Identify issues that appear more than once and explain the evidence.*



*### Security Concerns*



*List potential security concerns and the incident IDs supporting them.*



*### Compliance Concerns*



*List potential compliance concerns and the incident IDs supporting them.*



*### Preventive Actions*



*Provide practical actions derived from the observed incident patterns.*



*### Management Summary*



*Provide a short summary of the most important findings.*



*## Reliability Rules*



*- Use only the supplied incident records.*

*- Preserve incident IDs exactly.*

*- Do not fabricate missing values.*

*- If required data is missing, explicitly state that it is unavailable.*

*- Show the evidence behind recurring, security, and compliance findings.*

*- Distinguish observed facts from recommendations.*

