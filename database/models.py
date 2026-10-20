"""Database Models Definition Module.

Establishes the declarative schema configurations for relational data persistence
using modern SQLAlchemy 2.0 structural definitions and strict type constraints.
"""

from datetime import datetime, timezone
from sqlalchemy import String, Float, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    """Abstract base class for all declarative ORM entities mapping to the database."""
    pass


class CryptoPrice(Base):
    """SQLAlchemy Model representing the structural 'crypto_prices' table.
    
    Demonstrates advanced proficiency in SQLAlchemy 2.0 Mapped architecture,
    strict column constraint enforcement, and object string representations.
    """
    __tablename__ = 'crypto_prices'

    # Primary Key utilizing automated serial increments
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Core domain attributes with descriptive limits and non-nullable bounds
    asset_name: Mapped[str] = mapped_column(String(50), nullable=False)
    current_price: Mapped[float] = mapped_column(Float, nullable=False)
    daily_volume: Mapped[float] = mapped_column(Float, nullable=False)
    market_tier: Mapped[str] = mapped_column(String(20), nullable=False)  # Valid states: 'High Volume' | 'Standard'
    
    # Audit log field utilizing timezone-aware default timestamps to prevent offset drift
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )

    def __repr__(self) -> str:
        """Returns a clean, machine-readable string representation of the record instance."""
        return (
            f"<CryptoPrice(id={self.id}, asset='{self.asset_name}', "
            f"price={self.current_price}, tier='{self.market_tier}')>"
        )
