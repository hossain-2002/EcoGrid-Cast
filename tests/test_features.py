import pytest
import polars as pl
from datetime import datetime
from src.features.temporal_transforms import add_temporal_features
from src.features.build_features import create_features, split_data

def test_add_temporal_features():
    df = pl.DataFrame({
        "timestamp": pl.datetime_range(datetime(2024, 1, 1), datetime(2024, 1, 2), "1h", eager=True)
    })
    res = add_temporal_features(df)
    
    assert "sin_hour" in res.columns
    assert "cos_day_of_year" in res.columns
    # Check bounds
    assert res["sin_hour"].min() >= -1.0
    assert res["sin_hour"].max() <= 1.0

def test_create_features_no_leakage():
    # Create dummy data with 1h frequency
    time_index = pl.datetime_range(datetime(2024, 1, 1), datetime(2024, 1, 15), "1h", eager=True)
    n = len(time_index)
    df = pl.DataFrame({
        "timestamp": time_index,
        "bidding_zone": ["DE-LU"] * n,
        "solar_mw": list(range(n)),
        "wind_onshore_mw": list(range(n)),
        "wind_offshore_mw": list(range(n)),
        "actual_load_mw": list(range(n)),
        "day_ahead_price_eur": list(range(n)),
        "temperature_2m": list(range(n)),
        "wind_speed_100m": list(range(n)),
        "solar_radiation_ghi": list(range(n))
    })
    
    res = create_features(df)
    
    # Verify lag is correct and relies on past data.
    # The value of solar_mw at index i is i.
    # Lag 24 of index 24 should be value at index 0, which is 0.
    assert res["solar_mw_lag_24h"][24] == 0.0
    
    # Verify rolling uses past data only. 
    # rolling 12h mean for index 12: values shifted by 1 are indices 0 to 11.
    # Mean of 0 to 11 is 5.5.
    assert res["solar_mw_rolling_12h_mean"][12] == 5.5

def test_split_data():
    df = pl.DataFrame({
        "timestamp": [
            datetime(2024, 12, 31, 23, 0, 0),
            datetime(2025, 1, 1, 0, 0, 0),
            datetime(2025, 6, 30, 23, 0, 0),
            datetime(2025, 7, 1, 0, 0, 0)
        ]
    })
    train, calib, test = split_data(df)
    
    # Train
    assert len(train) == 1
    assert train["timestamp"][0] == datetime(2024, 12, 31, 23, 0, 0)
    
    # Calib
    assert len(calib) == 2
    assert calib["timestamp"][0] == datetime(2025, 1, 1, 0, 0, 0)
    
    # Test
    assert len(test) == 1
    assert test["timestamp"][0] == datetime(2025, 7, 1, 0, 0, 0)
