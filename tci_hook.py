import json
import requests
from flask import Flask, request

app = Flask(__name__)

# Travis CI Configuration
TRAVIS_CI_API_ENDPOINT = "https://api.travis-ci.com/repo/YOUR_REPO_SLUG/requests"
TRAVIS_CI_TOKEN = "YOUR_TRAVIS_CI_TOKEN"

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    try:
        payload = json.loads(request.data)  # Read the webhook payload from the POST request
        changelist = payload.get("changelist")

        if changelist:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Travis-API-Version": "3",
                "Authorization": "token {TRAVIS_CI_TOKEN}",
            }

            build_payload = {
                "request": {
                    "message": "Trigger build for Perforce changelist {changelist}",
                    "branch": "master",  # Replace with your desired branch
                    "config": {
                        "env": {"CHANGELIST": changelist}
                    }
                }
            }

            response = requests.post(TRAVIS_CI_API_ENDPOINT, json=build_payload, headers=headers)
            return response.text
        else:
            return "Changelist not found in payload"
    except Exception as e:
        return "Error: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
