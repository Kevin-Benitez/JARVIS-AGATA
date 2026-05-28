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
        subprocess.run("shutdown /s /t 10", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return "El equipo se apagará en 10 segundos."
    if any(w in text for w in ["reinicia", "restart", "reboot"]):
        subprocess.run("shutdown /r /t 10", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return "El equipo se reiniciará en 10 segundos."
    if any(w in text for w in ["bloquea", "lock"]):
        subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return "Pantalla bloqueada."

    # Dark mode toggle
    if any(w in text for w in ["dark mode", "modo oscuro", "modo claro", "light mode"]):
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
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
