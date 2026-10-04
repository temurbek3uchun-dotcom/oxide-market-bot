import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_IDS = [int(admin_id.strip()) for admin_id in os.getenv("ADMIN_IDS", "").split(",") if admin_id.strip()]
COMMISSION_PERCENT = float(os.getenv("COMMISSION_PERCENT", "10"))
MIN_COMMISSION = int(os.getenv("MIN_COMMISSION", "5000"))
VERIFICATION_PERIOD_MINUTES = int(os.getenv("VERIFICATION_PERIOD_MINUTES", "30"))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./shop.db")
