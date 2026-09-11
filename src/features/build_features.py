import polars as pl
from datetime import datetime, timezone
from src.features.temporal_transforms import add_temporal_features

def create_features(df: pl.DataFrame, time_col: str = "timestamp", group_col: str = "bidding_zone") -> pl.DataFrame:
    """
    Creates lag and rolling window features for model training, ensuring no forward-looking data leakage.
    Assumes df is sorted by time_col within each group.
    """
    df = df.sort([group_col, time_col])
    
    # 1. Cyclical temporal features
    df = add_temporal_features(df, time_col)
    
    # Target columns for lagging and rolling stats
    feature_cols = [
        "solar_mw", "wind_onshore_mw", "wind_offshore_mw",
        "actual_load_mw", "day_ahead_price_eur",
        "temperature_2m", "wind_speed_100m", "solar_radiation_ghi"
    ]
    
    # Check which columns exist in the DataFrame
    existing_cols = [col for col in feature_cols if col in df.columns]
    
    # 2. Lags: 24h, 48h, 168h
    lags = [24, 48, 168]
    lag_exprs = []
    for lag in lags:
        for col in existing_cols:
            lag_exprs.append(
                pl.col(col).shift(lag).over(group_col).alias(f"{col}_lag_{lag}h")
            )
            
    df = df.with_columns(lag_exprs)
    
    # 3. Rolling window stats: 12h, 24h
    # Shift by 1 first to prevent current time step leakage into the rolling window
    rolling_windows = [12, 24]
    rolling_exprs = []
    for w in rolling_windows:
        for col in existing_cols:
            rolling_exprs.append(
                pl.col(col).shift(1).rolling_mean(window_size=w).over(group_col).alias(f"{col}_rolling_{w}h_mean")
            )
            rolling_exprs.append(
                pl.col(col).shift(1).rolling_std(window_size=w).over(group_col).alias(f"{col}_rolling_{w}h_std")
            )
            
    df = df.with_columns(rolling_exprs)
    
    return df

def split_data(df: pl.DataFrame, time_col: str = "timestamp"):
    """
    Enforces strict temporal splits:
    - Train: up to 2024-12-31
    - Calibration: 2025-01-01 to 2025-06-30
    - Test: 2025-07-01 onwards
    """
    train = df.filter(pl.col(time_col) < datetime(2025, 1, 1, tzinfo=timezone.utc))
    calib = df.filter(
        (pl.col(time_col) >= datetime(2025, 1, 1, tzinfo=timezone.utc)) &
        (pl.col(time_col) < datetime(2025, 7, 1, tzinfo=timezone.utc))
    )
    test = df.filter(pl.col(time_col) >= datetime(2025, 7, 1, tzinfo=timezone.utc))
    
    return train, calib, test
