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
