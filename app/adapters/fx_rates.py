import httpx
from typing import Optional
from pydantic import BaseModel

class CurrencyRate(BaseModel):
    base_currency: str
    target_currency: str
    rate: float
    rate_date: str

class FrankfurterFXAdapter:
    BASE_URL = "https://api.frankfurter.dev/v1/latest"

    @classmethod
    async def fetch_fx_rate(cls, base: str = "USD", target: str = "EUR") -> Optional[CurrencyRate]:
        params = {"base": base, "symbols": target}
        async with httpx.AsyncClient(timeout=4.0) as client:
            try:
                response = await client.get(cls.BASE_URL, params=params)
                if response.status_code == 200:
                    data = response.json()
                    rates = data.get("rates", {})
                    if target in rates:
                        return CurrencyRate(
                            base_currency=base,
                            target_currency=target,
                            rate=rates[target],
                            rate_date=data.get("date", "")
                        )
            except Exception:
                return None
        return None
