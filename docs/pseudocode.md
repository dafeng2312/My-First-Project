# DataForge CLI - System Pseudocode & Data Contract

This document outlines the logical flow of our 3 core engine components before implementation.

## 1. Provider Layer (The Fetcher)
FUNCTION fetch_crypto_data():
    INIT API_URL = "https://coingecko.com"
    TRY:
        SEND HTTP GET request to API_URL
        IF response status is 200:
            RETURN raw JSON data
        ELSE:
            RAISE NetworkError with status code
    CATCH Exception as e:
        LOG "Failed to fetch data: " + e.message
        RETURN None

## 2. Transformer Layer (The Cleaner & Calculator)
FUNCTION transform_data(raw_json):
    IF raw_json IS None or empty:
        RAISE ValidationError("No data to process")
        
    INIT processed_records = empty list
    
    FOR EACH crypto_asset (bitcoin, ethereum) in raw_json:
        INIT price = raw_json[crypto_asset]['usd']
        INIT volume = raw_json[crypto_asset]['usd_24h_vol']
        
        # Validation Check (No negative or zero prices allowed)
        IF price <= 0 OR volume <= 0:
            SKIP current asset (Data Corrupted)
            
        # Calculate market tier metric
        INIT market_tier = "Standard"
        IF volume > 1000000000: # Over 1 Billion USD
            market_tier = "High Volume"
            
        CREATE record map with:
            - asset_name: crypto_asset
            - current_price: price
            - daily_volume: volume
            - market_tier: market_tier
            - timestamp: CURRENT_SYSTEM_TIME
            
        ADD record to processed_records
        
    RETURN processed_records

## 3. Database Layer (The Saver)
FUNCTION save_records(processed_records):
    IF processed_records is empty:
        LOG "Warning: No records to save."
        RETURN
        
    TRY:
        OPEN database connection session
        FOR EACH record in processed_records:
            CHECK if an asset with the same timestamp already exists
            IF NOT exists:
                MAP record fields to SQLAlchemy Model (CryptoPrice)
                STAGE insert into database session
        COMMIT database session (Save permanently)
        LOG "Successfully saved records to database."
    CATCH DatabaseError as e:
        ROLLBACK database session (Undo changes to prevent corruption)
        LOG "Database transaction failed: " + e.message
