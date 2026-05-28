"""
Ejecutar con: python setup_actions.py
Genera todos los módulos de actions/ con implementaciones reales.
"""
import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "actions")
os.makedirs(BASE, exist_ok=True)

files = {}

# ─── open_app ────────────────────────────────────────────────────────────────
files["open_app.py"] = '''
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
            subprocess.Popen(["code", project_path], shell=True)
            return f"Abriendo {project_path} en VS Code."
        except Exception as e:
            return f"No pude abrir el proyecto: {e}"

    target = APPS.get(key, app_name)

    if target.startswith("http"):
        webbrowser.open(target)
        return f"Abriendo {app_name} en el navegador."

    try:
        subprocess.Popen(target, shell=True)
        return f"{app_name} abierto correctamente."
    except Exception as e:
        return f"No pude abrir {app_name}: {e}"
'''

# ─── terminal ────────────────────────────────────────────────────────────────
files["terminal.py"] = '''
import subprocess, sys

def terminal(parameters=None, player=None, speak=None, **kwargs):
    if not parameters:
        return "No se especificó el comando."
    cmd = parameters.get("command", "").strip()
    timeout = parameters.get("timeout", 30)
    cwd = parameters.get("cwd", None)
    if not cmd:
        return "Comando vacío."
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            timeout=timeout, cwd=cwd, encoding="utf-8", errors="replace"
        )
        output = (result.stdout + result.stderr).strip()
        return output[:2000] if output else "Comando ejecutado sin salida."
    except subprocess.TimeoutExpired:
        return f"El comando superó el tiempo límite de {timeout}s."
    except Exception as e:
        return f"Error al ejecutar comando: {e}"
'''

# ─── computer_settings ───────────────────────────────────────────────────────
files["computer_settings.py"] = '''
import subprocess, os, time

def computer_settings(parameters=None, response=None, player=None, **kwargs):
    if not parameters:
        return "No se especificó la acción."
    action = parameters.get("action", "").lower()
    desc   = parameters.get("description", "").lower()
    value  = parameters.get("value", "")
    text   = action + " " + desc

    # Volume
    if any(w in text for w in ["volumen", "volume", "sube el volumen", "baja el volumen"]):
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            vol = cast(interface, POINTER(IAudioEndpointVolume))
            current = vol.GetMasterVolumeLevelScalar()
            if any(w in text for w in ["sube", "subir", "up", "aumenta"]):
                vol.SetMasterVolumeLevelScalar(min(1.0, current + 0.1), None)
                return "Volumen subido."
            elif any(w in text for w in ["baja", "bajar", "down", "reduce"]):
                vol.SetMasterVolumeLevelScalar(max(0.0, current - 0.1), None)
                return "Volumen bajado."
            elif any(w in text for w in ["mute", "silencia", "silencio"]):
                vol.SetMute(1, None)
                return "Sistema silenciado."
            elif any(w in text for w in ["unmute", "activa", "quita silencio"]):
                vol.SetMute(0, None)
                return "Silencio desactivado."
        except Exception as e:
            return f"No pude controlar el volumen: {e}"

    # Screenshot
    if any(w in text for w in ["screenshot", "captura", "pantalla", "capture"]):
        try:
            import pyautogui
            from datetime import datetime
            path = os.path.join(os.path.expanduser("~"), "Desktop",
                                f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            img = pyautogui.screenshot()
            img.save(path)
            return f"Captura guardada en {path}"
        except Exception as e:
            return f"Error al tomar captura: {e}"

    # Shutdown / restart
    if any(w in text for w in ["apaga", "shutdown", "apagar"]):
        subprocess.run("shutdown /s /t 10", shell=True)
        return "El equipo se apagará en 10 segundos."
    if any(w in text for w in ["reinicia", "restart", "reboot"]):
        subprocess.run("shutdown /r /t 10", shell=True)
        return "El equipo se reiniciará en 10 segundos."
    if any(w in text for w in ["bloquea", "lock"]):
        subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True)
        return "Pantalla bloqueada."

    # Dark mode toggle
    if any(w in text for w in ["dark mode", "modo oscuro", "modo claro", "light mode"]):
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r"Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize",
                0, winreg.KEY_ALL_ACCESS)
            val, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            new_val = 0 if val == 1 else 1
            winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, new_val)
            winreg.CloseKey(key)
            return "Modo oscuro activado." if new_val == 0 else "Modo claro activado."
        except Exception as e:
            return f"No pude cambiar el tema: {e}"

    # Keyboard shortcut
    if any(w in text for w in ["atajo", "shortcut", "hotkey", "presiona"]):
        try:
            import pyautogui
            if value:
                keys = [k.strip() for k in value.split("+")]
                pyautogui.hotkey(*keys)
                return f"Atajo {value} ejecutado."
        except Exception as e:
            return f"Error al ejecutar atajo: {e}"

    # Type text
    if any(w in text for w in ["escribe", "type", "escribir"]):
        try:
            import pyautogui, pyperclip
            text_to_type = value or parameters.get("value", "")
            pyperclip.copy(text_to_type)
            pyautogui.hotkey("ctrl", "v")
            return f"Texto escrito."
        except Exception as e:
            return f"Error al escribir: {e}"

    return f"Acción '{action}' no reconocida. Prueba con: volumen, screenshot, apagar, reiniciar, bloquear."
'''

