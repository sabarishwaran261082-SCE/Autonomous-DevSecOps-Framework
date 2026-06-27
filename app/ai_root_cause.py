import os
import json
import requests

# -----------------------------
# Hugging Face Configuration
# -----------------------------
API_TOKEN = os.getenv("HF_API_TOKEN")

API_URL = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# -----------------------------
# Read Security Reports
# -----------------------------
reports = []

# Bandit
if os.path.exists("bandit-report.json"):
    with open("bandit-report.json", "r") as f:
        reports.append("===== BANDIT REPORT =====")
        reports.append(f.read())

# Trivy
if os.path.exists("trivy-report.json"):
    with open("trivy-report.json", "r") as f:
        reports.append("===== TRIVY REPORT =====")
        reports.append(f.read())

# Gitleaks
if os.path.exists("gitleaks-report.json"):
    with open("gitleaks-report.json", "r") as f:
        reports.append("===== GITLEAKS REPORT =====")
        reports.append(f.read())

combined_report = "\n\n".join(reports)

print("Security reports loaded successfully.")
print("-----------------------------------")
print(combined_report[:1000])