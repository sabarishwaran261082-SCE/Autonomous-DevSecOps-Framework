import json
import os

decision_file = "deployment-decision.json"
status_file = "deployment-status.json"

if not os.path.exists(decision_file):
    raise FileNotFoundError("deployment-decision.json not found.")

with open(decision_file, "r", encoding="utf-8") as f:
    decision = json.load(f)

status = {}

if os.path.exists(status_file):

    with open(status_file, "r", encoding="utf-8") as f:
        status = json.load(f)

dashboard = f"""
=====================================
🤖 AUTONOMOUS DEVSECOPS DASHBOARD
=====================================

Project               : {decision.get("project","Autonomous DevSecOps Framework")}

-------------------------------------
SECURITY
-------------------------------------

Security Score        : {decision.get("security_score",0)}/100
Overall Risk          : {decision.get("overall_risk","UNKNOWN")}
AI Confidence         : {decision.get("confidence",0)}%

Bandit Issues         : {decision.get("bandit_issues",0)}
Trivy Vulnerabilities : {decision.get("trivy_vulnerabilities",0)}
Secrets Found         : {decision.get("gitleaks_secrets",0)}

-------------------------------------
AI DECISION
-------------------------------------

Deployment Decision   : {decision.get("deployment_decision","UNKNOWN")}

Reason:
{decision.get("reason","No reason available.")}

-------------------------------------
DEPLOYMENT STATUS
-------------------------------------

Pipeline Status       : {status.get("pipeline","UNKNOWN")}

Deployment Status     : {status.get("status","UNKNOWN")}

Deployment Allowed    : {status.get("deployment_allowed",False)}

Application Health    : {status.get("health","NOT CHECKED")}

Deployment Result     : {status.get("deployment_result","PENDING")}

-------------------------------------

Generated At:

{decision.get("generated_at","-")}

=====================================
"""

with open(
    "dashboard-summary.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(dashboard)

print(dashboard)

print("✅ dashboard-summary.txt generated successfully.")