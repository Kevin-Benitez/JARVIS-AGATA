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
                        contents=[prompts.get(action, instruction) + "\n\n" + content]
                    )
                    return resp.text
                except Exception as e:
                    return f"Contenido del archivo (análisis no disponible: {e}):\n{content[:500]}"
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
