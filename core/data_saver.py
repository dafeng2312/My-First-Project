from sqlalchemy.orm import Session
from database.models import CryptoPrice

class DataSaver:
    """
    Engine responsible ONLY for writing data into the repository layer.
    """
    def __init__(self, session: Session):
        self.session = session

    def save_records(self, processed_records: list[dict]) -> None:
        """
        Converts data dictionaries into Database models and commits the transaction.
        """
        if not processed_records:
            print("[INFO] No new records to save.")
            return

        try:
            for record in processed_records:
                # Map the data payload directly to our SQLAlchemy Model structure
                db_entry = CryptoPrice(
                    asset_name=record["asset_name"],
                    current_price=record["current_price"],
                    daily_volume=record["daily_volume"],
                    market_tier=record["market_tier"],
                    timestamp=record["timestamp"]
                )
                self.session.add(db_entry)

            # Permanently save changes to the .db file
            self.session.commit()
            print(f"[SUCCESS] Saved {len(processed_records)} records to the database.")
        except Exception as e:
            self.session.rollback()  # Reverse changes if an error happens to protect data
            print(f"[ERROR] Database commit failed: {e}")
            raise e
