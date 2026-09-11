import polars as pl
import numpy as np

def add_temporal_features(df: pl.DataFrame, time_col: str = "timestamp") -> pl.DataFrame:
    """
    Adds cyclical sine and cosine transformations for hour of day, day of week, and day of year.
    """
    return df.with_columns([
        (np.sin(2 * np.pi * pl.col(time_col).dt.hour() / 24)).alias("sin_hour"),
        (np.cos(2 * np.pi * pl.col(time_col).dt.hour() / 24)).alias("cos_hour"),
        (np.sin(2 * np.pi * pl.col(time_col).dt.weekday() / 7)).alias("sin_day_of_week"),
        (np.cos(2 * np.pi * pl.col(time_col).dt.weekday() / 7)).alias("cos_day_of_week"),
        (np.sin(2 * np.pi * pl.col(time_col).dt.ordinal_day() / 365.25)).alias("sin_day_of_year"),
        (np.cos(2 * np.pi * pl.col(time_col).dt.ordinal_day() / 365.25)).alias("cos_day_of_year")
    ])
