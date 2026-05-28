import os, sys, subprocess, webbrowser

APPS = {
    "chrome": "chrome", "google chrome": "chrome",
    "firefox": "firefox", "edge": "msedge", "opera": "opera",
    "notepad": "notepad", "bloc de notas": "notepad",
    "calculadora": "calc", "calculator": "calc",
    "explorador": "explorer", "explorer": "explorer",
    "word": "winword", "excel": "excel", "powerpoint": "powerpnt",
    "spotify": "spotify", "discord": "discord",
    "vscode": "code", "vs code": "code", "visual studio code": "code",
    "cmd": "cmd", "powershell": "powershell", "terminal": "cmd",
    "paint": "mspaint", "task manager": "taskmgr",
    "youtube": "https://youtube.com", "gmail": "https://gmail.com",
    "github": "https://github.com", "google": "https://google.com",
    "whatsapp": "https://web.whatsapp.com",
    "telegram": "https://web.telegram.org",
    "twitter": "https://twitter.com", "x": "https://x.com",
    "instagram": "https://instagram.com", "facebook": "https://facebook.com",
}

def open_app(parameters=None, response=None, player=None, **kwargs):
    if not parameters:
        return "No se especificó la aplicación."
    app_name = parameters.get("app_name", "").strip()
    project_path = parameters.get("project_path", "")
    key = app_name.lower()

    if project_path:
        try:
            subprocess.Popen(["code", project_path], shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            return f"Abriendo {project_path} en VS Code."
        except Exception as e:
            return f"No pude abrir el proyecto: {e}"

    target = APPS.get(key, app_name)

    if target.startswith("http"):
        webbrowser.open(target)
        return f"Abriendo {app_name} en el navegador."

    try:
        subprocess.Popen(target, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return f"{app_name} abierto correctamente."
    except Exception as e:
        return f"No pude abrir {app_name}: {e}"
