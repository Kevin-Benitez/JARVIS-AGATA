import json
from pathlib import Path

_MEMORY_FILE = Path(__file__).parent / "memory.json"


def load_memory() -> dict:
    if not _MEMORY_FILE.exists():
        return {}
    try:
        with open(_MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def update_memory(data: dict) -> None:
    memory = load_memory()
    for category, entries in data.items():
        if category not in memory:
            memory[category] = {}
        for key, payload in entries.items():
            memory[category][key] = payload
    try:
        with open(_MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[Memory] Failed to save: {e}")


def format_memory_for_prompt(memory: dict) -> str:
    if not memory:
        return ""
    lines = ["[USER MEMORY]"]
    for category, entries in memory.items():
        lines.append(f"\n{category.upper()}:")
        for key, payload in entries.items():
            value = payload.get("value", payload) if isinstance(payload, dict) else payload
            lines.append(f"  - {key}: {value}")
    lines.append("")
    return "\n".join(lines)
