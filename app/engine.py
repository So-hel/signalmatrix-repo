import re
from typing import Dict, List, Any
from datetime import datetime

class ScoringEngine:
    def __init__(self, raw_data: Dict[str, Any]):
        self.user = raw_data.get("user", {})
        self.repos = raw_data.get("repos", [])
        self.repo_details = raw_data.get("repo_details", {})
        
    def calculate_metrics(self) -> Dict[str, Any]:
        metrics = {
            "consistency": self._score_consistency(),
            "depth": self._score_depth(),
            "clarity": self._score_clarity(),
            "focus": self._score_focus(),
            "production": self._score_production(),
        }
        
        total_score = sum(metrics.values())
        
        return {
            "total_score": total_score,
            "breakdown": metrics,
            "decision": self._get_decision(total_score),
            "hiring_risk": self._get_risk_index(),
            "red_flags": self._detect_red_flags(),
            "signals": self._detect_strong_signals(),
            "maturity_trend": self._analyze_maturity(),
            "collaboration_score": self._score_collaboration(),
            "complexity_class": self._estimate_complexity(),
            "benchmark_position": self._get_benchmark_position(total_score)
        }

    def _score_consistency(self) -> int:
        # Based on commit frequency and repo age
        if not self.repos: return 0
        score = 0
        repo_count = len(self.repos)
        if repo_count > 5: score += 5
        
        recent_commits = 0
        for name, details in self.repo_details.items():
            recent_commits += len(details.get("commits", []))
            
        if recent_commits > 20: score += 5
        return min(10, score)

    def _score_depth(self) -> int:
        # Based on folder depth and modularity
        score = 0
        avg_depth = 0
        for name, details in self.repo_details.items():
            depth = self._calculate_repo_depth(details.get("contents", []))
            avg_depth += depth
            
        if self.repos:
            avg_depth /= len(self.repos)
            
        if avg_depth > 3: score += 5
        if len(self.repos) > 0 and any(len(d.get("languages", {})) > 2 for d in self.repo_details.values()):
            score += 5
        return min(10, score)

    def _score_clarity(self) -> int:
        # Based on README existence and documentation
        score = 0
        has_readme = sum(1 for d in self.repo_details.values() if any(c['name'].lower() == 'readme.md' for c in d.get('contents', [])))
        if self.repos and (has_readme / len(self.repos)) > 0.7: score += 5
        
        # Check for modular structure (folders like 'src', 'app', 'tests')
        structured_repos = 0
        for d in self.repo_details.values():
            names = [c['name'].lower() for c in d.get('contents', [])]
            if any(n in ['src', 'app', 'lib', 'include'] for n in names):
                structured_repos += 1
        
        if self.repos and (structured_repos / len(self.repos)) > 0.5: score += 5
        return min(10, score)

    def _score_focus(self) -> int:
        # Based on language specialization
        langs = {}
        for d in self.repo_details.values():
            for l, v in d.get('languages', {}).items():
                langs[l] = langs.get(l, 0) + v
        
        if not langs: return 0
        
        top_lang_ratio = max(langs.values()) / sum(langs.values())
        score = int(top_lang_ratio * 10)
        return min(10, score)

    def _score_production(self) -> int:
        # Based on CI/CD, Docker, Tests, Releases
        score = 0
        signals = 0
        for d in self.repo_details.values():
            contents = [c['name'].lower() for c in d.get('contents', [])]
            if 'dockerfile' in contents: signals += 2
            if '.github' in contents: signals += 2
            if any('test' in c for c in contents): signals += 2
            if d.get('releases'): signals += 2
            
        if signals > 5: score += 10
        elif signals > 2: score += 5
        return min(10, score)

    def _calculate_repo_depth(self, contents: List[Dict]) -> int:
        # Simplified depth calculation
        return 1 if any(c['type'] == 'dir' for c in contents) else 0

    def _get_decision(self, score: int) -> str:
        if score >= 40: return "Strong Shortlist"
        if score >= 28: return "Borderline"
        return "Not Ready"

    def _get_risk_index(self) -> str:
        score = 0
        # High risk factors
        if not self.user.get("bio"): score += 1
        if len(self.repos) < 3: score += 2
        
        fork_ratio = 0
        if self.repos:
            forks = sum(1 for r in self.repos if r.get("fork"))
            fork_ratio = forks / len(self.repos)
        
        if fork_ratio > 0.7: score += 2
        
        if score > 3: return "High"
        if score > 1: return "Medium"
        return "Low"

    def _detect_red_flags(self) -> Dict[str, List[str]]:
        flags = {"critical": [], "moderate": [], "minor": []}
        
        if not self.repos:
            flags["critical"].append("Empty Profile: No public repositories found.")
            return flags
            
        forks = sum(1 for r in self.repos if r.get("fork"))
        if len(self.repos) > 0 and (forks / len(self.repos)) > 0.8:
            flags["moderate"].append("Fork-Heavy: Most repositories are forks, not original work.")
            
        # Repetitive commits
        all_commits = []
        for d in self.repo_details.values():
            for c in d.get("commits", []):
                all_commits.append(c.get("commit", {}).get("message", ""))
        
        if all_commits:
            unique_commits = set(all_commits)
            if len(unique_commits) / len(all_commits) < 0.3:
                flags["moderate"].append("Repetitive Commits: Low diversity in commit messages.")

        return flags

    def _detect_strong_signals(self) -> List[str]:
        signals = []
        production_readiness = self._score_production()
        if production_readiness >= 8:
            signals.append("Production Ready: Strong evidence of CI/CD and deployment configuration.")
        
        collab = self._score_collaboration()
        if collab > 5:
            signals.append("Active Collaborator: Significant external contributions and issue tracking.")
            
        return signals

    def _analyze_maturity(self) -> str:
        if len(self.repos) < 2: return "N/A"
        # Compare newest vs oldest (by creation date)
        sorted_repos = sorted(self.repos, key=lambda x: x.get("created_at", ""))
        oldest = sorted_repos[0]
        newest = sorted_repos[-1]
        
        # Simple heuristic: Does the newer repo have better structure?
        return "Improving" # Placeholder for more complex comparison logic

    def _score_collaboration(self) -> int:
        score = 0
        for d in self.repo_details.values():
            if d.get("pulls"): score += 2
            if d.get("issues"): score += 1
        return min(10, score)

    def _estimate_complexity(self) -> str:
        total_files = 0
        for d in self.repo_details.values():
            total_files += len(d.get("contents", []))
            
        if total_files > 50: return "Advanced"
        if total_files > 20: return "Intermediate"
        return "Toy"

    def _get_benchmark_position(self, score: int) -> str:
        if score >= 40: return "Above Strong Candidate"
        if score >= 28: return "Near Production-Ready"
        return "At Learner Level"
