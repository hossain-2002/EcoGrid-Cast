import pytest
import pandas as pd
from src.ingestion.entsoe_client import EntsoeClient
from src.ingestion.db_loader import EnergyMarketData
from sqlalchemy import create_engine

def test_entsoe_synthetic_fallback(monkeypatch):
    # Ensure no token is present so it falls back to synthetic data
    monkeypatch.delenv("ENTSOE_TOKEN", raising=False)
    client = EntsoeClient()
    df = client.get_data("2024-01-01", "2024-01-03")
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    
    expected_cols = [
        "timestamp", "bidding_zone", "solar_mw", "wind_onshore_mw", 
        "wind_offshore_mw", "actual_load_mw", "day_ahead_price_eur"
    ]
    for col in expected_cols:
        assert col in df.columns

def test_db_schema_definition():
    # Check table creation columns in SQLAlchemy
    columns = [c.name for c in EnergyMarketData.__table__.columns]
    expected = [
        "timestamp", "bidding_zone", "solar_mw", "wind_onshore_mw",
        "wind_offshore_mw", "actual_load_mw", "day_ahead_price_eur",
        "temperature_2m", "wind_speed_100m", "solar_radiation_ghi"
    ]
    for col in expected:
        assert col in columns
