from fastapi import FastAPI, HTTPException, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional
import requests
import logging

from .collector import GitHubCollector
from .engine import ScoringEngine
from .ai_reasoning import AIReasoningEngine
from .report import ReportGenerator
from .config import settings

app = FastAPI(title="SignalMatrix Repo")

# Static files and templates
# Mount the root 'static' folder to '/static' path
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AnalysisRequest(BaseModel):
    # GitHub username validation: alphanumeric and hyphens, 1-39 chars
    # Avoiding look-ahead as it's not supported by Pydantic's default regex engine
    username: str = Field(..., min_length=1, max_length=39, pattern=r"^[a-zA-Z\d-]+$")
    resume_text: Optional[str] = ""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        # Serve index.html from the root directory
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Index file not found")

@app.post("/api/analyze")
async def analyze_profile(request: AnalysisRequest, authorization: Optional[str] = Header(None)):
    try:
        logger.info(f"Starting analysis for user: {request.username}")
        
        # Extract token from Bearer header if present
        token = None
        if authorization and authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]
            logger.info("Using provided GitHub token from client.")
        
        collector = GitHubCollector(token=token)
        
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
        return ReportGenerator.construct_final_report(scoring_results, ai_sections)
        
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        logger.error(f"GitHub API Error ({status_code}) for user {request.username}: {e.response.text}")
        detail = f"GitHub API Error: {status_code}"
        if status_code == 401:
            detail = "Authentication failed. Please verify the GITHUB_TOKEN."
        elif status_code == 404:
            detail = f"GitHub user '{request.username}' not found."
        raise HTTPException(status_code=status_code, detail=detail)
    except Exception as e:
        logger.error(f"Unexpected error during analysis for user {request.username}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during analysis")
