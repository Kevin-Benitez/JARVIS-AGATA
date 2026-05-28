import subprocess, webbrowser, os

BROWSERS = {
    "chrome": ["chrome", "google-chrome", "chromium"],
    "edge": ["msedge", "microsoft-edge"],
    "firefox": ["firefox"],
    "opera": ["opera"],
    "brave": ["brave", "brave-browser"],
}

def browser_control(parameters=None, player=None, **kwargs):
    if not parameters:
        return "No se especificó la acción."
    action  = parameters.get("action", "go_to")
    url     = parameters.get("url", "")
    query   = parameters.get("query", "")
    browser = parameters.get("browser", "").lower()
    text    = parameters.get("text", "")

    if action in ("go_to", "new_tab"):
        target = url or f"https://www.google.com/search?q={query.replace(' ', '+')}"
        if browser:
            names = BROWSERS.get(browser, [browser])
            for name in names:
                try:
                    subprocess.Popen([name, target], shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    return f"Abriendo {target} en {browser}."
                except:
                    pass
        webbrowser.open(target)
        return f"Abriendo {target}."

    if action == "search":
        engine = parameters.get("engine", "google")
        engines = {
            "google": "https://www.google.com/search?q=",
            "bing": "https://www.bing.com/search?q=",
            "duckduckgo": "https://duckduckgo.com/?q=",
        }
        base = engines.get(engine, engines["google"])
        webbrowser.open(base + query.replace(" ", "+"))
        return f"Buscando '{query}' en {engine}."

    if action == "screenshot":
        try:
            import pyautogui
            from datetime import datetime
            path = parameters.get("path", os.path.join(
                os.path.expanduser("~"), "Desktop",
                f"browser_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"))
            pyautogui.screenshot(path)
            return f"Captura guardada en {path}"
        except Exception as e:
            return f"Error al capturar: {e}"

    if action in ("back", "forward", "reload"):
        import pyautogui
        hotkeys = {"back": ["alt", "left"], "forward": ["alt", "right"], "reload": ["f5"]}
        pyautogui.hotkey(*hotkeys[action])
        return f"Acción {action} ejecutada."

    if action == "close":
        import pyautogui
        pyautogui.hotkey("ctrl", "w")
        return "Pestaña cerrada."

    return f"Acción de navegador '{action}' ejecutada."
