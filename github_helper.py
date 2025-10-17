import os
from github import Github

def get_github_instance():
    """
    Returns a Github instance authenticated with a personal access token.
    """
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable not set")
    return Github(token)

def create_repo(g, repo_name):
    """
    Creates a new public repository on GitHub.
    """
    user = g.get_user()
    repo = user.create_repo(repo_name, private=False)
    return repo

def upload_file(repo, file_path, content, commit_message):
    """
    Uploads or updates a file in the specified repository.
    """
    try:
        # Try to get the file to see if it exists
        existing_file = repo.get_contents(file_path)
        # If it exists, update it
        repo.update_file(file_path, commit_message, content, existing_file.sha)
    except Exception:
        # If it doesn't exist, create it
        repo.create_file(file_path, commit_message, content)

def add_license(repo):
    """
    Adds an MIT license to the repository.
    """
    license_content = """
MIT License

Copyright (c) 2023

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    repo.create_file("LICENSE", "Add MIT License", license_content)

def enable_pages(repo):
    """
    Enables GitHub Pages for the repository.
    """
    repo.create_pages_site(source={"branch": "main", "path": "/"})