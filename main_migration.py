import os
import sqlite3
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

def init_postgres_engine():
    """Memuat .env dan menginisialisasi koneksi ke Neon Tech PostgreSQL"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        raise ValueError("❌ DATABASE_URL tidak ditemukan di file .env! Pastikan file .env sudah dibuat dengan benar.")
    
    # Memastikan parameter SSL aktif untuk keamaan Neon Tech
    if "sslmode=require" not in database_url:
        database_url += "&sslmode=require" if "?" in database_url else "?sslmode=require"
        
    return create_engine(database_url)

def run_full_migration():
    """Membaca seluruh tabel dari SQLite lokal dan mendorongnya ke Neon Tech"""
    # 1. Definisikan Path Database SQLite Lokal
    sqlite_path = os.path.join("data", "raw", "sqlite_fifa_world_cup_2026.db")
    
    # Validasi apakah file SQLite sudah diletakkan di tempat yang benar
    if not os.path.exists(sqlite_path):
        print(f"❌ Error: File database tidak ditemukan di: {sqlite_path}")
        print("💡 Solusi: Pastikan Anda sudah membuat folder 'data/raw/' dan memindahkan file 'sqlite_fifa_world_cup_2026.db' ke dalamnya.")
        return

    print(f"🔄 Membuka database SQLite lokal: {sqlite_path}")
    sqlite_conn = sqlite3.connect(sqlite_path)
    
    try:
        # 2. Inisialisasi Engine PostgreSQL Cloud
        pg_engine = init_postgres_engine()
        print("🔌 Berhasil terhubung ke Cloud Database Neon Tech.")
        print("--------------------------------------------------")

        # 3. Ambil daftar semua tabel yang ada di dalam SQLite
        query_get_tables = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
        tables = pd.read_sql(query_get_tables, sqlite_conn)['name'].tolist()
        
        print(f"📦 Ditemukan {len(tables)} tabel di SQLite: {tables}")
        print("--------------------------------------------------")

        # 4. Iterasi dan migrasi setiap tabel secara otomatis
        for table_name in tables:
            print(f"🚀 Menarik data dari tabel [{table_name}]...")
            
            # Membaca data dari SQLite ke DataFrame Pandas
            df = pd.read_sql(f"SELECT * FROM {table_name};", sqlite_conn)
            
            print(f"   Mengirim {len(df)} baris data ke Neon Tech...")
            # Menulis ke PostgreSQL (if_exists='replace' akan membuat tabel baru jika belum ada)
            df.to_sql(table_name, pg_engine, if_exists='replace', index=False)
            
            print(f"   ✓ Tabel [{table_name}] Sukses Dimigrasikan.\n")
            
        print("--------------------------------------------------")
        print("🎉 [MIGRASI SELESAI] Semua tabel kini sudah aktif di cloud Neon Tech Anda!")

    except Exception as e:
        print(f"❌ Terjadi kesalahan saat proses migrasi berjalan: {e}")
        
    finally:
        # Menutup koneksi database lokal setelah selesai
        sqlite_conn.close()
        print("🔒 Koneksi SQLite lokal ditutup.")

if __name__ == "__main__":
    run_full_migration()