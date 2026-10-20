"""DataForge CLI - Enterprise Financial Data ETL Pipeline Engine.

This module acts as the orchestration layer and main entry point for the Linux CLI.
It leverages functional decoupling to pipeline live cryptocurrency metrics from public APIs, 
apply business logic schemas, and persist structured objects via an ORM session layer.
"""

import sys
import argparse
from typing import Final

# Core architecture subsystems imports
from database.connection import init_db, get_db_session
from core.providers.crypto_provider import CryptoProvider
from core.transformers.data_transformer import DataTransformer
from core.data_saver import DataSaver

# Terminal visual anchors using semantic emoji indicators
SUCCESS_MARK: Final[str] = "🚀 [SUCCESS]"
INFO_MARK: Final[str] = "ℹ️ [INFO]"
DEBUG_MARK: Final[str] = "⚙️ [DEBUG]"
CRITICAL_MARK: Final[str] = "❌ [CRITICAL]"


def run_pipeline(debug: bool) -> None:
    """Executes the synchronous Extract-Transform-Load (ETL) pipeline lifecycle.

    Args:
        debug: If True, activates verbose tracing across all pipeline operational stages.

    Raises:
        SystemExit: Closes execution with return code 1 if a fatal structural error occurs.
    """
    if debug:
        print(f"{DEBUG_MARK} Verbose trace mode initialized. Assembling core components...")
        print(f"{DEBUG_MARK} Provisioning local SQLite persistence architecture...")
    
    # Initialize connection structures and assert database schema presence
    init_db()

    # Instantiate decoupled boundary components applying SOLID dependencies mapping
    provider = CryptoProvider()
    transformer = DataTransformer()
    session = get_db_session()
    saver = DataSaver(session)

    try:
        # Phase 1: Data Extraction Layer (Network isolated bound)
        if debug:
            print(f"{DEBUG_MARK} Stage 1: Ingesting streaming payloads from remote CoinGecko API endpoints...")
        raw_payload = provider.fetch_raw_data()

        # Phase 2: Business Logic & Transform Layer (Pure Python execution)
        if debug:
            print(f"{DEBUG_MARK} Stage 2: Parsing payload schemas. Structural dictionary key count: {len(raw_payload)}")
        clean_records = transformer.transform(raw_payload)

        # Phase 3: Data Load Layer (ORM relational persistence)
        if debug:
            print(f"{DEBUG_MARK} Stage 3: Committing {len(clean_records)} schema-validated entities to the ORM scope...")
        saver.save_records(clean_records)

        print(f"{SUCCESS_MARK} ETL execution completed seamlessly through the Linux CLI environment.")
        
    except Exception as error:
        # Standard error emission utilizing standard error streams for diagnostic compliance
        print(
            f"{CRITICAL_MARK} Pipeline execution collapsed due to an unhandled runtime exception: {error}", 
            file=sys.stderr
        )
        sys.exit(1)
        
    finally:
        if debug:
            print(f"{DEBUG_MARK} Revoking database runtime tokens. Executing safe session termination.")
        session.close()


if __name__ == "__main__":
    # Native Linux CLI Argument Parsing layer configuration
    parser = argparse.ArgumentParser(
        description="DataForge CLI - High-throughput industrial ETL engine targeting Cryptomarket data processing."
    )
    
    # Optional operational flags declaration
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Enables fine-grained internal logs and runtime state traces during pipeline phases."
    )

    args = parser.parse_args()
    run_pipeline(debug=args.debug)
