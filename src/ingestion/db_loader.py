import os
from sqlalchemy import create_engine, Column, Float, String, DateTime, DDL, event, text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class EnergyMarketData(Base):
    __tablename__ = 'energy_market_data'
    
    timestamp = Column(DateTime, primary_key=True)
    bidding_zone = Column(String, primary_key=True)
    solar_mw = Column(Float)
    wind_onshore_mw = Column(Float)
    wind_offshore_mw = Column(Float)
    actual_load_mw = Column(Float)
    day_ahead_price_eur = Column(Float)
    temperature_2m = Column(Float)
    wind_speed_100m = Column(Float)
    solar_radiation_ghi = Column(Float)

@event.listens_for(EnergyMarketData.__table__, 'after_create')
def create_hypertable(target, connection, **kw):
    # This SQL will only succeed if the TimescaleDB extension exists.
    # It creates a hypertable partitioned by the timestamp column.
    try:
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;"))
        connection.execute(text(
            "SELECT create_hypertable('energy_market_data', 'timestamp', "
            "chunk_time_interval => INTERVAL '7 days', if_not_exists => TRUE);"
        ))
    except Exception as e:
        print(f"Failed to create hypertable: {e}")

def get_engine():
    db_user = os.getenv("POSTGRES_USER", "ecogrid_user")
    db_pass = os.getenv("POSTGRES_PASSWORD", "ecogrid_password")
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB", "ecogrid_db")
    
    conn_str = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    return create_engine(conn_str)

def init_db(engine):
    Base.metadata.create_all(engine)
