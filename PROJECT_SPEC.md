# EcoGrid-Cast Specification
Architecture:
- Ingestion: ENTSO-E API & Open-Meteo Weather API -> TimescaleDB (PostgreSQL time-series extension)
- Feature Store: Polars (cyclical sine/cosine, 24h/48h/168h lags, rolling window statistics)
- ML Core: Quantile LightGBM (q=0.05, 0.50, 0.95) calibrated via MAPIE (Conformal Prediction, 90% coverage)
- API: FastAPI asynchronous service with Pydantic v2 schemas and Redis response caching
- Web: React + TypeScript + Vite + Tailwind CSS + Plotly.js fan chart visualizer