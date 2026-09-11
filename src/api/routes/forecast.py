from fastapi import APIRouter, Depends
from typing import Optional
import json
import redis
import numpy as np
from datetime import datetime, timedelta, timezone

from src.api.schemas import ForecastRequest, ForecastPoint, ForecastResponse, SimulationRequest

router = APIRouter()

import os

_redis_client = None
try:
    redis_url = os.getenv('REDIS_URL')
    if redis_url:
        _r = redis.Redis.from_url(redis_url, decode_responses=True, socket_timeout=3.0)
    else:
        _r = redis.Redis(
            host='localhost', port=6379, db=0,
            decode_responses=True,
            socket_timeout=0.3,
            socket_connect_timeout=0.3,
            retry_on_timeout=False,
        )
    _r.ping()
    _redis_client = _r
except Exception:
    _redis_client = None

def get_redis():
    return _redis_client

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


@router.get("/latest", response_model=ForecastResponse)
def get_latest_forecast(
    bidding_zone: str = "DE_LU",
    horizon_hours: int = 48,
    r: Optional[redis.Redis] = Depends(get_redis)
):
    cache_key = f"forecast:latest:{bidding_zone}:{horizon_hours}"
    
    # Check cache
    if r is not None:
        cached = r.get(cache_key)
        if cached:
            try:
                # Return parsed JSON -> dict -> Pydantic validates it
                return json.loads(cached)
            except Exception:
                pass
                
    # Cache miss or no Redis -> Run inference
    response = mock_inference(bidding_zone, horizon_hours)
    
    # Store in cache
    if r is not None:
        try:
            r.setex(cache_key, 3600, response.model_dump_json())
        except Exception:
            pass
            
    return response


@router.post("/simulate", response_model=ForecastResponse)
def simulate_forecast(req: SimulationRequest):
    # Simulations are typically not cached to allow dynamic exploration
    response = mock_inference(
        bidding_zone=req.bidding_zone,
        horizon=req.horizon_hours,
        wind_delta=req.wind_speed_delta,
        solar_delta=req.solar_radiation_delta
    )
    return response
