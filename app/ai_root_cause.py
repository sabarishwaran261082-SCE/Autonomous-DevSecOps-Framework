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

    with open("ai-security-report.md", "w", encoding="utf-8") as report_file:
        report_file.write("# 🤖 AI Security Report\n\n")
        report_file.write(ai_report)

    print("\n✅ ai-security-report.md generated successfully.")

else:

    print("Error:", response.status_code)
    print(response.text)