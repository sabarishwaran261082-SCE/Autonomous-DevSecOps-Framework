import os
import json

summary = {}

# -----------------------------
# Bandit Summary
# -----------------------------
bandit_file = "bandit-report.json"

if os.path.exists(bandit_file):
    with open(bandit_file, "r") as f:
        bandit = json.load(f)

    summary["bandit"] = {
        "total_issues": len(bandit.get("results", [])),
        "metrics": bandit.get("metrics", {})
    }

# -----------------------------
# Trivy Summary
# -----------------------------
trivy_file = "trivy-report.json"

if os.path.exists(trivy_file):
    with open(trivy_file, "r") as f:
        trivy = json.load(f)

    vulnerabilities = 0

    for result in trivy.get("Results", []):
        vulnerabilities += len(result.get("Vulnerabilities", []))

    summary["trivy"] = {
        "total_vulnerabilities": vulnerabilities
    }

# -----------------------------
# Gitleaks Summary
# -----------------------------
gitleaks_file = "gitleaks-report.json"

if os.path.exists(gitleaks_file):
    with open(gitleaks_file, "r") as f:
        gitleaks = json.load(f)

    summary["gitleaks"] = {
        "total_secrets": len(gitleaks)
    }

# -----------------------------
# Save Summary
# -----------------------------
with open("security-summary.json", "w") as f:
    json.dump(summary, f, indent=4)

print("security-summary.json generated successfully.")