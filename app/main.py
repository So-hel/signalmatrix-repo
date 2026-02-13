from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import os
import requests

from .collector import GitHubCollector
from .engine import ScoringEngine
from .ai_reasoning import AIReasoningEngine
from .report import ReportGenerator

app = FastAPI(title="SignalMatrix Repo")

# Static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")

class AnalysisRequest(BaseModel):
    username: str
    resume_text: Optional[str] = ""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("app/static/index.html", "r") as f:
        return f.read()

@app.post("/api/analyze")
async def analyze_profile(request: AnalysisRequest):
    try:
        collector = GitHubCollector()
        
        # Layer 1: Data Collection
        user_data = collector.get_user(request.username)
        repos = collector.get_repos(request.username)
        
        # Get details for top 5 repos to avoid massive API calls
        repo_details = {}
        for repo in repos[:5]:
            name = repo["name"]
            repo_details[name] = {
                "languages": collector.get_languages(request.username, name),
                "contents": collector.get_contents(request.username, name),
                "commits": collector.get_commits(request.username, name),
                "pulls": collector.get_pulls(request.username, name),
                "issues": collector.get_issues(request.username, name),
                "releases": collector.get_releases(request.username, name)
            }
            
        full_data = {
            "user": user_data,
            "repos": repos,
            "repo_details": repo_details
        }
        
        # Layer 2 & 3: Scoring
        engine = ScoringEngine(full_data)
        scoring_results = engine.calculate_metrics()
        
        # Layer 4: AI Reasoning
        ai_engine = AIReasoningEngine()
        ai_sections = ai_engine.generate_report_sections(scoring_results, request.resume_text)
        
        # Layer 5: Report Generation
        final_report = ReportGenerator.construct_final_report(scoring_results, ai_sections)
        
        return final_report
        
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        detail = f"GitHub API Error ({status_code}): {e.response.text}"
        if status_code == 401:
            detail = "Invalid GitHub Token. Please check your .env file."
        raise HTTPException(status_code=status_code, detail=detail)
    except Exception as e:
        print(f"Error during analysis: {str(e)}") # Print to console for debugging
        raise HTTPException(status_code=500, detail=str(e))
