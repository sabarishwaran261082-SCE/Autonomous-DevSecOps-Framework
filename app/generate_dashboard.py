import json
import os

decision_file = "deployment-decision.json"

if not os.path.exists(decision_file):
    raise FileNotFoundError("deployment-decision.json not found.")

with open(decision_file, "r", encoding="utf-8") as f:
    data = json.load(f)

dashboard = f"""
=====================================
🤖 AI SECURITY DASHBOARD
=====================================

Project               : {data['project']}

Security Score        : {data['security_score']}/100
Overall Risk          : {data['overall_risk']}
AI Confidence         : {data['confidence']}%

Deployment Decision   : {data['deployment_decision']}

Bandit Issues         : {data['bandit_issues']}
Trivy Vulnerabilities : {data['trivy_vulnerabilities']}
Secrets Found         : {data['gitleaks_secrets']}

Reason:
{data['reason']}

Generated At:
{data['generated_at']}
"""

with open("dashboard-summary.txt", "w", encoding="utf-8") as f:
    f.write(dashboard)

print(dashboard)
print("✅ dashboard-summary.txt generated successfully.")