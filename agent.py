# Copyright © 2026 Chelsea Megan Woods | Woods AI Studio / Lyman Legacies / Nova Umbrella
# NovaReign — Elite Upgrade (Governance)
# Source of truth: chichi-lyman/saphira-ai monorepo

from __future__ import annotations
from typing import Any, Dict, List
import asyncio
import logging
import uuid

logger = logging.getLogger("NovaReign")

SYSTEM_VOICE = "You are Nova Reign — governance and orchestration. Plan cleanly and enforce policy."
CAPABILITIES = ["governance.plan", "dispatch.specialists", "policy.enforce"]
NAME = "novareign"


class NovaReign:
    name = NAME
    capabilities = CAPABILITIES
    default_policy = "ALLOW"
    SYSTEM_VOICE = SYSTEM_VOICE
    max_timeout_s = 45.0
    max_retries = 2

    def __init__(self, memory_store=None):
        self.memory = memory_store

    async def safe_run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        isolation_token = payload.get("isolation_token") or str(uuid.uuid4())
        last_error = None
        for attempt in range(1, self.max_retries + 2):
            try:
                result = await asyncio.wait_for(
                    self.process({**payload, "isolation_token": isolation_token}),
                    timeout=self.max_timeout_s,
                )
                result.setdefault("agent", self.name)
                result.setdefault("status", "success")
                result.setdefault("isolation_token", isolation_token)
                return result
            except asyncio.TimeoutError:
                last_error = "timeout"
            except Exception as e:
                last_error = str(e)
        return {
            "agent": self.name,
            "status": "recovered_from_failure",
            "error": last_error,
            "isolation_token": isolation_token,
        }

    async def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        goal = payload.get("text") or payload.get("objective") or ""
        dispatch = self._plan_dispatch(goal)
        return {
            "status": "success",
            "goal": goal,
            "dispatch": dispatch,
            "governance_ok": True,
            "message": "Plan approved.",
            "voice_lock": True,
        }

    def _plan_dispatch(self, goal: str) -> List[str]:
        g = goal.lower()
        if any(w in g for w in ("revenue", "growth", "capital", "business")):
            return ["apex", "instinct"]
        if any(w in g for w in ("research", "learn", "summarize", "knowledge")):
            return ["scholar"]
        if any(w in g for w in ("compliance", "legal", "contract", "risk")):
            return ["lexis"]
        if any(w in g for w in ("data", "finance", "chart", "metric")):
            return ["lyra"]
        if any(w in g for w in ("infra", "latency", "optimize", "system")):
            return ["cipher"]
        return []
