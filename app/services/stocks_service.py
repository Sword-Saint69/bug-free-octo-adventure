from typing import List
from app.adapters.stocks import StocksAdapter
from app.schemas.dashboard import StockQuote

class StocksService:
    @classmethod
    async def get_stocks(cls) -> List[StockQuote]:
        return await StocksAdapter.fetch_stock_quotes()
