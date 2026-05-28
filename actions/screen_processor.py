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
