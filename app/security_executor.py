import subprocess
import shutil
import os
import time
import json


class SecurityExecutor:

    def __init__(self, project_path):

        self.project_path = project_path

        # -----------------------------------
        # Execution Status
        # -----------------------------------

        self.execution_status = {

            "bandit": {
                "status": "NOT RUN",
                "duration": 0
            },

            "trivy": {
                "status": "NOT RUN",
                "duration": 0
            },

            "gitleaks": {
                "status": "NOT RUN",
                "duration": 0
            },

            "overall": "SUCCESS"

        }

        # -----------------------------------
        # Detect Trivy
        # -----------------------------------

        self.trivy = shutil.which("trivy")

        if self.trivy is None:

            possible = os.path.join(
                os.environ["LOCALAPPDATA"],
                "Microsoft",
                "WinGet",
                "Packages",
                "AquaSecurity.Trivy_Microsoft.Winget.Source_8wekyb3d8bbwe",
                "trivy.exe"
            )

            if os.path.exists(possible):
                self.trivy = possible

        # -----------------------------------
        # Detect Gitleaks
        # -----------------------------------

        self.gitleaks = shutil.which("gitleaks")

        if self.gitleaks is None:

            possible = os.path.join(
                os.environ["LOCALAPPDATA"],
                "Microsoft",
                "WinGet",
                "Packages",
                "Gitleaks.Gitleaks_Microsoft.Winget.Source_8wekyb3d8bbwe",
                "gitleaks.exe"
            )

            if os.path.exists(possible):
                self.gitleaks = possible

    # -----------------------------------
    # Run Bandit
    # -----------------------------------

    def run_bandit(self):

        print("\nRunning Bandit...")

        command = [

            "python",
            "-m",
            "bandit",
            "-r",
            self.project_path,
            "-f",
            "json",
            "-o",
            "bandit-report.json"

        ]

        start = time.time()

        result = subprocess.run(command, check=False)

        end = time.time()

        self.execution_status["bandit"]["duration"] = round(end - start, 2)

        if result.returncode == 0:

            self.execution_status["bandit"]["status"] = "SUCCESS"

        else:

            self.execution_status["bandit"]["status"] = "FAILED"
            self.execution_status["overall"] = "FAILED"

        print("✓ Bandit Completed")

    # -----------------------------------
    # Run Trivy
    # -----------------------------------

    def run_trivy(self):

        if self.trivy is None:

            print("⚠ Trivy not found. Skipping...")

            self.execution_status["trivy"]["status"] = "SKIPPED"

            return

        print("\nRunning Trivy...")

        command = [

            self.trivy,
            "fs",
            self.project_path,
            "--format",
            "json",
            "--output",
            "trivy-report.json"

        ]

        start = time.time()

        result = subprocess.run(command, check=False)

        end = time.time()

        self.execution_status["trivy"]["duration"] = round(end - start, 2)

        if result.returncode == 0:

            self.execution_status["trivy"]["status"] = "SUCCESS"

        else:

            self.execution_status["trivy"]["status"] = "FAILED"
            self.execution_status["overall"] = "FAILED"

        print("✓ Trivy Completed")

    # -----------------------------------
    # Run Gitleaks
    # -----------------------------------

    def run_gitleaks(self):

        if self.gitleaks is None:

            print("⚠ Gitleaks not found. Skipping...")

            self.execution_status["gitleaks"]["status"] = "SKIPPED"

            return

        print("\nRunning Gitleaks...")

        command = [

            self.gitleaks,
            "detect",
            "--source",
            self.project_path,
            "--report-format",
            "json",
            "--report-path",
            "gitleaks-report.json"

        ]

        start = time.time()

        result = subprocess.run(command, check=False)

        end = time.time()

        self.execution_status["gitleaks"]["duration"] = round(end - start, 2)

        if result.returncode == 0:

            self.execution_status["gitleaks"]["status"] = "SUCCESS"

        else:

            self.execution_status["gitleaks"]["status"] = "FAILED"
            self.execution_status["overall"] = "FAILED"

        print("✓ Gitleaks Completed")

    # -----------------------------------
    # Execute Pipeline
    # -----------------------------------

    def execute(self, pipeline):

        print("\n=================================")
        print("SECURITY EXECUTION ENGINE")
        print("=================================")

        for tool in pipeline:

            if tool == "Bandit":

                self.run_bandit()

            elif tool == "Trivy":

                self.run_trivy()

            elif tool == "Gitleaks":

                self.run_gitleaks()

        # -----------------------------------
        # Save Execution Status
        # -----------------------------------

        with open(
            "execution-status.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.execution_status,
                f,
                indent=4
            )

        print("\nExecution status saved.")

        print("\nExecution Summary")

        for tool in [

            "bandit",
            "trivy",
            "gitleaks"

        ]:

            print(
                f"{tool.capitalize():10} "
                f"{self.execution_status[tool]['status']:10} "
                f"{self.execution_status[tool]['duration']} sec"
            )

        print("\nOverall :", self.execution_status["overall"])

        print("\n=================================")
        print("PIPELINE FINISHED")
        print("=================================")