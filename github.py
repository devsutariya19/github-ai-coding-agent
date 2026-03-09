import os
import requests
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()

def fetch_github(owner, repo, endpoing):
  url = f"https://api.github.com/repos/{owner}/{repo}/{endpoing}"
  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
  else:
    print(f"Failed to fetch data from GitHub API: {response.status_code} - {response.text}")
    return []
  
  print(data)
  return data

def load_issues(issues):
  docs = []

  for issue in issues:
    metadata = {
      "author": issue["user"]["login"],
      "comments": issue["comments"],
      "body": issue["body"],
      "labels": issue["labels"],
      "created_at": issue["created_at"],
    }

    data = issue["title"]

    if issue["body"]:
      data += issue["body"]

    doc = Document(page_content=data, metadata=metadata)
    docs.append(doc)

  return docs

def fetch_github_issues(owner, repo):
  data = fetch_github(owner, repo, "issues")
  return load_issues(data)