# ─── web_search ──────────────────────────────────────────────────────────────
files["web_search.py"] = '''
import webbrowser

def web_search(parameters=None, player=None, **kwargs):
    if not parameters:
        return "No se especificó la búsqueda."
    query = parameters.get("query", "").strip()
    mode  = parameters.get("mode", "search")

    if not query:
        return "Consulta vacía."

    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddg:
            results = list(ddg.text(query, max_results=5))
        if not results:
            webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
            return f"No encontré resultados locales. Abriendo Google para: {query}"
        lines = [f"Resultados para '{query}':"]
        for r in results[:3]:
            lines.append(f"- {r.get('title','')}: {r.get('body','')[:120]}")
        return "\\n".join(lines)
    except ImportError:
        webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        return f"Búsqueda de '{query}' abierta en el navegador."
    except Exception as e:
        webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        return f"Búsqueda abierta en el navegador: {e}"
'''

# ─── weather_report ──────────────────────────────────────────────────────────
files["weather_report.py"] = '''
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
'''

# ─── news ────────────────────────────────────────────────────────────────────
files["news.py"] = '''
import webbrowser

def news(parameters=None, player=None, speak=None, **kwargs):
    if not parameters:
        return "No se especificó la acción."
    action   = parameters.get("action", "top")
    query    = parameters.get("query", "")
    category = parameters.get("category", "")
    max_r    = parameters.get("max_results", 5)

    search_query = query or category or "noticias"

    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddg:
            results = list(ddg.news(search_query, max_results=max_r))
        if not results:
            return f"No encontré noticias sobre '{search_query}'."
        lines = [f"Noticias sobre '{search_query}':"]
        for r in results:
            lines.append(f"- {r.get('title','')}: {r.get('body','')[:100]}")
        return "\\n".join(lines)
    except ImportError:
        webbrowser.open(f"https://news.google.com/search?q={search_query.replace(' ', '+')}")
        return "Instalá duckduckgo-search para obtener noticias. Abriendo Google News."
    except Exception as e:
        return f"Error al buscar noticias: {e}"
'''

# ─── browser_control ─────────────────────────────────────────────────────────
files["browser_control.py"] = '''
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
                    subprocess.Popen([name, target], shell=True)
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
'''

