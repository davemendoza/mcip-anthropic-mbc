"""
mcip_pipeline.py
Entry point for MCIP runs. Orchestrates loader, classifier, scoring, hooks.

Usage:
    python3 -m mcip.mcip_pipeline
    python3 -m mcip.mcip_pipeline --priority 1
    python3 -m mcip.mcip_pipeline --limit 50 --priority 1
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from mcip.mcip_seed_hub_loader import MCIPSeedHubLoader
from mcip.mcip_role_classifier import classify_role
from mcip.mcip_scoring import MCIPScoringEngine, MCIPOutreachHookGenerator

SEED_HUB_PATH = Path(__file__).parent / "MCIP_Seed_Hub_min.json"
OUTPUT_PATH = Path(__file__).parent / "outputs" / "mcip_run_output.json"


def run(limit=None, priority=None):
    print(f"[MCIP] Loading seed hub: {SEED_HUB_PATH}")
    loader = MCIPSeedHubLoader(str(SEED_HUB_PATH))
    seeds = loader.load()
    print(f"[MCIP] {len(seeds)} seeds loaded")
    print(f"[MCIP] Categories: {loader.category_summary()}")

    if priority:
        seeds = loader.by_priority(priority)
        print(f"[MCIP] Filtered to {len(seeds)} priority-{priority} seeds")

    if limit:
        seeds = seeds[:limit]
        print(f"[MCIP] Capped at {limit} seeds")

    engine = MCIPScoringEngine()
    hook_gen = MCIPOutreachHookGenerator()

    results = []
    for seed in seeds:
        classification = classify_role(
            seed.get("talent_type") or seed.get("target_function") or ""
        )
        lead_stub = {
            "Name": "",
            "Current_Employer": seed.get("source_name", ""),
            "Current_Title": seed.get("target_function", ""),
            "Role_Family": classification["Role_Family"],
            "Seniority": classification["Seniority"],
            "Source_Surface": seed.get("seed_category", ""),
            "Country": str(seed.get("geographic_coverage") or ""),
            "LinkedIn_URL": "",
            "Email_Pattern": "",
        }
        score = engine.score_lead(lead_stub, seed=seed)
        hook = hook_gen.generate(lead_stub, seed=seed)

        results.append({
            "seed_id": seed.get("_id"),
            "seed_category": seed.get("seed_category"),
            "source_name": seed.get("source_name"),
            "source_url": seed.get("source_url"),
            "priority": seed.get("priority"),
            "classification": classification,
            "scores": score.to_dict(),
            "outreach_hook": hook,
        })

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump({"total": len(results), "results": results}, f, indent=2, default=str)

    tier1 = [r for r in results if r["scores"].get("Priority") == "Tier 1"]
    tier2 = [r for r in results if r["scores"].get("Priority") == "Tier 2"]
    tier3 = len(results) - len(tier1) - len(tier2)

    print(f"[MCIP] Done — {len(results)} seeds scored")
    print(f"[MCIP] Tier 1: {len(tier1)} | Tier 2: {len(tier2)} | Tier 3: {tier3}")
    print(f"[MCIP] Output: {OUTPUT_PATH}")
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="MCIP Pipeline")
    parser.add_argument("--limit", type=int, default=None, help="Cap seed count")
    parser.add_argument("--priority", type=int, default=None, choices=[1, 2, 3])
    args = parser.parse_args()
    run(limit=args.limit, priority=args.priority)
