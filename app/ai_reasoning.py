import json
import requests
from typing import Dict, Any
from .config import settings

class AIReasoningEngine:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.openai_api_key
        self.model = settings.openai_model

    def generate_report_sections(self, signals: Dict[str, Any], resume_text: str = "") -> Dict[str, Any]:
        # Validation is now handled by settings, so we can proceed

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""
        Analyze the following GitHub profile signals and generate a recruiter-style report.
        
        GITHUB SIGNALS:
        {json.dumps(signals, indent=2)}
        
        RESUME TEXT (OPTIONAL):
        {resume_text}
        
        Generate the following sections in JSON format:
        1. "executive_summary": A professional executive summary of the candidate's engineering profile.
        2. "recruiter_reasoning": A 3-line concise recruiter-style reasoning for the hiring decision.
        3. "readme_evaluation": Qualitative feedback on the candidate's documentation.
        4. "resume_verification": Reasoning on whether the GitHub evidence supports the claims in the resume (if provided).
        5. "improvement_roadmap": {{"week1": "...", "week2": "...", "week3": "...", "week4": "..."}}
        
        STRICT JSON OUTPUT ONLY.
        """

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an expert technical recruiter and engineering manager."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"}
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()["choices"][0]["message"]["content"]
            return json.loads(data)
        except Exception as e:
            error_msg = str(e)
            if hasattr(e, 'response') and e.response is not None:
                error_msg = e.response.text
            
            return self._get_fallback_response(error_msg)

    def _get_fallback_response(self, error_msg: str) -> Dict[str, Any]:
        summary = "Error generating AI content."
        if "insufficient_quota" in error_msg:
            summary = "OpenAI Quota Exceeded. Please add credits to your OpenAI account for AI insights. Rule-based scoring is still available below."
        elif "Invalid GitHub Token" in error_msg or "401" in error_msg:
            summary = "Authentication failed. Check your API keys in the .env file."

        return {
            "error": error_msg,
            "executive_summary": summary,
            "recruiter_reasoning": "AI Analysis Offline",
            "improvement_roadmap": {
                "week1": "Update README with architectural diagrams.",
                "week2": "Increase unit test coverage.",
                "week3": "Containerize the application (Dockerfile).",
                "week4": "Implement CI/CD (GitHub Actions)."
            },
            "resume_verification": "N/A (AI Offline)"
        }