# ─── youtube_video ───────────────────────────────────────────────────────────
files["youtube_video.py"] = '''
import webbrowser, urllib.parse

def youtube_video(parameters=None, response=None, player=None, **kwargs):
    if not parameters:
        return "No se especificó la acción."
    action = parameters.get("action", "play")
    query  = parameters.get("query", "")
    url    = parameters.get("url", "")

    if action == "play" and query:
        search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        webbrowser.open(search_url)
        return f"Buscando '{query}' en YouTube."

    if action == "play" and url:
        webbrowser.open(url)
        return f"Abriendo video en YouTube."

    if action == "trending":
        region = parameters.get("region", "AR")
        webbrowser.open(f"https://www.youtube.com/feed/trending?gl={region}")
        return f"Abriendo videos tendencia en YouTube."

    if action in ("summarize", "get_info") and url:
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            video_id = url.split("v=")[-1].split("&")[0]
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["es", "en"])
            text = " ".join([t["text"] for t in transcript[:50]])
            return f"Transcripción (primeros 50 segmentos): {text[:500]}..."
        except Exception as e:
            webbrowser.open(url)
            return f"No pude obtener transcripción: {e}"

    webbrowser.open("https://www.youtube.com")
    return "Abriendo YouTube."
'''

# ─── spotify_control ─────────────────────────────────────────────────────────
files["spotify_control.py"] = '''
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
            subprocess.Popen(["spotify", "--uri", search_url], shell=True)
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
'''

# ─── screen_processor ────────────────────────────────────────────────────────
files["screen_processor.py"] = '''
import os
from datetime import datetime

def screen_process(parameters=None, response=None, player=None,
                   session_memory=None, speak_func=None, **kwargs):
    source   = (parameters or {}).get("source", "screen")
    question = (parameters or {}).get("question", "¿Qué ves en la pantalla?")

    try:
        if source == "camera":
            import cv2
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()
            if not ret:
                if speak_func:
                    speak_func("No pude acceder a la cámara.")
                return "Error al acceder a la cámara."
            path = os.path.join(os.path.expanduser("~"), "Desktop",
                                f"cam_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            cv2.imwrite(path, frame)
        else:
            import pyautogui
            path = os.path.join(os.path.expanduser("~"), "Desktop",
                                f"screen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            img = pyautogui.screenshot()
            img.save(path)

        # Try to analyze with Gemini
        try:
            from google import genai
            from core.config import get_api_key
            import PIL.Image
            client = genai.Client(api_key=get_api_key())
            image  = PIL.Image.open(path)
            resp   = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[question, image]
            )
            result = resp.text
            if speak_func:
                speak_func(result[:300])
            return result
        except Exception as e:
            msg = f"Captura guardada en {path}. No pude analizar: {e}"
            if speak_func:
                speak_func(msg)
            return msg

    except Exception as e:
        msg = f"Error al capturar pantalla: {e}"
        if speak_func:
            speak_func(msg)
        return msg
'''

