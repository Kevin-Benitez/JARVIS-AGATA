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
            return "\n".join(lines)
        except:
            webbrowser.open(f"https://www.google.com/search?q=receta+{query.replace(' ', '+')}")
            return f"Búsqueda de recetas abierta en el navegador."

    if action == "random":
        webbrowser.open("https://www.recetasgratis.net/recetas-al-azar.html")
        return "Abriendo recetas aleatorias."

    return "Acción no reconocida."
