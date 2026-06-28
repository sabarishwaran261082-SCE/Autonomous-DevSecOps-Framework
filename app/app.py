from flask import Flask, render_template
import json
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    ai = {
        "project": "Autonomous DevSecOps Framework",
        "security_score": 0,
        "overall_risk": "UNKNOWN",
        "confidence": 0,
        "deployment_decision": "PENDING",
        "bandit_issues": 0,
        "trivy_vulnerabilities": 0,
        "gitleaks_secrets": 0,
        "reason": "No AI analysis available.",
        "generated_at": "-"
    }

    decision_file = "deployment-decision.json"

    if os.path.exists(decision_file):
        with open(decision_file, "r", encoding="utf-8") as f:
            ai = json.load(f)

    # ----------------------------
    # Risk Color
    # ----------------------------
    risk_class = "unknown"

    if ai["overall_risk"] == "LOW":
        risk_class = "low"
    elif ai["overall_risk"] == "MEDIUM":
        risk_class = "medium"
    elif ai["overall_risk"] == "HIGH":
        risk_class = "high"
    elif ai["overall_risk"] == "CRITICAL":
        risk_class = "critical"

    # ----------------------------
    # Deployment Color
    # ----------------------------
    deployment_class = "pending"

    if ai["deployment_decision"] == "APPROVED":
        deployment_class = "approved"
    elif ai["deployment_decision"] == "APPROVED WITH CAUTION":
        deployment_class = "warning"
    elif ai["deployment_decision"] == "NOT APPROVED":
        deployment_class = "not-approved"

    return render_template(
        "dashboard.html",
        ai=ai,
        risk_class=risk_class,
        deployment_class=deployment_class
    )

@app.route("/health")
def health():
    return {
        "status": "UP",
        "application": "Autonomous DevSecOps Framework"
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)