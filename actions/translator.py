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
        prompt = f"Translate the following text to {target_lang}. Return ONLY the translation, no explanation:\n\n{text}"
        client = genai.Client(api_key=get_api_key())
        resp   = client.models.generate_content(model="gemini-2.0-flash", contents=[prompt])
        return resp.text.strip()
    except Exception as e:
        return f"Error al traducir: {e}"
