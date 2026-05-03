"""
Module 02 — Memory and Tool Use in Agents
==========================================
Agents become useful when they remember past turns and can call external tools.
This module shows three memory patterns:

  1. In-context memory       — just append to the prompt (cheapest, limited by context window)
  2. Summary memory          — periodically summarise old turns (saves tokens)
  3. External key-value store — persist facts between sessions

We also show how to wire up tools with JSON schemas so an LLM can decide
which tool to call and with what arguments.
"""

import json
from collections import deque
from typing import Any

# ---------------------------------------------------------------------------
# 1. In-context conversation memory
# ---------------------------------------------------------------------------

class ConversationBuffer:
    """Stores the last N turns in a list."""

    def __init__(self, max_turns: int = 10):
        self.turns: deque[dict] = deque(maxlen=max_turns)

    def add(self, role: str, content: str) -> None:
        self.turns.append({"role": role, "content": content})

    def to_prompt(self) -> str:
        lines = []
        for turn in self.turns:
            prefix = "User" if turn["role"] == "user" else "Assistant"
            lines.append(f"{prefix}: {turn['content']}")
        return "\n".join(lines)

    def __len__(self):
        return len(self.turns)


# ---------------------------------------------------------------------------
# 2. Summary memory (stub — replace summarise() with a real LLM call)
# ---------------------------------------------------------------------------

class SummaryMemory:
    """Keeps a running summary plus the most recent N turns."""

    def __init__(self, recent_turns: int = 4):
        self.summary = ""
        self.recent: ConversationBuffer = ConversationBuffer(max_turns=recent_turns)

    def add(self, role: str, content: str) -> None:
        self.recent.add(role, content)

    def summarise(self) -> None:
        """Stub: in production call an LLM to compress self.recent into self.summary."""
        oldest = list(self.recent.turns)[:2]
        for turn in oldest:
            prefix = "User" if turn["role"] == "user" else "Asst"
            self.summary += f" [{prefix}: {turn['content'][:40]}...]"

    def to_prompt(self) -> str:
        parts = []
        if self.summary:
            parts.append(f"[Summary of earlier conversation:{self.summary}]")
        parts.append(self.recent.to_prompt())
        return "\n".join(parts)


# ---------------------------------------------------------------------------
# 3. External key-value fact store
# ---------------------------------------------------------------------------

class FactStore:
    """Simple dict-backed store. Replace with Redis / SQLite for persistence."""

    def __init__(self):
        self._store: dict[str, Any] = {}

    def remember(self, key: str, value: Any) -> None:
        self._store[key] = value

    def recall(self, key: str, default=None) -> Any:
        return self._store.get(key, default)

    def forget(self, key: str) -> None:
        self._store.pop(key, None)

    def all(self) -> dict:
        return dict(self._store)


# ---------------------------------------------------------------------------
# JSON-schema tool definitions (OpenAI function-calling style)
# ---------------------------------------------------------------------------

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Return the current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name, e.g. Paris"}
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "remember_fact",
            "description": "Store a key-value fact for later retrieval.",
            "parameters": {
                "type": "object",
                "properties": {
                    "key":   {"type": "string"},
                    "value": {"type": "string"},
                },
                "required": ["key", "value"],
            },
        },
    },
]


# ---------------------------------------------------------------------------
# Stub tool implementations
# ---------------------------------------------------------------------------

def get_weather(city: str) -> str:
    fake_data = {"Paris": "18 C, partly cloudy", "Tokyo": "28 C, sunny", "London": "12 C, rainy"}
    return fake_data.get(city, "Weather data unavailable.")


def remember_fact(key: str, value: str, store: FactStore) -> str:
    store.remember(key, value)
    return f"Stored: {key} = {value}"


def dispatch_tool(name: str, args: dict, store: FactStore) -> str:
    if name == "get_weather":
        return get_weather(**args)
    if name == "remember_fact":
        return remember_fact(store=store, **args)
    return f"Unknown tool: {name}"


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== ConversationBuffer demo ===")
    buf = ConversationBuffer(max_turns=4)
    buf.add("user", "Hi, my name is Alex.")
    buf.add("assistant", "Hello Alex! How can I help?")
    buf.add("user", "What is the weather in Paris?")
    print(buf.to_prompt())

    print("\n=== FactStore demo ===")
    store = FactStore()
    result = dispatch_tool("remember_fact", {"key": "user_name", "value": "Alex"}, store)
    print(result)
    print("Stored facts:", store.all())

    weather = dispatch_tool("get_weather", {"city": "Paris"}, store)
    print("Weather:", weather)

    print("\n=== SummaryMemory demo ===")
    mem = SummaryMemory(recent_turns=4)
    for role, msg in [("user","Hello"), ("assistant","Hi!"),
                      ("user","My project is about LLMs"),("assistant","Cool!")]:
        mem.add(role, msg)
    mem.summarise()
    mem.add("user", "Remind me what my project is about?")
    print(mem.to_prompt())
