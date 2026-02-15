import json
import requests
from typing import Dict, Any
from .config import settings

class AIReasoningEngine:
    def __init__(self):
        self.provider = settings.ai_provider.lower()
        
        if self.provider == "blackbox":
            self.api_key = settings.blackbox_api_key
            self.model = settings.blackbox_model
            self.url = "https://api.blackbox.ai/v1/chat/completions"
        else:
            self.api_key = settings.openai_api_key
            self.model = settings.openai_model
            self.url = "https://api.openai.com/v1/chat/completions"

    def generate_report_sections(self, signals: Dict[str, Any], resume_text: str = "") -> Dict[str, Any]:
        if not self.api_key:
            return self._get_fallback_response(f"Missing API key for {self.provider}")

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
            ]
        }
        
        # OpenAI requires response_format for JSON mode, Blackbox might not or might handle it differently
        if self.provider == "openai":
            payload["response_format"] = {"type": "json_object"}

        try:
            response = requests.post(self.url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()["choices"][0]["message"]["content"]
            
            # Clean up response if it contains markdown code blocks
            if "```json" in data:
                data = data.split("```json")[1].split("```")[0].strip()
            elif "```" in data:
                data = data.split("```")[1].split("```")[0].strip()
                
            return json.loads(data)
        except Exception as e:
            error_msg = str(e)
            if hasattr(e, 'response') and e.response is not None:
                error_msg = e.response.text
            
            return self._get_fallback_response(error_msg)

    def _get_fallback_response(self, error_msg: str) -> Dict[str, Any]:
        summary = f"Error generating content with {self.provider}."
        if "insufficient_quota" in error_msg or "429" in error_msg:
            summary = f"{self.provider.capitalize()} Quota Exceeded. Please check your account credits. Rule-based scoring is still available below."
        elif "authentication" in error_msg.lower() or "401" in error_msg:
            summary = f"Authentication failed for {self.provider}. Check your API keys in the .env file."

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

