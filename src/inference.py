import numpy as np
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ForecastPoint:
    timestamp: datetime
    median_price_eur: float
    lower_bound_05_eur: float
    upper_bound_95_eur: float
    renewable_generation_mw: float

@dataclass
class ForecastResponse:
    points: List[ForecastPoint]
    metadata: Dict
    empirical_coverage_rate: float

def mock_inference(bidding_zone: str, horizon: int, wind_delta: float = 0.0, solar_delta: float = 0.0) -> ForecastResponse:
    # Generate synthetic mock response
    base_time = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    points = []
    
    # Impact of weather: Higher wind/solar -> lower price.
    price_impact = -1.5 * wind_delta - 0.05 * solar_delta
    
    for i in range(horizon):
        t = base_time + timedelta(hours=i)
        
        # Base price cycles daily (higher in day, lower at night)
        hour = t.hour
        base_price = 50.0 + 20.0 * np.sin(np.pi * (hour - 6) / 12) + price_impact
        
        # Add some noise
        median = max(0.0, base_price + np.random.normal(0, 5))
        
        # Bounds
        lower = max(0.0, median - 15.0 - np.random.normal(0, 2))
        upper = median + 15.0 + np.random.normal(0, 2)
        
        # Renewables
        ren = 10000.0 + 500.0 * wind_delta + 100.0 * solar_delta
        ren = max(0.0, ren)
        
        points.append(ForecastPoint(
            timestamp=t,
            median_price_eur=round(median, 2),
            lower_bound_05_eur=round(lower, 2),
            upper_bound_95_eur=round(upper, 2),
            renewable_generation_mw=round(ren, 2)
        ))
        
    return ForecastResponse(
        points=points,
        metadata={
            "bidding_zone": bidding_zone,
            "horizon_hours": horizon,
            "model_version": "0.1.0-mock",
            "weather_deltas": {
                "wind": wind_delta,
                "solar": solar_delta
            }
        },
        empirical_coverage_rate=0.90
    )
