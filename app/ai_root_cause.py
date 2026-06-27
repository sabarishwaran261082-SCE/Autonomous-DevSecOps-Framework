import os
import json
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
# Send Request
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
    # Generate Deployment Decision JSON
    # -----------------------------------
    deployment = {
        "deployment_decision": "APPROVED",
        "overall_risk": "LOW",
        "security_score": 95,
        "confidence": 98,
        "reason": "No critical vulnerabilities or secrets detected."
    }

    report_upper = ai_report.upper()

    if "CRITICAL" in report_upper:
        deployment["deployment_decision"] = "NOT APPROVED"
        deployment["overall_risk"] = "CRITICAL"
        deployment["security_score"] = 20
        deployment["confidence"] = 99
        deployment["reason"] = "Critical vulnerabilities detected."

    elif "HIGH RISK" in report_upper:
        deployment["deployment_decision"] = "NOT APPROVED"
        deployment["overall_risk"] = "HIGH"
        deployment["security_score"] = 45
        deployment["confidence"] = 97
        deployment["reason"] = "High-risk vulnerabilities detected."

    elif "MEDIUM" in report_upper:
        deployment["deployment_decision"] = "APPROVED WITH CAUTION"
        deployment["overall_risk"] = "MEDIUM"
        deployment["security_score"] = 75
        deployment["confidence"] = 95
        deployment["reason"] = "Medium severity findings detected."

    # -----------------------------------
    # Save Deployment Decision
    # -----------------------------------
    with open("deployment-decision.json", "w", encoding="utf-8") as f:
        json.dump(deployment, f, indent=4)

    print("✅ deployment-decision.json generated successfully.")

else:

    print("Error:", response.status_code)
    print(response.text)