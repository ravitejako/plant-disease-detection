from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    
    def get_db(self):
        """Return database instance"""
        return self.client[settings.DATABASE_NAME]

    async def connect_to_database(self):
        """Create database connection."""
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URL)
            logger.info("Connected to MongoDB.")
        except Exception as e:
            logger.error(f"Could not connect to MongoDB: {e}")
            raise

    async def close_database_connection(self):
        """Close database connection."""
        try:
            self.client.close()
            logger.info("Closed MongoDB connection.")
        except Exception as e:
            logger.error(f"Could not close MongoDB connection: {e}")
            raise

# Create a database instance
db = Database() 