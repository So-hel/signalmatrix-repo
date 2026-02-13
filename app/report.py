from typing import Dict, Any

class ReportGenerator:
    @staticmethod
    def construct_final_report(scoring: Dict[str, Any], ai_sections: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "overall_score": f"{scoring['total_score']}/50",
            "recruiter_decision": scoring["decision"],
            "hiring_risk": scoring["hiring_risk"],
            "signal_breakdown": scoring["breakdown"],
            "strong_signals": scoring["signals"],
            "red_flags": scoring["red_flags"],
            "collaboration_score": scoring["collaboration_score"],
            "maturity_trend": scoring["maturity_trend"],
            "complexity_classification": scoring["complexity_class"],
            "benchmark_position": scoring["benchmark_position"],
            "executive_summary": ai_sections.get("executive_summary", "N/A"),
            "recruiter_reasoning": ai_sections.get("recruiter_reasoning", "N/A"),
            "readme_evaluation": ai_sections.get("readme_evaluation", "N/A"),
            "resume_verification": ai_sections.get("resume_verification", "N/A"),
            "improvement_roadmap": ai_sections.get("improvement_roadmap", {})
        }
