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
├── src/<img width="1912" height="821" alt="Screenshot 2026-07-14 104846" src="https://github.com/user-attachments/assets/40d689da-1ec7-4dcb-8705-dcb6d9201579" />
<img width="1912" height="821" alt="Screenshot 2026-07-14 104846" src="https://github.com/user-attachments/assets/f9e482c3-d0d8-49a3-910e-1d5c2939f0bc" />

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

## 📊 Interactive Dashboards & Insights

*   **Feature 1:** Top 10 Underpriced Overachievers (ROI Score)
  
Identifies players yielding the highest on-field performance return relative to their current market valuation. Higher scores indicate premium efficiency.
<img width="1912" height="707" alt="Screenshot 2026-07-14 104634" src="https://github.com/user-attachments/assets/fa919228-3ac6-4064-9c55-d4966e98969a" />

*   **Feature 2:** Squad Value vs Tournament Progress
  
A macro-level view mapping total national squad values against the highest stage achieved, complete with a global squad value benchmark line (€1,080.8M).
<img width="1912" height="821" alt="Screenshot 2026-07-14 104846" src="https://github.com/user-attachments/assets/1971c0d3-0f24-4dcc-858c-2a445b83f016" />

*   **Feature 3:** Top 10 Clutch Player Index
  
Tracks critical late-game execution by mapping out the top players who scored decisive goals at or after the 80th minute.
<img width="576" height="266" alt="Screenshot 2026-07-14 105438" src="https://github.com/user-attachments/assets/07aff095-71ef-4c25-aeb6-d8439e5c982f" />
