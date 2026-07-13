## ValuePitch 2026: World Cup ROI Analytics & Performance Prediction

An end-to-end data science and machine learning pipeline designed to expose market inefficiencies in football talent scouting. By leveraging cloud data engineering, custom efficiency metrics, and predictive modeling, this project identifies undervalued assets ("hidden gems") and forecasts fair market value adjustments based on real-time tournament performance.

## 🛠️ Tech Stack & Architecture

*   **Database Infrastructure:** Neon Tech (Cloud PostgreSQL), SQLAlchemy, Psycopg2
*   **Data Pipeline & Cleaning:** Python, Pandas, NumPy
*   **Interactive Visualizations:** Plotly Express, Plotly Graph Objects (HTML-rendered executive dashboards)
*   **Machine Learning:** Scikit-Learn (Linear Regression), Train-Test Split validation

```text
WORLD-CUP-ROI-ANALYTICS/
│
├── src/
│   ├── __init__.py             # Package indicator
│   ├── database.py             # Cloud Neon Tech engine initialization
│   ├── analytics.py            # ROI Score & Hidden Gem extraction
│   ├── dashboard.py            # Squad Value vs Tournament Progress plot
│   ├── clutch_index.py         # Late-game performance (Mins >= 80) metrics
│   └── regression_model.py     # Predictive machine learning model
│
├── notebooks/                  # Production HTML interactive plots
│   ├── underpriced_overachievers.html
│   ├── squad_value_vs_progress.html
│   └── clutch_player_index.html
│
├── main_migration.py           # Core cloud database ingestion script
└── .env                        # Environment variables (Ignored in git)
```
