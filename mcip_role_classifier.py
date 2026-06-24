"""
mcip_role_classifier.py
Maps MBC role families to Anthropic target roles.
"""

ROLE_FAMILY_MAP = {
    "Field Marketing": ["Field Marketing Manager", "Senior Field Marketing Manager", "Head of Field Marketing"],
    "Communications": ["Communications Manager", "Senior Communications Manager", "Director of Communications"],
    "Corporate Comms": ["Corporate Communications Manager", "Head of Corporate Communications"],
    "PMM": ["Product Marketing Manager", "Senior PMM", "Director of Product Marketing"],
    "DevRel": ["Developer Relations Engineer", "Senior Developer Advocate", "Head of DevRel"],
    "Developer Community": ["Developer Community Manager", "Community Lead"],
    "Content": ["Content Strategist", "Senior Content Strategist", "Head of Content"],
    "Brand": ["Brand Strategist", "Senior Brand Manager", "Head of Brand"],
    "Brand & Creative": ["Creative Director", "Brand Creative Lead"],
    "Motion Design": ["Motion Designer", "Senior Motion Designer"],
    "Design Engineering": ["Design Engineer", "Senior Design Engineer"],
    "Events": ["Events Manager", "Senior Events Manager", "Head of Events"],
    "SEO": ["SEO Specialist", "Senior SEO Manager"],
    "Policy Comms": ["Policy Communications Manager", "Head of Policy Communications"],
    "Research Comms": ["Research Communications Manager"],
    "Executive Comms": ["Executive Communications Manager"],
    "Content & Copy": ["Copywriter", "Senior Copywriter", "Content & Copy Lead"],
}

SENIORITY_SIGNALS = {
    "chief": 10, "cmo": 10, "cco": 10,
    "vp": 8, "vice president": 8,
    "head of": 7,
    "director": 6,
    "senior": 5, "lead": 5, "principal": 5,
    "manager": 4,
    "specialist": 3,
    "coordinator": 2,
    "junior": 1, "associate": 2,
}

def classify_role(title: str) -> dict:
    t = title.lower()
    role_family = "Marketing"

    if "devrel" in t or "developer advocate" in t or "developer relations" in t:
        role_family = "DevRel"
    elif "motion" in t:
        role_family = "Motion Design"
    elif "design engineer" in t:
        role_family = "Design Engineering"
    elif "policy" in t:
        role_family = "Policy Comms"
    elif "research comm" in t:
        role_family = "Research Comms"
    elif "exec" in t and "comm" in t:
        role_family = "Executive Comms"
    elif "content" in t and "copy" in t:
        role_family = "Content & Copy"
    elif "brand" in t and "creat" in t:
        role_family = "Brand & Creative"
    elif "field marketing" in t:
        role_family = "Field Marketing"
    elif "product market" in t or "pmm" in t:
        role_family = "PMM"
    elif "communit" in t and "develop" in t:
        role_family = "Developer Community"
    elif "seo" in t:
        role_family = "SEO"
    elif "event" in t:
        role_family = "Events"
    elif "brand" in t:
        role_family = "Brand"
    elif "content" in t:
        role_family = "Content"
    elif "comm" in t:
        role_family = "Communications"

    seniority_score = 3
    seniority_label = "IC"
    for signal, score in SENIORITY_SIGNALS.items():
        if signal in t:
            seniority_score = score
            if score >= 8:
                seniority_label = "VP+"
            elif score >= 6:
                seniority_label = "Director"
            elif score >= 5:
                seniority_label = "Senior/Lead"
            elif score >= 4:
                seniority_label = "Manager"
            else:
                seniority_label = "IC"
            break

    return {
        "Role_Family": role_family,
        "Seniority": seniority_label,
        "Seniority_Score": seniority_score,
        "Target_Anthropic_Roles": ROLE_FAMILY_MAP.get(role_family, []),
    }
