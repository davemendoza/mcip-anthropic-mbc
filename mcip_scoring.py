"""
mcip_scoring.py
MBC authority scoring for MCIP domain.
Governance: NEVER use followers, likes, views, engagement, virality.
"""
from dataclasses import dataclass, field
from typing import Optional

SOURCE_WEIGHTS = {
    "Congressional_Government": 10, "Tier1_Conference": 10,
    "Think_Tank_Author": 9, "Major_Publication": 9,
    "Major_Podcast": 8, "Award_Judge": 8,
    "Newsletter": 7, "Press_Wire": 7, "Design_Award": 7,
    "Community": 6, "Agency_Portfolio": 6,
    "Social_Platform": 3,
    "Followers": 0, "Engagement": 0, "Virality": 0,
}

ROLE_AI_RELEVANCE = {
    "Field Marketing": 8, "Communications": 8, "Corporate Comms": 8,
    "PMM": 8, "DevRel": 9, "Developer Community": 9,
    "Content": 7, "Brand": 7, "Brand & Creative": 7,
    "Motion Design": 6, "Design Engineering": 7,
    "Events": 6, "SEO": 6, "Policy Comms": 8,
    "Research Comms": 8, "Executive Comms": 7, "Content & Copy": 7,
}

@dataclass
class MCIPScore:
    ai_relevance: int = 0
    anthropic_relevance: int = 0
    candidate_quality: int = 0
    authority_score: float = 0.0
    influence_score: float = 0.0
    public_visibility: int = 5
    invisible_titan_score: float = 0.0
    tier: str = "Tier 3"
    confidence: str = "LOW"
    signals_used: list = field(default_factory=list)

    def to_dict(self):
        return {
            "AI_Relevance": self.ai_relevance,
            "Anthropic_Relevance": self.anthropic_relevance,
            "Candidate_Quality": self.candidate_quality,
            "Priority": self.tier,
            "Contact_Confidence": self.confidence,
            "_authority_score": round(self.authority_score, 2),
            "_invisible_titan_score": round(self.invisible_titan_score, 2),
        }

class MCIPScoringEngine:
    def score_lead(self, lead: dict, seed: Optional[dict] = None) -> MCIPScore:
        s = MCIPScore()
        role = lead.get("Role_Family") or ""
        s.ai_relevance = self._clamp(ROLE_AI_RELEVANCE.get(role, 6))

        emp = (lead.get("Current_Employer") or "").lower()
        s.anthropic_relevance = 10 if "anthropic" in emp else                                  8 if "openai" in emp else                                  7 if "mistral" in emp or "deepmind" in emp else 5

        if seed:
            s.anthropic_relevance = max(s.anthropic_relevance, int(seed.get("anthropic_relevance") or 0))

        cat = (seed or {}).get("seed_category") or lead.get("Source_Surface") or ""
        s.authority_score = self._authority_from_category(cat)

        seniority = (lead.get("Seniority") or "").lower()
        bonus = 4 if "vp" in seniority else 3 if "director" in seniority else                 2 if "senior" in seniority or "lead" in seniority else 1
        s.candidate_quality = self._clamp(round(s.authority_score * 0.6) + bonus)

        s.public_visibility = 2 if "hidden" in cat.lower() or "arxiv" in cat.lower()                               else 3 if "design credit" in cat.lower()                               else 4 if "press" in cat.lower()                               else 6 if "conference" in cat.lower()                               else 7 if "podcast" in cat.lower() else 5

        s.influence_score = min(10, s.anthropic_relevance * 0.7 + s.authority_score * 0.3)
        s.invisible_titan_score = s.authority_score + s.influence_score - s.public_visibility

        s.tier = "Tier 1" if s.anthropic_relevance >= 8 and s.candidate_quality >= 7 else                  "Tier 2" if s.anthropic_relevance >= 5 and s.candidate_quality >= 5 else "Tier 3"

        email = lead.get("Email_Pattern") or ""
        linkedin = lead.get("LinkedIn_URL") or ""
        s.confidence = "CONFIRMED" if email and "@" in email and not email.startswith("[") else                        "HIGH" if email and linkedin else                        "MEDIUM" if linkedin or email else "LOW"
        return s

    def _authority_from_category(self, cat: str) -> float:
        c = cat.lower()
        if "hidden authority" in c: return 9.0
        if "press" in c: return 7.0
        if "design credit" in c: return 7.0
        if "conference" in c: return 7.0
        if "award" in c: return 8.0
        if "podcast" in c: return 8.0
        if "vc" in c: return 8.0
        if "community" in c: return 6.0
        if "agency" in c: return 6.0
        if "arxiv" in c or "academic" in c: return 8.0
        if "policy" in c: return 9.0
        return 5.0

    def _clamp(self, v, lo=1, hi=10):
        return max(lo, min(hi, int(v or lo)))

class MCIPOutreachHookGenerator:
    def generate(self, lead: dict, seed: Optional[dict] = None) -> str:
        name = ((lead.get("Name") or "").split() or ["there"])[0]
        employer = lead.get("Current_Employer") or ""
        role = lead.get("Role_Family") or ""
        country = str(lead.get("Country") or "").lower()
        src = str(lead.get("Source_Surface") or (seed or {}).get("seed_category") or "").lower()

        if "arxiv" in src or "acknowledgment" in src:
            return f"{name}, found you via acknowledgments in Anthropic research. The role I am sourcing sits exactly at that boundary between research and public communication. Open to a brief conversation?"
        if "japan" in country or "connpass" in src:
            return f"{name}, organizing Claude events in Japan puts you in a category of one. Anthropic is building its first Japan-based team. I would like to learn more about what you are seeing on the ground."
        if "belgium" in country or "brussels" in src or "eu ai" in src:
            return f"{name}, your EU AI policy background is the rarest overlap in communications right now. Anthropic is small in Brussels and the mandate is significant. Worth 20 minutes?"
        if "press" in src:
            return f"{name}, found you via a {employer} press release. The comms scope at Anthropic right now is unusual for an AI company at this stage. Worth a quick call?"
        if "design credit" in src:
            return f"{name}, found your work through {src}. Anthropic brand is still early relative to its scale. The open canvas is real. Worth a call?"
        if "openai" in employer.lower() or "mistral" in employer.lower():
            return f"{name}, you have built the exact thing Anthropic needs built next. I am sourcing for that role and wanted to ask if you would be open to a conversation."
        return f"{name}, found you via {src or employer}. The {role} role at Anthropic is unusually open-scope for where the company is right now. Worth a quick conversation?"
