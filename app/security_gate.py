import json
import os

print("========== SECURITY GATE ==========\n")

# -----------------------------
# Bandit
# -----------------------------
bandit_issues = 0

if os.path.exists("bandit-report.json"):
    with open("bandit-report.json", "r") as file:
        bandit = json.load(file)
        bandit_issues = len(bandit.get("results", []))

print(f"Bandit Issues          : {bandit_issues}")

# -----------------------------
# Trivy
# -----------------------------
trivy_vulnerabilities = 0

if os.path.exists("../trivy-report.json"):
    with open("../trivy-report.json", "r") as file:
        trivy = json.load(file)

        for result in trivy.get("Results", []):
            trivy_vulnerabilities += len(result.get("Vulnerabilities", []))

print(f"Trivy Vulnerabilities  : {trivy_vulnerabilities}")

# -----------------------------
# Gitleaks
# -----------------------------
gitleaks_secrets = 0

if os.path.exists("../gitleaks-report.json"):
    with open("../gitleaks-report.json", "r") as file:
        gitleaks = json.load(file)

        if isinstance(gitleaks, list):
            gitleaks_secrets = len(gitleaks)

print(f"Gitleaks Secrets       : {gitleaks_secrets}")
print("\n===================================")

# -----------------------------------
# Security Decision
# -----------------------------------

if (
    bandit_issues == 0
    and trivy_vulnerabilities == 0
    and gitleaks_secrets == 0
):
    print("\n✅ SECURITY GATE PASSED")
else:
    print("\n❌ SECURITY GATE FAILED")