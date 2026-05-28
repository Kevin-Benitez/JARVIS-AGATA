import subprocess, webbrowser, time

def _spotify_hotkey(keys):
    try:
        import pyautogui
        pyautogui.hotkey(*keys)
        return True
    except:
        return False

def spotify_control(parameters=None, player=None, speak=None, **kwargs):
    if not parameters:
        return "No se especificó la acción."
    action = parameters.get("action", "play")
    query  = parameters.get("query", "")

    if action == "play" and query:
        # Open Spotify with search
        search_url = f"spotify:search:{query.replace(' ', '%20')}"
        try:
            subprocess.Popen(["spotify", "--uri", search_url], shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            time.sleep(1)
        except:
            pass
        webbrowser.open(f"https://open.spotify.com/search/{query.replace(' ', '%20')}")
        return f"Buscando '{query}' en Spotify."

    if action == "pause":
        _spotify_hotkey(["space"])
        return "Spotify pausado."

    if action == "resume":
        _spotify_hotkey(["space"])
        return "Reproducción reanudada."

    if action == "next":
        _spotify_hotkey(["ctrl", "right"])
        return "Siguiente canción."

    if action == "previous":
        _spotify_hotkey(["ctrl", "left"])
        return "Canción anterior."

    if action == "volume_up":
        _spotify_hotkey(["ctrl", "up"])
        return "Volumen de Spotify subido."

    if action == "volume_down":
        _spotify_hotkey(["ctrl", "down"])
        return "Volumen de Spotify bajado."

    return f"Acción de Spotify '{action}' no reconocida."
