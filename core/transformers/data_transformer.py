from datetime import datetime, timezone

class DataTransformer:
    """
    Engine responsible ONLY for validating and computing metrics.
    This is a pure data transformation layer, making it trivial to Unit Test.
    """
    def transform(self, raw_data: dict) -> list[dict]:
        """
        Validates inputs and injects business metrics like Market Tier.
        """
        if not raw_data:
            raise ValueError("Cannot transform empty payload.")

        processed_records = []
        current_time = datetime.now(timezone.utc)

        for asset_name, metrics in raw_data.items():
            price = metrics.get("usd", 0.0)
            volume = metrics.get("usd_24h_vol", 0.0)

            # Data integrity check (Filter out corrupted API data safely)
            if price <= 0.0:
                print(f"[WARN] Skipping {asset_name} due to invalid price data.")
                continue

            # Business Logic rule: Define market tier based on 24h volume boundary
            # 1 Billion USD as threshold
            market_tier = "High Volume" if volume > 1_000_000_000 else "Standard"

            # Map the data payload to match our database columns perfectly
            record = {
                "asset_name": asset_name,
                "current_price": float(price),
                "daily_volume": float(volume),
                "market_tier": market_tier,
                "timestamp": current_time
            }
            processed_records.append(record)

        return processed_records
