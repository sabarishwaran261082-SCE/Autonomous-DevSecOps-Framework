import json
import os

deployment_file = "deployment-decision.json"
audit_file = "audit-log.json"

if not os.path.exists(deployment_file):
    raise FileNotFoundError("deployment-decision.json not found.")

with open(deployment_file, "r", encoding="utf-8") as f:
    deployment = json.load(f)

audit = []

if os.path.exists(audit_file):

    try:
        with open(audit_file, "r", encoding="utf-8") as f:
            audit = json.load(f)

    except Exception:
        audit = []

record = {
    "run": len(audit) + 1,
    "generated_at": deployment["generated_at"],
    "score": deployment["security_score"],
    "risk": deployment["overall_risk"],
    "decision": deployment["deployment_decision"],
    "confidence": deployment["confidence"]
}

audit.append(record)

audit = audit[-50:]

with open(audit_file, "w", encoding="utf-8") as f:
    json.dump(audit, f, indent=4)

print("✅ audit-log.json updated.")