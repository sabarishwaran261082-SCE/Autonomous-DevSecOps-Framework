import json
import os
import sys

print("========== SECURITY GATE ==========\n")

# -----------------------------
# Bandit
# -----------------------------
bandit_high = 0

if os.path.exists("bandit-report.json"):
    with open("bandit-report.json", "r") as file:
        bandit = json.load(file)

    for issue in bandit.get("results", []):
        if issue.get("issue_severity") == "HIGH":
            bandit_high += 1
# -----------------------------
# Trivy
# -----------------------------
trivy_critical = 0

if os.path.exists("../trivy-report.json"):
    with open("../trivy-report.json", "r") as file:
        trivy = json.load(file)

    for result in trivy.get("Results", []):
        for vuln in result.get("Vulnerabilities", []):
            if vuln.get("Severity") == "CRITICAL":
                trivy_critical += 1
# -----------------------------
# Gitleaks
# -----------------------------
gitleaks_secrets = 0

if os.path.exists("../gitleaks-report.json"):
    with open("../gitleaks-report.json", "r") as file:
        gitleaks = json.load(file)

        if isinstance(gitleaks, list):
            gitleaks_secrets = len(gitleaks)

print(f"Bandit Issues          : {bandit_high}")
print(f"Trivy Vulnerabilities  : {trivy_critical}")
print(f"Gitleaks Secrets       : {gitleaks_secrets}")
print("\n===================================")

# -----------------------------------
# Security Decision
# -----------------------------------

if (
    bandit_high == 0
    and trivy_critical == 0
    and gitleaks_secrets == 0
):
    print("\n✅ SECURITY GATE PASSED")
else:
    print("\n❌ SECURITY GATE FAILED")
    print("Deployment Blocked!")
    sys.exit(1)