from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes.forecast import router as forecast_router

app = FastAPI(
    title="EcoGrid-Cast API",
    description="API for accessing Day-Ahead Price Forecasts and Simulations",
    version="0.1.0"
)

# Allow CORS for all origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(forecast_router, prefix="/api/v1/forecast", tags=["forecast"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
