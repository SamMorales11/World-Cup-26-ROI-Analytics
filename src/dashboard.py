import os
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database import get_db_engine

def generate_squad_value_chart():
    """Mengagregasi nilai skuad dan membuat scatter plot berstandar profesional"""
    try:
        engine = get_db_engine()
        
        # 1. Tentukan nama kolom pertandingan secara dinamis
        sample_matches = pd.read_sql("SELECT * FROM matches LIMIT 1;", engine)
        match_cols = [c.lower() for c in sample_matches.columns]
        
        if 'home_team_id' in match_cols:
            home_col, away_col = 'home_team_id', 'away_team_id'
        else:
            team_cols = [c for c in sample_matches.columns if 'team' in c.lower() and 'id' in c.lower()]
            home_col, away_col = team_cols[0], team_cols[1]
            
        # 2. Query Data Relational
        query = f"""
        SELECT 
            t.team_name,
            ts.stage_name,
            p.market_value_eur
        FROM teams t
        JOIN squads_and_players p ON t.team_id = p.team_id
        JOIN (
            SELECT {home_col} AS team_id, stage_id FROM matches
            UNION
            SELECT {away_col} AS team_id, stage_id FROM matches
        ) m ON t.team_id = m.team_id
        JOIN tournament_stages ts ON m.stage_id = ts.stage_id;
        """
        
        df_raw = pd.read_sql(query, engine)
        
        if df_raw.empty:
            print("⚠️ Data tidak ditemukan.")
            return

        # 3. Data Cleaning (String ke Numerik)
        df_raw['market_value_eur'] = df_raw['market_value_eur'].astype(str)\
            .str.replace('€', '', regex=False)\
            .str.replace(',', '', regex=False)\
            .str.replace('.', '', regex=False).str.strip()
        df_raw['market_value_eur'] = pd.to_numeric(df_raw['market_value_eur'], errors='coerce').fillna(0)

        # 4. Pengurutan Fase Turnamen (Memastikan Progres Naik ke Atas)
        stage_order = ['Group Stage', 'Round of 32', 'Round of 16', 'Quarter-Finals']
        df_raw['stage_name'] = pd.Categorical(df_raw['stage_name'], categories=stage_order, ordered=True)
        
        # Aggregasi
        df_grouped = df_raw.sort_values('stage_name').groupby('team_name').agg(
            highest_stage=('stage_name', 'last'),
            total_squad_value_eur=('market_value_eur', 'sum')
        ).reset_index()
        
        df_grouped['squad_value_m_eur'] = df_grouped['total_squad_value_eur'] / 1_000_000
        
        # Hitung rata-rata nilai skuad global sebagai garis patokan (benchmark)
        avg_squad_value = df_grouped['squad_value_m_eur'].mean()

        print("🎨 Membuat visualisasi berstandar eksekutif...")

        # 5. Membuat Scatter Plot dengan Desain Baru
        # - Menghapus argumen `text` statis untuk mencegah penumpukan teks.
        # - Menggunakan `color` berdasarkan fase untuk segmentasi visual yang kuat.
        fig = px.scatter(
            df_grouped,
            x='squad_value_m_eur',
            y='highest_stage',
            color='highest_stage',
            hover_name='team_name',
            title='<b>ValuePitch 2026: Squad Value vs Tournament Progress</b><br><sup>Analisis Korelasi Nilai Pasar Terhadap Efisiensi Performa Perempat Final</sup>',
            labels={
                'squad_value_m_eur': 'Total Squad Value (Million EUR)',
                'highest_stage': 'Highest Stage Achieved',
                'color': 'Tournament Stage'
            },
            category_orders={'highest_stage': stage_order},
            color_discrete_sequence=px.colors.sequential.Viridis,
            height=650
        )
        
        # 6. Kustomisasi Desain Marker & Tooltip
        fig.update_traces(
            marker=dict(
                size=14, 
                opacity=0.85, 
                line=dict(width=1.5, color='White') # Batasan putih tipis di sekitar lingkaran
            ),
            hovertemplate="<b>%{hovertext}</b><br><br>" +
                          "Fase Terjauh: %{y}<br>" +
                          "Nilai Skuad: €%{x:,.1f}M<extra></extra>"
        )
        
        # 7. Menambahkan Garis Rata-Rata (Benchmark Line)
        fig.add_vline(
            x=avg_squad_value, 
            line_width=2, 
            line_dash="dash", 
            line_color="rgba(219, 68, 85, 0.7)"
        )
        
        # Menambahkan label teks pada garis rata-rata
        fig.add_annotation(
            x=avg_squad_value,
            y='Quarter-Finals',
            text=f"Rata-rata Skuad: €{avg_squad_value:.1f}M",
            showarrow=False,
            xshift=10,
            font=dict(color="rgb(219, 68, 85)", size=11, family="Arial Black"),
            align="left"
        )

        # 8. Kustomisasi Layout Makro
        fig.update_layout(
            plot_bgcolor='rgb(248, 249, 250)', # Background abu-abu sangat muda yang elegan
            paper_bgcolor='white',
            title_font=dict(size=18, family="Arial"),
            xaxis=dict(
                gridcolor='white',
                zerolinecolor='white',
                showline=True,
                linewidth=1,
                linecolor='lightgray',
                ticks='outside'
            ),
            yaxis=dict(
                gridcolor='rgb(235, 235, 235)',
                showline=True,
                linewidth=1,
                linecolor='lightgray'
            ),
            legend=dict(
                title_font_family="Arial Black",
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="lightgray",
                borderwidth=1
            )
        )
        
        # Simpan ke folder notebooks
        os.makedirs("notebooks", exist_ok=True)
        output_path = os.path.join("notebooks", "squad_value_vs_progress.html")
        fig.write_html(output_path)
        print(f"🎉 [SUKSES] Dashboard profesional baru disimpan di: {output_path}")
        
    except Exception as e:
        print(f"❌ Gagal membuat visualisasi: {e}")

if __name__ == "__main__":
    generate_squad_value_chart()