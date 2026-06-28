import json
import os

# -----------------------------------
# File Paths
# -----------------------------------
decision_file = "deployment-decision.json"
history_file = "deployment-history.json"

# -----------------------------------
# Check if deployment decision exists
# -----------------------------------
if not os.path.exists(decision_file):
    raise FileNotFoundError("deployment-decision.json not found.")

# -----------------------------------
# Read latest deployment decision
# -----------------------------------
with open(decision_file, "r", encoding="utf-8") as f:
    deployment = json.load(f)

# -----------------------------------
# Load existing history
# -----------------------------------
history = []

if os.path.exists(history_file):
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)

            # Safety check
            if not isinstance(history, list):
                history = []

    except json.JSONDecodeError:
        history = []

# -----------------------------------
# Append latest deployment
# -----------------------------------
history.append(deployment)

# -----------------------------------
# Keep only the last 20 deployments
# -----------------------------------
MAX_HISTORY = 20
history = history[-MAX_HISTORY:]

# -----------------------------------
# Save updated history
# -----------------------------------
with open(history_file, "w", encoding="utf-8") as f:
    json.dump(history, f, indent=4)

print("===================================")
print("AI DEPLOYMENT HISTORY UPDATED")
print("===================================")
print(f"Total Records : {len(history)}")
print("Saved as deployment-history.json")