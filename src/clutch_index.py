import os
import sys
import pandas as pd
import plotly.express as px

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database import get_db_engine

def calculate_clutch_index():
    """Menganalisis gol di atas menit ke-80 untuk menyaring Clutch Players dan membuat visualisasi premium"""
    try:
        engine = get_db_engine()
        
        # 1. Query Data Relational
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
            
        # 2. Pembersihan Menit (Mengatasi Extra Time '90+2')
        df_events['minute_cleaned'] = df_events['minute'].astype(str).str.split('+').str[0]
        df_events['minute_cleaned'] = pd.to_numeric(df_events['minute_cleaned'], errors='coerce').fillna(0).astype(int)
        
        # Filter Menit >= 80
        df_clutch = df_events[df_events['minute_cleaned'] >= 80].copy()
        
        if df_clutch.empty:
            print("⚠️ Tidak ditemukan data gol di atas menit ke-80.")
            return
            
        # 3. Agregasi Top 10 Clutch Performer
        clutch_players = df_clutch.groupby(['player_name']).size().reset_index(name='late_goals')
        clutch_players = clutch_players.sort_values(by='late_goals', ascending=False).head(10)
        
        print("\n🏆 TOP 10 CLUTCH PLAYER INDEX BERHASIL DIPROSES.")
        
        # 4. Membuat Visualisasi Premium Horizontal Bar Chart
        print("🎨 Membuat grafik batang premium interaktif...")
        fig = px.bar(
            clutch_players,
            x='late_goals',
            y='player_name',
            orientation='h',
            color='late_goals',
            title='<b>ValuePitch 2026: Top 10 Clutch Player Index</b><br><sup>Analisis Pemain Penentu Berdasarkan Produktivitas Gol Krusial Menit Akhir (≥ 80\')</sup>',
            labels={
                'late_goals': 'Jumlah Gol Menit Akhir',
                'player_name': 'Nama Pemain'
            },
            color_continuous_scale=px.colors.sequential.YlOrRd, # Gradasi warna premium (Kuning-Oranye-Merah)
            height=600
        )
        
        # 5. Kustomisasi Desain Layout Makro & Kebersihan Grid
        fig.update_layout(
            plot_bgcolor='rgb(248, 249, 250)', # Background abu-abu tipis premium
            paper_bgcolor='white',
            title_font=dict(size=18, family="Arial", color="rgb(33, 37, 41)"),
            xaxis=dict(
                tickmode='linear',
                dtick=1,
                gridcolor='white',
                showline=True,
                linewidth=1,
                linecolor='lightgray'
            ),
            yaxis=dict(
                categoryorder='total ascending',
                gridcolor='white',
                showline=True,
                linewidth=1,
                linecolor='lightgray',
                title=None # Menghapus teks judul sumbu Y vertikal agar lebih rapi
            ),
            coloraxis_showscale=False, # Menyembunyikan side bar skala warna agar fokus pada grafik
            margin=dict(l=160, r=40, t=90, b=60) # Memberi ruang aman di sisi kiri agar nama panjang tidak terpotong
        )
        
        # 6. Menyempurnakan Ujung Batang dan Desain Hover Box
        fig.update_traces(
            texttemplate='<b>%{x} Gol</b>', # Menebalkan label teks di ujung grafik batang
            textposition='outside', 
            cliponaxis=False,
            marker=dict(
                line=dict(width=1.5, color='White'), # Garis tepi putih tegas di sekeliling bar
                opacity=0.9
            ),
            hovertemplate="<b>%{y}</b><br><br>" +
                          "⚽ Gol Menit Akhir: %{x}<br>" +
                          "🎯 Kategori: High-Critical Clutch Performer<extra></extra>"
        )
        
        # 7. Menyimpan ke Folder Notebooks
        os.makedirs("notebooks", exist_ok=True)
        output_path = os.path.join("notebooks", "clutch_player_index.html")
        fig.write_html(output_path)
        
        print(f"🎉 [SUKSES] Visualisasi premium baru disimpan di: {output_path}")
        
    except Exception as e:
        print(f"❌ Gagal memproses visualisasi: {e}")

if __name__ == "__main__":
    calculate_clutch_index()