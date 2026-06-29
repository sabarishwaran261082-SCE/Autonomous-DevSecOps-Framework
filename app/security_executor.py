import subprocess
import shutil
import os


class SecurityExecutor:

    def __init__(self, project_path):
        self.project_path = project_path

        # -----------------------------
        # Detect Trivy
        # -----------------------------
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

        # -----------------------------
        # Detect Gitleaks
        # -----------------------------
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
    # Bandit
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

        subprocess.run(command, check=False)

        print("✓ Bandit Completed")

    # -----------------------------------
    # Trivy
    # -----------------------------------
    def run_trivy(self):

        if self.trivy is None:

            print("⚠ Trivy not found. Skipping...")

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

        subprocess.run(command, check=False)

        print("✓ Trivy Completed")

    # -----------------------------------
    # Gitleaks
    # -----------------------------------
    def run_gitleaks(self):

        if self.gitleaks is None:

            print("⚠ Gitleaks not found. Skipping...")

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

        subprocess.run(command, check=False)

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

        print("\n=================================")
        print("PIPELINE FINISHED")
        print("=================================")