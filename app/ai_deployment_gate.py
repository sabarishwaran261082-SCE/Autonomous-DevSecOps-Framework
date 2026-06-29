import json
import os
import sys
from datetime import datetime

decision_file = "deployment-decision.json"

if not os.path.exists(decision_file):
    print("❌ deployment-decision.json not found.")

    status = {
        "status": "FAILED",
        "deployment_allowed": False,
        "decision": "UNKNOWN",
        "pipeline": "STOP",
        "timestamp": str(datetime.now())
    }

    with open("deployment-status.json", "w", encoding="utf-8") as f:
        json.dump(status, f, indent=4)

    sys.exit(1)

with open(decision_file, "r", encoding="utf-8") as f:
    decision = json.load(f)

print("\n===================================")
print("AI DEPLOYMENT GATE")
print("===================================\n")

print(f"Deployment Decision : {decision['deployment_decision']}")
print(f"Overall Risk        : {decision['overall_risk']}")
print(f"Security Score      : {decision['security_score']}")
print(f"Confidence          : {decision['confidence']}%")
print(f"Reason              : {decision['reason']}\n")

allowed = [
    "APPROVED",
    "APPROVED WITH CAUTION"
]

deployment_allowed = decision["deployment_decision"] in allowed

status = {
    "status": "SUCCESS" if deployment_allowed else "BLOCKED",
    "deployment_allowed": deployment_allowed,
    "decision": decision["deployment_decision"],
    "overall_risk": decision["overall_risk"],
    "security_score": decision["security_score"],
    "confidence": decision["confidence"],
    "reason": decision["reason"],
    "pipeline": "CONTINUE" if deployment_allowed else "STOP",
    "timestamp": str(datetime.now())
}

with open("deployment-status.json", "w", encoding="utf-8") as f:
    json.dump(status, f, indent=4)

print("✅ deployment-status.json generated.")

if deployment_allowed:
    print("✅ AI approved deployment.")
    sys.exit(0)

print("❌ AI blocked deployment.")
sys.exit(1)