from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base

# Base class that our models inherit from to map to database tables
Base = declarative_base()

class CryptoPrice(Base):
    """
    SQLAlchemy Model representing the 'crypto_prices' table.
    Demonstrates knowledge of Data Types, Constraints, and Relational Schema.
    """
    __tablename__ = 'crypto_prices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_name = Column(String(50), nullable=False)
    current_price = Column(Float, nullable=False)
    daily_volume = Column(Float, nullable=False)
    market_tier = Column(String(20), nullable=False) # e.g., 'High Volume' or 'Standard'
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<CryptoPrice(asset='{self.asset_name}', price={self.current_price}, tier='{self.market_tier}')>"
