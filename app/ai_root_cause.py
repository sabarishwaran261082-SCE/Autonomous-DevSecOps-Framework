import os
import json
import requests
from datetime import datetime

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
# Read Security Summary
# -----------------------------------
summary_file = "security-summary.json"

if not os.path.exists(summary_file):
    raise FileNotFoundError("security-summary.json not found.")

with open(summary_file, "r", encoding="utf-8") as f:
    security_summary = json.load(f)

# -----------------------------------
# Build AI Prompt
# -----------------------------------
prompt = f"""
You are a Senior DevSecOps Security Engineer.

Analyze the following security summary JSON.

Generate a professional security assessment.

Return the report in Markdown format.

Include:

# AI Security Report

## Overall Risk

## Executive Summary

## Root Cause Analysis

## Recommendations

## Deployment Decision

Security Summary:

{json.dumps(security_summary, indent=2)}
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
    "max_tokens": 700
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
    print("AI SECURITY REPORT")
    print("===================================\n")
    print(ai_report)

    # -----------------------------------
    # Save AI Markdown Report
    # -----------------------------------
    with open("ai-security-report.md", "w", encoding="utf-8") as report_file:
        report_file.write("# 🤖 AI Security Report\n\n")
        report_file.write(ai_report)

    print("\n✅ ai-security-report.md generated successfully.")

    # -----------------------------------
    # Read Security Metrics
    # -----------------------------------
    bandit_issues = security_summary.get("bandit", {}).get("total_issues", 0)

    trivy_vulnerabilities = security_summary.get("trivy", {}).get(
        "total_vulnerabilities", 0
    )

    gitleaks_secrets = security_summary.get("gitleaks", {}).get(
        "total_secrets", 0
    )

    critical = security_summary.get("trivy", {}).get("critical", 0)
    high = security_summary.get("trivy", {}).get("high", 0)
    medium = security_summary.get("trivy", {}).get("medium", 0)
    low = security_summary.get("trivy", {}).get("low", 0)

    # -----------------------------------
    # Calculate Security Score
    # -----------------------------------
    security_score = 100

    security_score -= bandit_issues * 5
    security_score -= critical * 20
    security_score -= high * 10
    security_score -= medium * 5
    security_score -= low * 2
    security_score -= gitleaks_secrets * 20

    security_score = max(security_score, 0)

    # -----------------------------------
    # Default Deployment Object
    # -----------------------------------
    deployment = {
        "project": "Autonomous DevSecOps Framework",
        "generated_at": datetime.now().astimezone().isoformat(),

        "overall_risk": "LOW",
        "security_score": security_score,
        "confidence": 98,

        "deployment_decision": "APPROVED",
        "reason": "No critical vulnerabilities detected.",

        "bandit_issues": bandit_issues,
        "trivy_vulnerabilities": trivy_vulnerabilities,
        "gitleaks_secrets": gitleaks_secrets
    }

    # -----------------------------------
    # AI Deployment Gate Logic
    # -----------------------------------
    if critical > 0 or gitleaks_secrets > 0:

        deployment["deployment_decision"] = "NOT APPROVED"
        deployment["overall_risk"] = "CRITICAL"
        deployment["confidence"] = 99
        deployment["reason"] = "Critical vulnerabilities or secrets detected."

    elif high > 0:

        deployment["deployment_decision"] = "APPROVED WITH CAUTION"
        deployment["overall_risk"] = "HIGH"
        deployment["confidence"] = 97
        deployment["reason"] = "High severity vulnerabilities detected."

    elif medium > 0 or bandit_issues > 0:

        deployment["deployment_decision"] = "APPROVED WITH CAUTION"
        deployment["overall_risk"] = "MEDIUM"
        deployment["confidence"] = 95
        deployment["reason"] = "Medium severity findings detected."

    else:

        deployment["deployment_decision"] = "APPROVED"
        deployment["overall_risk"] = "LOW"
        deployment["confidence"] = 98
        deployment["reason"] = "No critical vulnerabilities detected."

    # -----------------------------------
    # Save Deployment Decision
    # -----------------------------------
    with open("deployment-decision.json", "w", encoding="utf-8") as f:
        json.dump(deployment, f, indent=4)

    print("✅ deployment-decision.json generated successfully.")

else:

    print("Error:", response.status_code)
    print(response.text)