from app.adapters.daily_content import DailyContentAdapter
from app.schemas.dashboard import DailyContentModule

class DailyContentService:
    @classmethod
    async def get_daily_content(cls) -> DailyContentModule:
        return await DailyContentAdapter.get_daily_content_module()
