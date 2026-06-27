import os
import requests

# -----------------------------------
# Hugging Face Configuration
# -----------------------------------
API_TOKEN = os.getenv("HF_API_TOKEN")

API_URL = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# -----------------------------------
# Read Security Reports
# -----------------------------------
reports = []

# Bandit Report
if os.path.exists("bandit-report.json"):
    with open("bandit-report.json", "r") as f:
        reports.append("===== BANDIT REPORT =====")
        reports.append(f.read())

# Trivy Report
if os.path.exists("trivy-report.json"):
    with open("trivy-report.json", "r") as f:
        reports.append("===== TRIVY REPORT =====")
        reports.append(f.read())

# Gitleaks Report
if os.path.exists("gitleaks-report.json"):
    with open("gitleaks-report.json", "r") as f:
        reports.append("===== GITLEAKS REPORT =====")
        reports.append(f.read())

combined_report = "\n\n".join(reports)

# -----------------------------------
# Build AI Prompt
# -----------------------------------
prompt = f"""
You are a Senior DevSecOps Security Engineer.

Analyze the following security reports and generate a professional security assessment.

Provide your response in the following format:

# AI SECURITY REPORT

## Overall Risk
(LOW / MEDIUM / HIGH / CRITICAL)

## Executive Summary

## Bandit Findings

## Trivy Findings

## Gitleaks Findings

## Root Cause Analysis

## Recommended Fixes

## Deployment Decision
(APPROVED or NOT APPROVED)

Security Reports:

{combined_report}
"""

# -----------------------------------
# Send Request to Hugging Face
# -----------------------------------
payload = {
    "model": "meta-llama/Llama-3.1-8B-Instruct",
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],
    "max_tokens": 800
}

response = requests.post(
    API_URL,
    headers=headers,
    json=payload
)

# -----------------------------------
# Process AI Response
# -----------------------------------
if response.status_code == 200:

    result = response.json()

    ai_report = result["choices"][0]["message"]["content"]

    print("\n===================================")
    print("      AI SECURITY REPORT")
    print("===================================\n")

    print(ai_report)

else:

    print("Error:", response.status_code)
    print(response.text)