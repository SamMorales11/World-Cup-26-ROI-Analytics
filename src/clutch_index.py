import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database import get_db_engine

def calculate_clutch_index():
    """Menganalisis gol di atas menit ke-80 untuk menyaring Clutch Players"""
    try:
        engine = get_db_engine()
        
        # Tarik semua data menit sebagai teks terlebih dahulu tanpa filter >= 80 di SQL
        query = """
        SELECT 
            p.player_name,
            me.match_id,
            me.minute,
            me.event_type
        FROM match_events me
        JOIN squads_and_players p ON me.player_id = p.player_id
        WHERE LOWER(me.event_type) LIKE '%%goal%%';
        """
        
        df_events = pd.read_sql(query, engine)
        
        if df_events.empty:
            print("⚠️ Tidak ditemukan data event gol pertandingan.")
            return
            
        # Pembersihan menit: Jika ada tambahan waktu seperti '90+2', ambil angka utamanya '90'
        df_events['minute_cleaned'] = df_events['minute'].astype(str).str.split('+').str[0]
        
        # Ubah secara paksa menjadi tipe data numerik
        df_events['minute_cleaned'] = pd.to_numeric(df_events['minute_cleaned'], errors='coerce').fillna(0).astype(int)
        
        # Lakukan filter menit >= 80 di layer Pandas DataFrame
        df_clutch = df_events[df_events['minute_cleaned'] >= 80].copy()
        
        if df_clutch.empty:
            print("⚠️ Tidak ditemukan data gol di atas menit ke-80 setelah pembersihan data.")
            return
            
        # Menghitung akumulasi gol late-game per pemain
        clutch_players = df_clutch.groupby(['player_name']).size().reset_index(name='late_goals')
        clutch_players = clutch_players.sort_values(by='late_goals', ascending=False).head(10)
        
        print("\n🏆 TOP 10 CLUTCH PLAYER INDEX (Goals Scored after 80') :")
        print("=====================================================================")
        print(clutch_players.to_string(index=False))
        print("=====================================================================")
        
    except Exception as e:
        print(f"❌ Gagal memproses Clutch Player Index: {e}")

if __name__ == "__main__":
    calculate_clutch_index()