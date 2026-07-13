import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database import get_db_engine

def train_market_value_predictor():
    try:
        engine = get_db_engine()
        
        # 1. Query Relational Data (Menghapus filter WHERE di tingkat SQL untuk menghindari error tipe data)
        query = """
        SELECT 
            s.goals,
            s.assists,
            s.minutes_played,
            p.market_value_eur
        FROM squads_and_players p
        JOIN player_stats s ON p.player_id = s.player_id;
        """
        
        df = pd.read_sql(query, engine)
        
        # 2. Data Preprocessing (Pembersihan Tipe Data String ke Numerik)
        # Bersihkan kolom market value
        df['market_value_eur'] = df['market_value_eur'].astype(str)\
            .str.replace('€', '', regex=False)\
            .str.replace(',', '', regex=False)\
            .str.replace('.', '', regex=False).str.strip()
        df['market_value_eur'] = pd.to_numeric(df['market_value_eur'], errors='coerce').fillna(0)
        
        # Bersihkan fitur performa lainnya termasuk minutes_played secara aman
        df['goals'] = pd.to_numeric(df['goals'], errors='coerce').fillna(0).astype(int)
        df['assists'] = pd.to_numeric(df['assists'], errors='coerce').fillna(0).astype(int)
        df['minutes_played'] = pd.to_numeric(df['minutes_played'], errors='coerce').fillna(0).astype(int)
        
        # 3. Filter Data di Layer Pandas (Menyaring menit > 0 dan harga > 0 secara aman)
        df = df[(df['market_value_eur'] > 0) & (df['minutes_played'] > 0)].copy()
        
        # Mengubah target ke satuan Juta EUR agar skala prediksi lebih mudah dibaca
        df['market_value_m_eur'] = df['market_value_eur'] / 1_000_000

        # 4. Simulasi Kenaikan Harga Pasar (Target Variabel berbasis performa turnamen)
        np.random.seed(42)
        df['market_value_increase_m_eur'] = ((df['goals'] * 2.5) + (df['assists'] * 1.5) + (df['market_value_m_eur'] * 0.1))
        # Tambahkan noise statistik normal acak
        df['market_value_increase_m_eur'] += np.random.normal(0, 1, size=len(df))
        df['market_value_increase_m_eur'] = df['market_value_increase_m_eur'].clip(lower=0) 

        # 5. Menentukan Fitur (X) dan Target (y)
        X = df[['goals', 'assists', 'minutes_played']]
        y = df['market_value_increase_m_eur']
        
        # 6. Split Data (80% Training, 20% Testing) untuk validasi performa model
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # 7. Inisialisasi dan Training Model Linear Regression
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # 8. Evaluasi Model Menggunakan Data Testing
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        print("\n📈 VALUEPITCH 2026: MACHINE LEARNING MODEL REPORT")
        print("=====================================================================")
        print(f"Fitur Utama yang Digunakan : {list(X.columns)}")
        print(f"Intercept Model            : {model.intercept_:.2f}")
        print(f"Koefisien Bobot (Goals)    : {model.coef_[0]:.4f}")
        print(f"Koefisien Bobot (Assists)  : {model.coef_[1]:.4f}")
        print(f"Koefisien Bobot (Minutes)  : {model.coef_[2]:.4f}")
        print("---------------------------------------------------------------------")
        print(f"R-squared (R2 Score)       : {r2:.4f} ({r2*100:.2f}%)")
        print(f"Rata-rata Error (RMSE)     : {rmse:.2f} Million EUR")
        print("=====================================================================")
        
        # 9. Simulasi Prediksi untuk Pemain Rekomendasi Scout
        scouted_player = pd.DataFrame([[3, 1, 270]], columns=['goals', 'assists', 'minutes_played'])
        predicted_value = model.predict(scouted_player)
        
        print(f"💡 Hasil Prediksi Scout:")
        print(f"   Pemain dengan 3 Gol & 1 Asis layak dihargai: +€{predicted_value[0]:.2f} Juta EUR\n")
        
    except Exception as e:
        print(f"❌ Gagal melatih model regresi: {e}")

if __name__ == "__main__":
    train_market_value_predictor()