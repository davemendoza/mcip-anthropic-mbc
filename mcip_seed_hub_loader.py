"""
mcip_seed_hub_loader.py
Wraps MCIP_Seed_Hub_min.json for runtime consumption.
"""
import json
from pathlib import Path

class MCIPSeedHubLoader:
    def __init__(self, path: str):
        self.path = Path(path)
        self._seeds = []

    def load(self):
        with open(self.path) as f:
            data = json.load(f)
        self._seeds = data.get("seeds", [])
        return self._seeds

    def category_summary(self):
        out = {}
        for s in self._seeds:
            cat = s.get("seed_category") or "Unknown"
            out[cat] = out.get(cat, 0) + 1
        return dict(sorted(out.items(), key=lambda x: -x[1]))

    def by_category(self, category):
        return [s for s in self._seeds if (s.get("seed_category") or "") == category]

    def by_priority(self, priority):
        # priority arg: int (1,2,3) or full string ("1 -- CRITICAL")
        if isinstance(priority, int):
            return [s for s in self._seeds if str(s.get("priority") or "").startswith(str(priority))]
        return [s for s in self._seeds if s.get("priority") == priority]

    def critical_seeds(self):
        return self.by_priority(1)

    def press_wire_seeds(self):
        return self.by_category("Press Intelligence")

    def design_credit_seeds(self):
        return self.by_category("Design Credit Database")

    def to_hermes_input(self):
        out = []
        for s in self._seeds:
            url = s.get("source_url")
            if not url:
                continue
            out.append({
                "url": url,
                "seed_id": s.get("_id"),
                "category": s.get("seed_category"),
                "priority": s.get("priority"),
                "authority_strength": s.get("authority_strength"),
                "extraction_method": s.get("extraction_method"),
                "talent_domain": "mcip",
            })
        return out
