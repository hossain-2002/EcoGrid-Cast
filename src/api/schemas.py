from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class ForecastRequest(BaseModel):
    bidding_zone: str = Field(..., description="Bidding zone (e.g., DE_LU)")
    horizon_hours: int = Field(default=48, ge=1, le=168, description="Forecast horizon in hours")

class ForecastPoint(BaseModel):
    timestamp: datetime
    median_price_eur: float
    lower_bound_05_eur: float
    upper_bound_95_eur: float
    renewable_generation_mw: float

class ForecastResponse(BaseModel):
    points: List[ForecastPoint]
    metadata: dict
    empirical_coverage_rate: float

class SimulationRequest(BaseModel):
    bidding_zone: str = Field(..., description="Bidding zone (e.g., DE_LU)")
    horizon_hours: int = Field(default=48, ge=1, le=168, description="Forecast horizon in hours")
    wind_speed_delta: float = Field(default=0.0, description="Delta applied to wind speed in m/s")
    solar_radiation_delta: float = Field(default=0.0, description="Delta applied to solar radiation in W/m^2")
