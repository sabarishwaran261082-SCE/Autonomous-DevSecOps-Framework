import os
import json

summary = {
    "project": "Autonomous DevSecOps Framework",
    "generated_by": "GitHub Actions",
    "version": "1.0"
}

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
    critical = 0
    high = 0
    medium = 0
    low = 0

    for result in trivy.get("Results", []):
        vulns = result.get("Vulnerabilities", [])

        vulnerabilities += len(vulns)

        for vuln in vulns:
            severity = vuln.get("Severity", "")

            if severity == "CRITICAL":
                critical += 1
            elif severity == "HIGH":
                high += 1
            elif severity == "MEDIUM":
                medium += 1
            elif severity == "LOW":
                low += 1

    summary["trivy"] = {
        "total_vulnerabilities": vulnerabilities,
        "critical": critical,
        "high": high,
        "medium": medium,
        "low": low
    }

# -----------------------------
# Gitleaks Summary
# -----------------------------
gitleaks_file = "gitleaks-report.json"

if os.path.exists(gitleaks_file):
    with open(gitleaks_file, "r") as f:
        gitleaks = json.load(f)

    summary["gitleaks"] = {
        "total_secrets": len(gitleaks),
        "status": "No Secrets Found" if len(gitleaks) == 0 else "Secrets Detected"
    }

# -----------------------------
# Save Summary
# -----------------------------
with open("security-summary.json", "w") as f:
    json.dump(summary, f, indent=4)

print("✅ security-summary.json generated successfully.")