import json, os
from datetime import datetime, timedelta

CALENDAR_FILE = os.path.join(os.path.dirname(__file__), "..", "config", "calendar.json")

def _load():
    if os.path.exists(CALENDAR_FILE):
        with open(CALENDAR_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def _save(events):
    os.makedirs(os.path.dirname(CALENDAR_FILE), exist_ok=True)
    with open(CALENDAR_FILE, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2, ensure_ascii=False)

def calendar_manager(parameters=None, player=None, speak=None, **kwargs):
    if not parameters:
        return "No se especificó la acción."
    action = parameters.get("action", "list")
    events = _load()

    if action in ("list", "upcoming", "today"):
        if not events:
            return "No hay eventos en el calendario."
        days = parameters.get("days", 7)
        now  = datetime.now()
        lines = ["Próximos eventos:"]
        for e in events:
            try:
                dt = datetime.fromisoformat(e.get("datetime", ""))
                if action == "today" and dt.date() != now.date():
                    continue
                if (dt - now).days > days:
                    continue
                lines.append(f"- {e['title']} | {dt.strftime('%d/%m/%Y %H:%M')} | {e.get('location','')}")
            except:
                continue
        return "\n".join(lines) if len(lines) > 1 else "No hay eventos próximos."

    if action == "add":
        event = {
            "title": parameters.get("title", "Evento"),
            "datetime": parameters.get("datetime", ""),
            "location": parameters.get("location", ""),
        }
        events.append(event)
        _save(events)
        return f"Evento '{event['title']}' agregado."

    if action == "remove":
        index = parameters.get("index", 0)
        if 0 <= index < len(events):
            removed = events.pop(index)
            _save(events)
            return f"Evento '{removed['title']}' eliminado."
        return "Índice inválido."

    return f"Acción '{action}' no reconocida."