# ─── file_controller ─────────────────────────────────────────────────────────
files["file_controller.py"] = '''
import os, shutil, glob

SHORTCUTS = {
    "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
    "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
    "documents": os.path.join(os.path.expanduser("~"), "Documents"),
    "home": os.path.expanduser("~"),
}

def _resolve(path):
    if not path:
        return os.path.expanduser("~")
    return SHORTCUTS.get(path.lower().strip(), os.path.expandvars(path))

def file_controller(parameters=None, player=None, **kwargs):
    if not parameters:
        return "No se especificó la acción."
    action = parameters.get("action", "list")
    path   = _resolve(parameters.get("path", ""))

    if action == "list":
        try:
            items = os.listdir(path)
            return f"Contenido de {path}:\\n" + "\\n".join(items[:30])
        except Exception as e:
            return f"Error al listar: {e}"

    if action == "create_file":
        name    = parameters.get("name", "nuevo.txt")
        content = parameters.get("content", "")
        full    = os.path.join(path, name)
        try:
            with open(full, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Archivo creado: {full}"
        except Exception as e:
            return f"Error al crear archivo: {e}"

    if action == "create_folder":
        name = parameters.get("name", "nueva_carpeta")
        full = os.path.join(path, name)
        try:
            os.makedirs(full, exist_ok=True)
            return f"Carpeta creada: {full}"
        except Exception as e:
            return f"Error al crear carpeta: {e}"

    if action == "delete":
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            return f"Eliminado: {path}"
        except Exception as e:
            return f"Error al eliminar: {e}"

    if action == "move":
        dest = _resolve(parameters.get("destination", ""))
        try:
            shutil.move(path, dest)
            return f"Movido a: {dest}"
        except Exception as e:
            return f"Error al mover: {e}"

    if action == "copy":
        dest = _resolve(parameters.get("destination", ""))
        try:
            if os.path.isdir(path):
                shutil.copytree(path, os.path.join(dest, os.path.basename(path)))
            else:
                shutil.copy2(path, dest)
            return f"Copiado a: {dest}"
        except Exception as e:
            return f"Error al copiar: {e}"

    if action == "rename":
        new_name = parameters.get("new_name", "")
        new_path = os.path.join(os.path.dirname(path), new_name)
        try:
            os.rename(path, new_path)
            return f"Renombrado a: {new_name}"
        except Exception as e:
            return f"Error al renombrar: {e}"

    if action == "read":
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read(3000)
            return content
        except Exception as e:
            return f"Error al leer: {e}"

    if action == "write":
        content = parameters.get("content", "")
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Escrito en: {path}"
        except Exception as e:
            return f"Error al escribir: {e}"

    if action == "find":
        name = parameters.get("name", "")
        ext  = parameters.get("extension", "")
        pattern = f"**/*{name}*{ext}" if name else f"**/*{ext}"
        try:
            results = glob.glob(os.path.join(path, pattern), recursive=True)[:10]
            return "\\n".join(results) if results else "No se encontraron archivos."
        except Exception as e:
            return f"Error al buscar: {e}"

    if action == "disk_usage":
        try:
            usage = shutil.disk_usage(path)
            total = usage.total // (1024**3)
            used  = usage.used  // (1024**3)
            free  = usage.free  // (1024**3)
            return f"Disco: Total={total}GB | Usado={used}GB | Libre={free}GB"
        except Exception as e:
            return f"Error al obtener uso de disco: {e}"

    if action == "info":
        try:
            stat = os.stat(path)
            return (f"Ruta: {path}\\nTamaño: {stat.st_size} bytes\\n"
                    f"Es directorio: {os.path.isdir(path)}")
        except Exception as e:
            return f"Error: {e}"

    return f"Acción '{action}' no reconocida."
'''

# ─── file_processor ──────────────────────────────────────────────────────────
files["file_processor.py"] = '''
import os

def file_processor(parameters=None, player=None, speak=None, **kwargs):
    if not parameters:
        return "No se especificó la acción."
    file_path   = parameters.get("file_path", "")
    action      = parameters.get("action", "")
    instruction = parameters.get("instruction", "")

    if not file_path or not os.path.exists(file_path):
        return f"Archivo no encontrado: {file_path}"

    ext = os.path.splitext(file_path)[1].lower()

    # Images
    if ext in (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"):
        if action == "describe":
            try:
                from google import genai
                from core.config import get_api_key
                import PIL.Image
                client = genai.Client(api_key=get_api_key())
                img    = PIL.Image.open(file_path)
                resp   = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[instruction or "Describe esta imagen en español.", img]
                )
                return resp.text
            except Exception as e:
                return f"Error al analizar imagen: {e}"
        if action in ("resize", "compress", "convert"):
            try:
                from PIL import Image
                img = Image.open(file_path)
                if action == "resize":
                    w = parameters.get("width", img.width // 2)
                    h = parameters.get("height", img.height // 2)
                    img = img.resize((w, h))
                out = file_path.replace(ext, f"_{action}{ext}")
                quality = parameters.get("quality", 85)
                img.save(out, quality=quality)
                return f"Imagen procesada: {out}"
            except Exception as e:
                return f"Error al procesar imagen: {e}"

    # Text / docs
    if ext in (".txt", ".md", ".py", ".js", ".html", ".css", ".json", ".csv"):
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read(5000)
            if action in ("summarize", "fix", "explain", "review"):
                try:
                    from google import genai
                    from core.config import get_api_key
                    prompts = {
                        "summarize": "Resume este texto en español:",
                        "fix": "Corrige errores en este código:",
                        "explain": "Explica este código en español:",
                        "review": "Revisa y mejora este código:",
                    }
                    client = genai.Client(api_key=get_api_key())
                    resp   = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[prompts.get(action, instruction) + "\\n\\n" + content]
                    )
                    return resp.text
                except Exception as e:
                    return f"Contenido del archivo (análisis no disponible: {e}):\\n{content[:500]}"
            return content[:2000]
        except Exception as e:
            return f"Error al leer archivo: {e}"

    # PDF
    if ext == ".pdf":
        try:
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                text = " ".join(p.extract_text() or "" for p in pdf.pages[:5])
            return text[:2000] if text else "PDF sin texto extraíble."
        except ImportError:
            try:
                import PyPDF2
                with open(file_path, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    text = " ".join(p.extract_text() or "" for p in reader.pages[:5])
                return text[:2000]
            except Exception as e:
                return f"Error al leer PDF: {e}"

    return f"Tipo de archivo {ext} no soportado para acción '{action}'."
'''

