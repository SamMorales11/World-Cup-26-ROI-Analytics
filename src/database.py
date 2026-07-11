import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Memuat environment variables dari file .env
load_dotenv()

def get_db_engine():
    """
    Membuat dan mengembalikan database engine SQLAlchemy untuk Neon Tech PostgreSQL.
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("❌ DATABASE_URL tidak ditemukan di file .env. Pastikan Anda sudah membuatnya.")
    
    # Neon Tech menggunakan SSL, pastikan parameter sslmode=require ada di URI
    if "sslmode=require" not in database_url:
        if "?" in database_url:
            database_url += "&sslmode=require"
        else:
            database_url += "?sslmode=require"
            
    return create_engine(database_url)