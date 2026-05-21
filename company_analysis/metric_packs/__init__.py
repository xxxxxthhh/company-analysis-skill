"""Industry metric pack loader."""
from __future__ import annotations

import importlib

ALIASES = {
    "auto": "generic",
    "saas": "saas_cloud",
    "saas-cloud": "saas_cloud",
    "cloud": "saas_cloud",
    "fintech": "fintech_crypto_infra",
    "crypto": "fintech_crypto_infra",
    "software": "software_platform",
    "software-platform": "software_platform",
    "bank": "banks",
    "banks": "banks",
    "ecommerce": "ecommerce_consumer",
    "e-commerce": "ecommerce_consumer",
    "consumer": "ecommerce_consumer",
    "semi": "semiconductors",
    "semis": "semiconductors",
    "semiconductors": "semiconductors",
}

# Packs with real SEC-data extraction. All others fall back to generic.
IMPLEMENTED = {"generic"}


def load_metric_pack(name: str):
    module_name = ALIASES.get(name, name).replace("-", "_")
    if module_name not in IMPLEMENTED:
        # Fallback to generic; caller can inspect __name__ to report it.
        module_name = "generic"
    return importlib.import_module(f"company_analysis.metric_packs.{module_name}")