# ─── pdf_tools ───────────────────────────────────────────────────────────────
files["pdf_tools.py"] = '''
import os

def pdf_tools(parameters=None, player=None, speak=None, **kwargs):
    if not parameters:
        return "No se especificó la acción."
    action    = parameters.get("action", "read")
    file_path = parameters.get("file_path", "")
    pages_str = parameters.get("pages", "")

    if action == "read":
        try:
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                text = "\\n".join(p.extract_text() or "" for p in pdf.pages[:10])
            return text[:3000] if text else "PDF sin texto."
        except ImportError:
            try:
                import PyPDF2
                with open(file_path, "rb") as f:
                    r = PyPDF2.PdfReader(f)
                    text = "\\n".join(p.extract_text() or "" for p in r.pages[:10])
                return text[:3000]
            except Exception as e:
                return f"Error: {e}"

    if action == "info":
        try:
            import PyPDF2
            with open(file_path, "rb") as f:
                r = PyPDF2.PdfReader(f)
                return (f"PDF: {file_path}\\n"
                        f"Páginas: {len(r.pages)}\\n"
                        f"Metadatos: {r.metadata}")
        except Exception as e:
            return f"Error: {e}"

    if action == "merge":
        files_str = parameters.get("files", "")
        out_name  = parameters.get("output_name", "merged.pdf")
        try:
            import PyPDF2
            writer = PyPDF2.PdfWriter()
            for fp in files_str.split(","):
                fp = fp.strip()
                if os.path.exists(fp):
                    with open(fp, "rb") as f:
                        reader = PyPDF2.PdfReader(f)
                        for page in reader.pages:
                            writer.add_page(page)
            out_path = os.path.join(os.path.dirname(file_path), out_name)
            with open(out_path, "wb") as f:
                writer.write(f)
            return f"PDFs combinados en: {out_path}"
        except Exception as e:
            return f"Error al combinar: {e}"

    if action == "split":
        try:
            import PyPDF2
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                base   = os.path.splitext(file_path)[0]
                for i, page in enumerate(reader.pages):
                    writer = PyPDF2.PdfWriter()
                    writer.add_page(page)
                    out = f"{base}_page_{i+1}.pdf"
                    with open(out, "wb") as fout:
                        writer.write(fout)
            return f"PDF dividido en {len(reader.pages)} archivos."
        except Exception as e:
            return f"Error al dividir: {e}"

    return f"Acción PDF '{action}' no reconocida."
'''

