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
