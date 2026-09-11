import os
import pandas as pd
import numpy as np

class EntsoeClient:
    def __init__(self, bidding_zone="10Y1001A1001A83F"): # Germany
        self.token = os.getenv("ENTSOE_TOKEN")
        self.bidding_zone = bidding_zone

    def get_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetches generation and price data from ENTSO-E.
        If no ENTSOE_TOKEN is provided, falls back to a synthetic data generator.
        """
        if not self.token:
            print("Warning: ENTSOE_TOKEN not found. Falling back to synthetic data generator.")
            return self._generate_synthetic_data(start_date, end_date)
        
        # In a real implementation, we would use the token to query the ENTSO-E API here.
        # e.g., using `entsoe-py` or direct requests.
        raise NotImplementedError("ENTSO-E API real implementation requires parsing logic.")
        
    def _generate_synthetic_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        # Create an hourly datetime range
        dr = pd.date_range(start=start_date, end=end_date, freq='h', tz='UTC')
        n = len(dr)
        
        # Base diurnal patterns
        hours = dr.hour.values
        
        # Solar pattern (active mostly between 6am and 6pm)
        solar_pattern = np.clip(np.sin(np.pi * (hours - 6) / 12), 0, 1)
        solar_mw = solar_pattern * 40000 + np.random.normal(0, 1000, n)
        solar_mw = np.clip(solar_mw, 0, None)
        
        # Wind pattern
        wind_onshore_mw = 15000 + np.random.normal(0, 2000, n) + np.sin(np.arange(n) / 24) * 5000
        wind_onshore_mw = np.clip(wind_onshore_mw, 0, None)
        
        wind_offshore_mw = 5000 + np.random.normal(0, 500, n) + np.cos(np.arange(n) / 24) * 1000
        wind_offshore_mw = np.clip(wind_offshore_mw, 0, None)
        
        # Load pattern (peaks during day, lower at night)
        actual_load_mw = 50000 + np.sin(np.pi * (hours - 6) / 12) * 10000 + np.random.normal(0, 1500, n)
        
        # Price model: inversely correlated with renewable generation (very simplistically)
        net_load = actual_load_mw - (solar_mw + wind_onshore_mw + wind_offshore_mw)
        day_ahead_price_eur = net_load * 0.002 + np.random.normal(0, 5, n)
        
        return pd.DataFrame({
            "timestamp": dr,
            "bidding_zone": "DE-LU",
            "solar_mw": solar_mw,
            "wind_onshore_mw": wind_onshore_mw,
            "wind_offshore_mw": wind_offshore_mw,
            "actual_load_mw": actual_load_mw,
            "day_ahead_price_eur": day_ahead_price_eur
        })
