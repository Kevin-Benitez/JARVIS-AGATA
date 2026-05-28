import requests

def weather_action(parameters=None, player=None, **kwargs):
    if not parameters:
        return "No se especificó la ciudad."
    city = parameters.get("city", "Buenos Aires").strip()
    try:
        url = f"https://wttr.in/{city.replace(' ', '+')}?format=3&lang=es"
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            return r.text.strip()
        return f"No pude obtener el clima de {city}."
    except Exception as e:
        return f"Error al consultar el clima: {e}"
