from typing import Dict, List, Any
from app.models.database import CandidateJobRanking, Candidate


class SHAPExplainer:
    """Generate SHAP-style feature importance explanations for rankings."""

    @staticmethod
    def explain_ranking(ranking: CandidateJobRanking, candidate: Candidate) -> Dict[str, Any]:
        """
        Generate an explainability summary for a ranking decision.

        Returns feature importance, contributing factors, and narratives.
        """
        scores = {
            "semantic_match": float(ranking.semantic_match_score or 0.0),
            "experience_match": float(ranking.experience_match_score or 0.0),
            "behavioral_score": float(ranking.behavioral_score or 0.0),
            "career_growth": float(ranking.career_growth_score or 0.0),
            "leadership": float(ranking.leadership_score or 0.0),
            "culture_fit": float(ranking.culture_fit_score or 0.0),
        }

        # Determine top contributing factors
        sorted_factors = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_contributing_factors = [factor[0] for factor in sorted_factors[:3]]

        # Build narrative based on scores
        strengths = ranking.top_strengths or []
        risks = ranking.potential_risks or []

        why_selected_narrative = (
            f"Candidate {candidate.anonymized_name} scored {ranking.final_score} on the ranking due to "
            f"strong {', '.join(top_contributing_factors[:2])}. "
            f"Key strengths: {', '.join(strengths[:2]) if strengths else 'varied background'}. "
        )

        risks_narrative = (
            f"Potential concerns: {', '.join(risks[:2]) if risks else 'none identified'}. "
            if risks
            else "No significant risks identified."
        )

        opportunities_narrative = (
            f"Growth potential: Candidate has demonstrated {len(candidate.skills or [])} skills and "
            f"{len(candidate.career_history or [])} roles, indicating strong adaptability and learning ability."
        )

        return {
            "ranking_id": ranking.id,
            "candidate_id": ranking.candidate_id,
            "final_score": float(ranking.final_score or 0.0),
            "feature_importance": scores,
            "top_contributing_factors": top_contributing_factors,
            "why_selected_narrative": why_selected_narrative,
            "risks_narrative": risks_narrative,
            "opportunities_narrative": opportunities_narrative,
            "top_strengths": strengths,
            "potential_risks": risks,
            "hidden_gem_indicators": ranking.hidden_gem_indicators or [],
        }

    @staticmethod
    def compare_rankings(
        ranking1: CandidateJobRanking,
        ranking2: CandidateJobRanking,
        candidate1: Candidate,
        candidate2: Candidate,
    ) -> Dict[str, Any]:
        """Compare two rankings and explain the difference."""
        exp1 = SHAPExplainer.explain_ranking(ranking1, candidate1)
        exp2 = SHAPExplainer.explain_ranking(ranking2, candidate2)

        score_diff = exp1["final_score"] - exp2["final_score"]
        winner = "Candidate 1" if score_diff > 0 else "Candidate 2"

        return {
            "candidate1_explanation": exp1,
            "candidate2_explanation": exp2,
            "score_difference": round(score_diff, 3),
            "ranking_winner": winner,
            "reason": (
                f"{winner} ranks higher primarily due to stronger "
                f"{exp1['top_contributing_factors'][0] if score_diff > 0 else exp2['top_contributing_factors'][0]}."
            ),
        }
