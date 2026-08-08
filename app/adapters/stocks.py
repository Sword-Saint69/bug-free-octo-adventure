import httpx
from typing import List
from app.schemas.dashboard import StockQuote

class StocksAdapter:
    # Keyless Yahoo Finance v8 chart query API
    BASE_URL = "https://query1.finance.yahoo.com/v8/finance/chart/"

    # Default stock and index symbols to monitor
    DEFAULT_SYMBOLS = [
        {"symbol": "^GSPC", "name": "S&P 500"},
        {"symbol": "^IXIC", "name": "NASDAQ"},
        {"symbol": "^NSEI", "name": "NIFTY 50"},
        {"symbol": "GC=F", "name": "Gold"},
        {"symbol": "CL=F", "name": "Crude Oil"},
        {"symbol": "AAPL", "name": "Apple Inc."}
    ]

    @classmethod
    async def fetch_stock_quotes(cls) -> List[StockQuote]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko)"
        }
        quotes: List[StockQuote] = []
        async with httpx.AsyncClient(timeout=4.0, headers=headers) as client:
            for item in cls.DEFAULT_SYMBOLS:
                symbol = item["symbol"]
                name = item["name"]
                try:
                    url = f"{cls.BASE_URL}{symbol}"
                    response = await client.get(url, params={"interval": "1d", "range": "2d"})
                    if response.status_code == 200:
                        data = response.json()
                        result = data.get("chart", {}).get("result", [])[0]
                        meta = result.get("meta", {})
                        price = round(meta.get("regularMarketPrice", 0.0), 2)
                        prev_close = meta.get("chartPreviousClose") or meta.get("previousClose") or price
                        change_amt = round(price - prev_close, 2)
                        change_pct = round((change_amt / prev_close * 100) if prev_close else 0.0, 2)
                        currency = meta.get("currency", "USD")

                        if price > 0:
                            quotes.append(
                                StockQuote(
                                    symbol=symbol,
                                    name=name,
                                    price=price,
                                    change_amount=change_amt,
                                    change_percent=change_pct,
                                    currency=currency
                                )
                            )
                except Exception:
                    pass

        return quotes
