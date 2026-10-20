import sys
from database.connection import init_db, get_db_session
from core.providers.crypto_provider import CryptoProvider
from core.transformers.data_transformer import DataTransformer
from core.data_saver import DataSaver

def run_pipeline():
    print("====================================")
    print("🚀 Starting DataForge CLI Pipeline...")
    print("====================================")

    # 1. Initialize the database schema (Creates dataforge.db if it doesn't exist)
    init_db()

    # 2. Instantiate our decoupled engine components (SOLID Principles)
    provider = CryptoProvider()
    transformer = DataTransformer()
    session = get_db_session()
    saver = DataSaver(session)

    try:
        # Execute Extraction (Fetcher)
        print("[1/3] Fetching data from external API...")
        raw_payload = provider.fetch_raw_data()

        # Execute Transformation (Cleaner)
        print("[2/3] Cleaning and calculating business metrics...")
        clean_records = transformer.transform(raw_payload)

        # Execute Load (Saver)
        print("[3/3] Committing records to storage layer...")
        saver.save_records(clean_records)

        print("\n✅ Execution Finished Successfully!")
    except Exception as e:
        print(f"\n❌ Pipeline failed during execution: {e}")
        sys.exit(1)
    finally:
        # Clean up by shutting down the session connection
        session.close()

if __name__ == "__main__":
    run_pipeline()
