import json
from pathlib import Path

_CONFIG_FILE = Path(__file__).parent.parent / "config" / "api_keys.json"

def get_api_key() -> str:
    if _CONFIG_FILE.exists():
        try:
            data = json.loads(_CONFIG_FILE.read_text(encoding="utf-8"))
            return data.get("gemini_api_key", "")
        except Exception:
            pass
    key = input("Ingresa tu Gemini API key: ").strip()
    _CONFIG_FILE.parent.mkdir(exist_ok=True)
    _CONFIG_FILE.write_text(json.dumps({"gemini_api_key": key}, indent=2), encoding="utf-8")
    return key