# ─── backup ──────────────────────────────────────────────────────────────────
files["backup.py"] = '''
import os, shutil
from datetime import datetime

def backup(parameters=None, player=None, speak=None, **kwargs):
    if not parameters:
        return "No se especificó la acción."
    action  = parameters.get("action", "run")
    source  = parameters.get("source", "")
    destination = parameters.get("destination", "")

    if not source or not os.path.exists(source):
        return f"Origen no encontrado: {source}"

    if action == "run":
        if not destination:
            destination = os.path.join(os.path.expanduser("~"), "Desktop", "Backups")
        os.makedirs(destination, exist_ok=True)
        ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = os.path.basename(source.rstrip("\\\\/"))
        dest_path = os.path.join(destination, f"{name}_{ts}")
        try:
            if os.path.isdir(source):
                shutil.copytree(source, dest_path)
            else:
                shutil.copy2(source, dest_path)
            return f"Backup completado: {dest_path}"
        except Exception as e:
            return f"Error al hacer backup: {e}"

    return f"Acción de backup '{action}' no reconocida."
'''

# ─── system_monitor ──────────────────────────────────────────────────────────
files["system_monitor.py"] = '''
def system_monitor(parameters=None, player=None, speak=None, **kwargs):
    action = (parameters or {}).get("action", "full")
    try:
        import psutil
        lines = []
        if action in ("cpu", "full"):
            cpu = psutil.cpu_percent(interval=1)
            lines.append(f"CPU: {cpu}%")
        if action in ("ram", "full"):
            ram = psutil.virtual_memory()
            lines.append(f"RAM: {ram.percent}% usado ({ram.used//1024**2}MB / {ram.total//1024**2}MB)")
        if action in ("disk", "full"):
            disk = psutil.disk_usage("/")
            lines.append(f"Disco: {disk.percent}% ({disk.used//1024**3}GB / {disk.total//1024**3}GB)")
        if action in ("battery", "full"):
            bat = psutil.sensors_battery()
            if bat:
                lines.append(f"Batería: {bat.percent:.0f}% {'(cargando)' if bat.power_plugged else ''}")
        if action in ("processes", "full"):
            procs = sorted(psutil.process_iter(["name", "cpu_percent", "memory_percent"]),
                           key=lambda p: p.info["cpu_percent"] or 0, reverse=True)[:5]
            for p in procs:
                lines.append(f"  {p.info['name']}: CPU={p.info['cpu_percent']}% MEM={p.info['memory_percent']:.1f}%")
        if action in ("uptime", "full"):
            import time
            boot = psutil.boot_time()
            up   = int(time.time() - boot)
            h, m = divmod(up // 60, 60)
            lines.append(f"Uptime: {h}h {m}m")
        return "\\n".join(lines) if lines else "Sin datos."
    except ImportError:
        return "Instalá psutil: pip install psutil"
    except Exception as e:
        return f"Error: {e}"
'''

# ─── translator ──────────────────────────────────────────────────────────────
files["translator.py"] = '''
def translator(parameters=None, player=None, speak=None, **kwargs):
    if not parameters:
        return "No se especificó el texto."
    text        = parameters.get("text", "")
    target_lang = parameters.get("target_lang", "english")
    source_lang = parameters.get("source_lang", "")

    if not text:
        return "Texto vacío."

    try:
        from google import genai
        from core.config import get_api_key
        prompt = f"Translate the following text to {target_lang}. Return ONLY the translation, no explanation:\\n\\n{text}"
        client = genai.Client(api_key=get_api_key())
        resp   = client.models.generate_content(model="gemini-2.0-flash", contents=[prompt])
        return resp.text.strip()
    except Exception as e:
        return f"Error al traducir: {e}"
'''

