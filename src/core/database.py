import motor
import motor.motor_asyncio
from odmantic import AIOEngine

from src.core.config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
mongoEngine = AIOEngine(client=client, database="kinnema")
