from flask import Flask, request, jsonify
import os
import generator
import github_helper
import requests
import threading
import time

app = Flask(__name__)

# This should be loaded from a secure location, but for now, we'll hardcode it.
SECRET = "my-super-secret-key"

def build_and_deploy(data):
    """
    This function runs in a separate thread to avoid blocking the main thread.
    """
    try:
        print("Starting build and deploy process...")
        # 1. Generate app code
        filename, content, _ = generator.generate_app(data["brief"], data.get("attachments", []), data["round"])
        if not filename:
            print("Error: Could not generate app for the given brief")
            return

        # 2. Set up GitHub interaction
        g = github_helper.get_github_instance()
        repo_name = data["task"]

        # 3. Create repo
        repo = github_helper.create_repo(g, repo_name)
        print(f"Successfully created repo: {repo.full_name}")

        # 4. Upload generated file
        github_helper.upload_file(repo, filename, content, f"Add {filename}")
        print(f"Successfully uploaded {filename}")

        # 5. Add LICENSE
        github_helper.add_license(repo)
        print("Successfully added MIT LICENSE")

        # 6. Add README.md
        readme_content = f"""
# {repo_name}

This project was generated based on the following brief:

> {data['brief']}

## Setup
This is a static website. No setup is required.

## Usage
The page can be viewed on GitHub Pages.

## Code Explanation
The `index.html` file contains the HTML, CSS, and JavaScript for the application.

## License
This project is licensed under the MIT License.
"""
        github_helper.upload_file(repo, "README.md", readme_content, "Add README.md")
        print("Successfully added README.md")

        # 7. Enable GitHub Pages
        github_helper.enable_pages(repo)
        print("Enabled GitHub Pages. Waiting for deployment...")
        time.sleep(10) # Give GitHub some time to deploy the page

        user = g.get_user().login
        pages_url = f"https://{user}.github.io/{repo_name}/"

        # 8. Get the latest commit SHA
        commits = repo.get_commits()
        latest_commit_sha = commits[0].sha

        # 9. Notify evaluation URL
        evaluation_payload = {
            "email": data["email"],
            "task": data["task"],
            "round": data["round"],
            "nonce": data["nonce"],
            "repo_url": repo.html_url,
            "commit_sha": latest_commit_sha,
            "pages_url": pages_url,
        }

        print(f"Sending payload to evaluation_url: {evaluation_payload}")
        response = requests.post(data["evaluation_url"], json=evaluation_payload)
        response.raise_for_status()
        print(f"Successfully notified evaluation server. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred during build and deploy: {e}")


def revise_and_deploy(data):
    """
    This function runs in a separate thread to avoid blocking the main thread.
    """
    try:
        print("Starting revise and deploy process...")
        # 1. Generate app code
        filename, content, _ = generator.generate_app(data["brief"], data.get("attachments", []), data["round"])
        if not filename:
            print("Error: Could not generate app for the given brief")
            return

        # 2. Set up GitHub interaction
        g = github_helper.get_github_instance()
        repo_name = data["task"]
        user = g.get_user()
        repo = user.get_repo(repo_name)

        # 3. Upload generated file
        github_helper.upload_file(repo, filename, content, f"Update {filename} for round 2")
        print(f"Successfully uploaded {filename}")

        # 4. Update README.md
        readme_content = f"""
# {repo_name}

This project was generated based on the following brief:

> {data['brief']}

## Setup
This is a static website. No setup is required.

## Usage
The page can be viewed on GitHub Pages.

## Code Explanation
The `index.html` file contains the HTML, CSS, and JavaScript for the application.

## License
This project is licensed under the MIT License.
"""
        github_helper.upload_file(repo, "README.md", readme_content, "Update README.md for round 2")
        print("Successfully updated README.md")

        # 5. Get the latest commit SHA
        commits = repo.get_commits()
        latest_commit_sha = commits[0].sha

        # 6. Notify evaluation URL
        evaluation_payload = {
            "email": data["email"],
            "task": data["task"],
            "round": data["round"],
            "nonce": data["nonce"],
            "repo_url": repo.html_url,
            "commit_sha": latest_commit_sha,
            "pages_url": repo.html_url + "index.html", # This might need adjustment
        }

        print(f"Sending payload to evaluation_url: {evaluation_payload}")
        response = requests.post(data["evaluation_url"], json=evaluation_payload)
        response.raise_for_status()
        print(f"Successfully notified evaluation server. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred during revise and deploy: {e}")


@app.route('/api-endpoint', methods=['POST'])
def handle_request():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    required_fields = ["email", "secret", "task", "round", "nonce", "brief", "checks", "evaluation_url"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    if data["secret"] != SECRET:
        return jsonify({"error": "Invalid secret"}), 403

    if data["round"] == 1:
        thread = threading.Thread(target=build_and_deploy, args=(data,))
        thread.start()
        return jsonify({"status": "build-started"}), 200
    elif data["round"] == 2:
        thread = threading.Thread(target=revise_and_deploy, args=(data,))
        thread.start()
        return jsonify({"status": "revise-started"}), 200

    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)