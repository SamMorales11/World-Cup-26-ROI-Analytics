import pandas as pd
from src.database import get_db_engine

engine = get_db_engine()

print("📋 Kolom di tabel 'teams':")
print(pd.read_sql("SELECT * FROM teams LIMIT 1;", engine).columns.tolist())

print("\n📋 Kolom di tabel 'tournament_stages' (jika ada data fase):")
try:
    print(pd.read_sql("SELECT * FROM tournament_stages LIMIT 1;", engine).columns.tolist())
except Exception as e:
    print("Tidak ada tabel tournament_stages atau error:", e)