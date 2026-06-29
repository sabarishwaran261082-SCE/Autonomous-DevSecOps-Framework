import json
import os
from datetime import datetime

# -----------------------------------
# Files
# -----------------------------------
decision_file = "deployment-decision.json"
status_file = "deployment-status.json"
history_file = "deployment-history.json"

# -----------------------------------
# Check Files
# -----------------------------------
if not os.path.exists(decision_file):
    raise FileNotFoundError("deployment-decision.json not found.")

if not os.path.exists(status_file):
    raise FileNotFoundError("deployment-status.json not found.")

# -----------------------------------
# Read Deployment Decision
# -----------------------------------
with open(decision_file, "r", encoding="utf-8") as f:
    decision = json.load(f)

# -----------------------------------
# Read Deployment Status
# -----------------------------------
with open(status_file, "r", encoding="utf-8") as f:
    status = json.load(f)

# -----------------------------------
# Create Deployment Record
# -----------------------------------
deployment = {

    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

    "project": decision.get("project", "Autonomous DevSecOps Framework"),

    "security_score": decision.get("security_score", 0),

    "overall_risk": decision.get("overall_risk", "UNKNOWN"),

    "confidence": decision.get("confidence", 0),

    "deployment_decision": decision.get(
        "deployment_decision",
        "UNKNOWN"
    ),

    "deployment_status": status.get(
        "status",
        "UNKNOWN"
    ),

    "pipeline_status": status.get(
        "pipeline",
        "STOP"
    ),

    "deployment_allowed": status.get(
        "deployment_allowed",
        False
    ),

    "reason": decision.get(
        "reason",
        "No reason available."
    ),

    # Enterprise Fields
    "git_commit": os.getenv("GITHUB_SHA", "LOCAL_RUN"),

    "github_run": os.getenv("GITHUB_RUN_ID", "LOCAL"),

    "docker_image": os.getenv(
        "ECR_REPOSITORY",
        "local-image"
    ),

    "ec2_status":
        "DEPLOYED"
        if status.get("deployment_allowed")
        else "BLOCKED"
}

# -----------------------------------
# Load Existing History
# -----------------------------------
history = []

if os.path.exists(history_file):

    try:

        with open(history_file, "r", encoding="utf-8") as f:

            history = json.load(f)

            if not isinstance(history, list):
                history = []

    except Exception:
        history = []

# -----------------------------------
# Append Latest Deployment
# -----------------------------------
history.append(deployment)

# Keep latest 100 records
history = history[-100:]

# -----------------------------------
# Save History
# -----------------------------------
with open(history_file, "w", encoding="utf-8") as f:

    json.dump(history, f, indent=4)

print("\n===================================")
print("AI DEPLOYMENT HISTORY")
print("===================================")

print("Project             :", deployment["project"])
print("Deployment Decision :", deployment["deployment_decision"])
print("Deployment Status   :", deployment["deployment_status"])
print("Pipeline Status     :", deployment["pipeline_status"])
print("Security Score      :", deployment["security_score"])
print("Risk                :", deployment["overall_risk"])
print("Timestamp           :", deployment["timestamp"])
print("History Records     :", len(history))

print("\n✅ deployment-history.json updated successfully.")