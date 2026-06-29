import requests
import json
import os

HEALTH_URL = "http://34.234.153.246:5000/health"

status_file = "deployment-status.json"

print("\n===================================")
print("DEPLOYMENT HEALTH CHECK")
print("===================================\n")

deployment_status = {}

if os.path.exists(status_file):
    with open(status_file, "r", encoding="utf-8") as f:
        deployment_status = json.load(f)

try:

    response = requests.get(HEALTH_URL, timeout=10)

    if response.status_code == 200:

        print("✅ Application is healthy.")

        deployment_status["health"] = "HEALTHY"
        deployment_status["deployment_result"] = "SUCCESS"

    else:

        print("❌ Health endpoint returned", response.status_code)

        deployment_status["health"] = "UNHEALTHY"
        deployment_status["deployment_result"] = "FAILED"

except Exception as e:

    print("❌ Health Check Failed")
    print(e)

    deployment_status["health"] = "UNREACHABLE"
    deployment_status["deployment_result"] = "FAILED"

with open(status_file, "w", encoding="utf-8") as f:
    json.dump(deployment_status, f, indent=4)

print("\n✅ deployment-status.json updated.")