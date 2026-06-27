import json
import os
import sys

decision_file = "deployment-decision.json"

if not os.path.exists(decision_file):
    print("❌ deployment-decision.json not found.")
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

# -----------------------------------
# AI Deployment Decision
# -----------------------------------

allowed = [
    "APPROVED",
    "APPROVED WITH CAUTION"
]

if decision["deployment_decision"] in allowed:
    print("✅ AI approved deployment.")
    sys.exit(0)

print("❌ AI blocked deployment.")
sys.exit(1)