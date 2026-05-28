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
        return "\n".join(lines)
    except ImportError:
        webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        return f"Búsqueda de '{query}' abierta en el navegador."
    except Exception as e:
        webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        return f"Búsqueda abierta en el navegador: {e}"
