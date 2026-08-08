import httpx
from typing import Optional, List
from pydantic import BaseModel

class CryptoQuote(BaseModel):
    symbol: str
    price_usd: float
    change_24h: float
    freshness_sec: int

class CoinGeckoAdapter:
    BASE_URL = "https://api.coingecko.com/api/v3/simple/price"

    @classmethod
    async def fetch_crypto_prices(cls, coin_ids: List[str] = ["bitcoin", "ethereum", "solana"]) -> List[CryptoQuote]:
        ids_param = ",".join(coin_ids)
        params = {
            "ids": ids_param,
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        }
        async with httpx.AsyncClient(timeout=4.0) as client:
            try:
                response = await client.get(cls.BASE_URL, params=params)
                if response.status_code == 200:
                    data = response.json()
                    quotes = []
                    for coin_id in coin_ids:
                        if coin_id in data:
                            coin_data = data[coin_id]
                            quotes.append(
                                CryptoQuote(
                                    symbol=coin_id.upper(),
                                    price_usd=coin_data.get("usd", 0.0),
                                    change_24h=round(coin_data.get("usd_24h_change", 0.0), 2),
                                    freshness_sec=0
                                )
                            )
                    return quotes
            except Exception:
                return []
        return []
