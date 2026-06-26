import json
import os

print("========== SECURITY GATE ==========")

# -----------------------------
# Read Bandit Report
# -----------------------------
bandit_file = "bandit-report.json"

if os.path.exists(bandit_file):
    with open(bandit_file, "r") as file:
        bandit = json.load(file)

    print("Bandit report loaded successfully.")
else:
    print("Bandit report not found.")

# -----------------------------
# Read Trivy Report
# -----------------------------
trivy_file = "../trivy-report.json"

if os.path.exists(trivy_file):
    with open(trivy_file, "r") as file:
        trivy = json.load(file)

    print("Trivy report loaded successfully.")
else:
    print("Trivy report not found.")

# -----------------------------
# Read Gitleaks Report
# -----------------------------
gitleaks_file = "../gitleaks-report.json"

if os.path.exists(gitleaks_file):
    with open(gitleaks_file, "r") as file:
        gitleaks = json.load(file)

    print("Gitleaks report loaded successfully.")
else:
    print("Gitleaks report not found.")

print("===================================")