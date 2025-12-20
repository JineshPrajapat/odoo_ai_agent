from email.mime import text
from app.odoo.auth import OdooAuthService
from app.core.database import engine
from sqlalchemy import text

def check_db_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Database connected successfully")
    except Exception as e:
        print("❌ Database connection failed:", e)

def check_odoo_connection():
    try:
        uid = OdooAuthService().authenticate()
        print(f"✅ Odoo connected successfully (uid={uid})")
    except Exception as e:
        print("❌ Odoo connection failed:", e)
        raise