# ─── stocks_crypto ───────────────────────────────────────────────────────────
files["stocks_crypto.py"] = '''
import requests

def stocks_crypto(parameters=None, player=None, speak=None, **kwargs):
    if not parameters:
        return "No se especificó el símbolo."
    action = parameters.get("action", "stock")
    symbol = parameters.get("symbol", "").strip()

    if action == "crypto":
        name_map = {
            "btc": "bitcoin", "eth": "ethereum", "sol": "solana",
            "ada": "cardano", "doge": "dogecoin", "xrp": "ripple",
        }
        coin = name_map.get(symbol.lower(), symbol.lower())
        try:
            r = requests.get(
                f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd",
                timeout=8
            )
            data = r.json()
            if coin in data:
                price = data[coin]["usd"]
                return f"{coin.capitalize()}: ${price:,.2f} USD"
            return f"No encontré datos para {symbol}."
        except Exception as e:
            return f"Error al consultar crypto: {e}"

    if action == "stock":
        try:
            r = requests.get(
                f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d",
                headers={"User-Agent": "Mozilla/5.0"}, timeout=8
            )
            data = r.json()
            price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
            return f"{symbol.upper()}: ${price:,.2f} USD"
        except Exception as e:
            return f"Error al consultar {symbol}: {e}"

    return "Acción no reconocida. Usa: stock o crypto."
'''

# ─── recipes ─────────────────────────────────────────────────────────────────
files["recipes.py"] = '''
import webbrowser

def recipes(parameters=None, player=None, speak=None, **kwargs):
    if not parameters:
        return "No se especificó la acción."
    action = parameters.get("action", "search")
    query  = parameters.get("query", "")

    if action == "search" and query:
        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddg:
                results = list(ddg.text(f"receta {query}", max_results=3))
            lines = [f"Recetas para '{query}':"]
            for r in results:
                lines.append(f"- {r.get('title','')}: {r.get('body','')[:120]}")
            return "\\n".join(lines)
        except:
            webbrowser.open(f"https://www.google.com/search?q=receta+{query.replace(' ', '+')}")
            return f"Búsqueda de recetas abierta en el navegador."

    if action == "random":
        webbrowser.open("https://www.recetasgratis.net/recetas-al-azar.html")
        return "Abriendo recetas aleatorias."

    return "Acción no reconocida."
'''

# ─── calendar_manager ────────────────────────────────────────────────────────
files["calendar_manager.py"] = '''
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
        return "\\n".join(lines) if len(lines) > 1 else "No hay eventos próximos."

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
'''

# ─── Stubs para módulos complejos ─────────────────────────────────────────────
STUBS = {
    "computer_control.py": "computer_control",
    "desktop.py": "desktop_control",
    "code_helper.py": "code_helper",
    "dev_agent.py": "dev_agent",
    "game_updater.py": "game_updater",
    "flight_finder.py": "flight_finder",
    "agata_creator.py": None,
    "clipboard_manager.py": "clipboard_manager",
    "file_converter.py": "file_converter",
    "database_query.py": "database_query",
    "scheduler.py": "scheduler",
    "email_manager.py": "email_manager",
    "macro_recorder.py": "macro_recorder",
    "workflow.py": "workflow",
    "podcast.py": "podcast",
    "web_builder.py": "web_builder",
    "slide_builder.py": "slide_builder",
    "send_message.py": "send_message",
    "reminder.py": "reminder",
}

for fname, fn in STUBS.items():
    if fname not in files:
        if fname == "agata_creator.py":
            files[fname] = (
                "def agata_create(*a, **kw): return 'Agata no implementada.'\n"
                "def list_palettes(*a, **kw): return 'Sin paletas disponibles.'\n"
            )
        else:
            files[fname] = f"def {fn}(*args, **kwargs): return 'Función {fn} no implementada aún.'\n"

# ─── Escritura ────────────────────────────────────────────────────────────────
count = 0
for filename, content in files.items():
    path = os.path.join(BASE, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    count += 1

# __init__.py
init_path = os.path.join(BASE, "__init__.py")
if not os.path.exists(init_path):
    open(init_path, "w").close()

print(f"✅ {count} módulos de actions creados en: {BASE}")
print("Ahora ejecutá: python main.py")
