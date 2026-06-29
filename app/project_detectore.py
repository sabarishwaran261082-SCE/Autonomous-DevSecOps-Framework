import os


def detect_project(project_path):
    """
    Detect project language/framework by searching recursively.
    """

    for root, dirs, files in os.walk(project_path):

        # -----------------------------
        # Python
        # -----------------------------
        if "requirements.txt" in files or "app.py" in files:
            return {
                "language": "Python",
                "framework": "Flask/Django",
                "reason": f"Python files found in {root}"
            }

        # -----------------------------
        # Java (Maven)
        # -----------------------------
        if "pom.xml" in files:
            return {
                "language": "Java",
                "framework": "Maven",
                "reason": f"pom.xml found in {root}"
            }

        # -----------------------------
        # Java (Gradle)
        # -----------------------------
        if "build.gradle" in files:
            return {
                "language": "Java",
                "framework": "Gradle",
                "reason": f"build.gradle found in {root}"
            }

        # -----------------------------
        # Node.js
        # -----------------------------
        if "package.json" in files:
            return {
                "language": "Node.js",
                "framework": "Node.js",
                "reason": f"package.json found in {root}"
            }

        # -----------------------------
        # Go
        # -----------------------------
        if "go.mod" in files:
            return {
                "language": "Go",
                "framework": "Go Modules",
                "reason": f"go.mod found in {root}"
            }

    return {
        "language": "Unknown",
        "framework": "Unknown",
        "reason": "No known project files detected."
    }