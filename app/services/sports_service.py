from app.adapters.sports import SportsAdapter
from app.schemas.dashboard import SportsModule

class SportsService:
    @classmethod
    async def get_sports(cls) -> SportsModule:
        return await SportsAdapter.get_sports_module()
