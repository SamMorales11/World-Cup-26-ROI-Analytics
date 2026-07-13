import os
import sys
import pandas as pd
import plotly.express as px

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database import get_db_engine

def analyze_and_visualize_roi():
    """
    Menarik data dari Neon Tech, kalkulasi ROI Score, 
    dan menghasilkan grafik batang horizontal interaktif.
    """
    try:
        engine = get_db_engine()
        
        # 1. Query gabungan data personal pemain dan statistik performa
        query = """
        SELECT 
            p.player_name,
            p.position,
            p.market_value_eur,
            s.goals,
            s.assists,
            s.minutes_played
        FROM squads_and_players p
        JOIN player_stats s ON p.player_id = s.player_id;
        """
        
        df = pd.read_sql(query, engine)
        
        if df.empty:
            print("⚠️ Data tidak ditemukan di database.")
            return

        # 2. Data Preprocessing & Cleaning (String ke Numerik)
        df['market_value_eur'] = df['market_value_eur'].astype(str)\
            .str.replace('€', '', regex=False)\
            .str.replace(',', '', regex=False)\
            .str.replace('.', '', regex=False).str.strip()
        
        df['market_value_eur'] = pd.to_numeric(df['market_value_eur'], errors='coerce').fillna(0)
        df['goals'] = pd.to_numeric(df['goals'], errors='coerce').fillna(0).astype(int)
        df['assists'] = pd.to_numeric(df['assists'], errors='coerce').fillna(0).astype(int)
        df['minutes_played'] = pd.to_numeric(df['minutes_played'], errors='coerce').fillna(0).astype(int)
        
        # Saring pemain (Menit bermain > 90 dan Harga Pasar > 0)
        df = df[(df['market_value_eur'] > 0) & (df['minutes_played'] > 90)].copy()
        df['market_value_m_eur'] = df['market_value_eur'] / 1_000_000
        
        # 3. Kalkulasi ROI Score
        df['roi_score'] = (
            ((df['goals'] * 4.0) + (df['assists'] * 2.5)) / df['market_value_m_eur']
        ) * (df['minutes_played'] / 90)
        
        # Ambil Top 10 ROI tertinggi
        top_roi = df.sort_values(by='roi_score', ascending=False).head(10)
        
        print("\n🔥 TOP 10 UNDERPRICED OVERACHIEVERS BERHASIL DIPROSES.")

        # 4. Membuat Visualisasi Horizontal Bar Chart
        print("🎨 Membuat grafik batang horizontal ROI interaktif...")
        fig = px.bar(
            top_roi,
            x='roi_score',
            y='player_name',
            orientation='h',
            color='roi_score',
            title='<b>ValuePitch 2026: Top 10 Underpriced Overachievers</b><br><sup>Efisiensi Nilai Pemain Berdasarkan Kontribusi Performa vs Harga Pasar</sup>',
            labels={
                'roi_score': 'ROI Score (Higher = Better Value)',
                'player_name': 'Nama Pemain',
                'color': 'Skor ROI'
            },
            color_continuous_scale=px.colors.sequential.Mint, # Gradasi warna hijau ekonomis
            height=550
        )
        
        # 5. Kustomisasi Desain Layout & Tooltip (Hover)
        fig.update_layout(
            plot_bgcolor='rgb(248, 249, 250)',
            paper_bgcolor='white',
            yaxis=dict(categoryorder='total ascending'), # Skor tertinggi di posisi paling atas
            coloraxis_showscale=False
        )
        
        fig.update_traces(
            texttemplate='%{x:.2f}', # Menampilkan 2 angka di belakang koma pada ujung batang grafik
            textposition='outside',
            cliponaxis=False,
            marker=dict(line=dict(width=1, color='White')),
            hovertemplate="<b>%{y}</b><br><br>" +
                          "Skor ROI: %{x:.2f}<br>" +
                          "Harga Pasar: €%{customdata[0]:.2f}M<br>" +
                          "Total Gol: %{customdata[1]}<br>" +
                          "Total Asis: %{customdata[2]}<extra></extra>",
            customdata=top_roi[['market_value_m_eur', 'goals', 'assists']]
        )
        
        # 6. Menyimpan Hasil ke Folder Notebooks
        os.makedirs("notebooks", exist_ok=True)
        output_path = os.path.join("notebooks", "underpriced_overachievers.html")
        fig.write_html(output_path)
        print(f"🎉 [SUKSES] Visualisasi ROI Score berhasil disimpan di: {output_path}")
        
    except Exception as e:
        print(f"❌ Gagal memproses visualisasi ROI Score: {e}")

if __name__ == "__main__":
    analyze_and_visualize_roi()