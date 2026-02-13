import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
repo_name = "signalmatrix-repo"
username = "So-hel"

print(f"Checking/Creating repository '{repo_name}' for user '{username}'...")

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# 1. Check if repo exists
url = f"https://api.github.com/repos/{username}/{repo_name}"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(f"✅ Repository '{repo_name}' already exists.")
elif response.status_code == 404:
    # 2. Create repo
    print(f"Creating repository '{repo_name}'...")
    create_url = "https://api.github.com/user/repos"
    payload = {
        "name": repo_name,
        "description": "Premium GitHub Portfolio Analyzer with AI reasoning and deterministic scoring.",
        "private": False
    }
    create_response = requests.post(create_url, headers=headers, json=payload)
    if create_response.status_code == 201:
        print(f"✅ Repository '{repo_name}' created successfully!")
    else:
        print(f"❌ Failed to create repository ({create_response.status_code}): {create_response.text}")
else:
    print(f"❌ Error checking repository ({response.status_code}): {response.text}")
