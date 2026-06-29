def get_security_pipeline(language):
    """
    Return the security tools based on the detected language.
    """

    pipelines = {

        "Python": [
            "Bandit",
            "Trivy",
            "Gitleaks"
        ],

        "Java": [
            "SpotBugs",
            "Trivy",
            "Gitleaks"
        ],

        "Node.js": [
            "npm audit",
            "Trivy",
            "Gitleaks"
        ],

        "Go": [
            "gosec",
            "Trivy",
            "Gitleaks"
        ],

        "Unknown": [
            "Trivy",
            "Gitleaks"
        ]
    }

    return pipelines.get(language, pipelines["Unknown"])