import subprocess
from time import time

from flask import Flask, render_template, request
import json
import os
import zipfile
import shutil

from project_detectore import detect_project 
from security_pipeline import get_security_pipeline
from security_executor import SecurityExecutor
 
app = Flask(__name__)
 
UPLOAD_FOLDER = "uploads"
 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
 
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

EXTRACT_FOLDER = "extracted"

os.makedirs(EXTRACT_FOLDER, exist_ok=True)

app.config["EXTRACT_FOLDER"] = EXTRACT_FOLDER


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
 
    # -----------------------------------
    # Read Deployment History
    # -----------------------------------
 
    history = []
 
    history_file = "deployment-history.json"
 
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
 
    # Show only latest 5 deployments
    history = history[::-1][:5]
 
    audit = []
 
    audit_file = "audit-log.json"
 
    if os.path.exists(audit_file):
        with open(audit_file, "r", encoding="utf-8") as f:
            audit = json.load(f)
 
    audit = audit[::-1][:10]
 
    return render_template(
        "dashboard.html",
        ai=ai,
        history=history,
        history_json=json.dumps(history),
        audit=audit,
        risk_class=risk_class,
        deployment_class=deployment_class
    )
 
@app.route("/upload")
def upload_page():
    return render_template("upload.html")
 
@app.route("/upload", methods=["POST"])
def upload_project():
 
    if "project" not in request.files:
        return "No file selected."
 
    file = request.files["project"]
 
    if file.filename == "":
        return "No file selected."
 
    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )
 
    file.save(file_path)
    
    # -----------------------------------
    # Extract uploaded ZIP
    # -----------------------------------

    project_name = os.path.splitext(file.filename)[0]

    extract_path = os.path.join(
        app.config["EXTRACT_FOLDER"],
        project_name
    )

    # Remove old extraction if it exists
    if os.path.exists(extract_path):

    # Give Windows a moment to release file handles
         time.sleep(1)

         try:
             shutil.rmtree(extract_path)

         except PermissionError:

             print("⚠ Previous extracted folder is in use. Removing ignored.")

             shutil.rmtree(
                 extract_path,
                 ignore_errors=True
            )

    os.makedirs(extract_path)

    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)
    
    project = detect_project(extract_path)

    print("\n=================================")
    print("PROJECT DETECTION")
    print("=================================")
    print("Language :", project["language"])
    print("Framework:", project["framework"])
    print("Reason   :", project["reason"])
    
    pipeline = get_security_pipeline(
         project["language"]
    )

    print("\n===============================")
    print("SECURITY PIPELINE")
    print("===============================")
    
    executor = SecurityExecutor(extract_path)

    executor.execute(pipeline)
    
    print("\nGenerating Security Summary...")

    subprocess.run(
         ["python", "generate_summary.py"],
         check=False
    )

    print("✓ Security Summary Generated")
    
    print("\nRunning AI Root Cause Analyzer...")

    subprocess.run(
         ["python", "ai_root_cause.py"],
         check=False
    )

    print("✓ AI Security Report Generated")

    pipeline_html = "<br>".join(pipeline)
    
    return f"""
<h2>✅ Project Uploaded Successfully</h2>

<p><b>ZIP File:</b> {file.filename}</p>

<p><b>Language:</b> {project["language"]}</p>

<p><b>Framework:</b> {project["framework"]}</p>

<p><b>Reason:</b> {project["reason"]}</p>

<p><b>Extracted To:</b> {extract_path}</p>

<br>

<h3>Selected Security Pipeline</h3>

<p>{pipeline_html}</p>

<br>

<a href="/dashboard">Go to Dashboard</a>
"""

@app.route("/health")
def health():
    return {
        "status": "UP",
        "application": "Autonomous DevSecOps Framework"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)