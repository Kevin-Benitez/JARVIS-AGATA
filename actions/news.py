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
        return "\n".join(lines)
    except ImportError:
        webbrowser.open(f"https://news.google.com/search?q={search_query.replace(' ', '+')}")
        return "Instalá duckduckgo-search para obtener noticias. Abriendo Google News."
    except Exception as e:
        return f"Error al buscar noticias: {e}"
