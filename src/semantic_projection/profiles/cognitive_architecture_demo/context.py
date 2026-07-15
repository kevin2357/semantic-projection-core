from __future__ import annotations

CONTEXT_ID = "cognitive_architecture.general.v0"


def context_salience(context: dict, domains: list[str]) -> float:
    # The demo currently has one deliberately simple context.
    return 1.0
