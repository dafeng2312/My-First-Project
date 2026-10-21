"""DataForge CLI - Enterprise Financial Data ETL Pipeline Engine.

This module acts as the orchestration layer and main entry point for the Linux CLI.
It leverages functional decoupling to pipeline live cryptocurrency metrics from public APIs, 
apply business logic schemas, and persist structured objects via an Excel Spreadsheet.
"""

import sys
import argparse
from typing import Final
# 1. IMPORTAMOS PANDAS PARA GESTIONAR EL EXCEL
import pandas as pd

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
    
    # [NOTAS] Dejamos inicializar la DB por seguridad si otros módulos dependen de ella,
    # pero el guardado real ahora irá al archivo Excel.
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

        # =========================================================================
        # NUEVA FASE 3: Guardar directamente a un archivo de Excel (.xlsx)
        # =========================================================================
                # =========================================================================
        # NUEVA FASE 3: Guardar directamente a un archivo de Excel (.xlsx)
        # =========================================================================
        if debug:
            print(f"{DEBUG_MARK} Stage 3: Intercepting records and generating Excel spreadsheet...")
        
        # 2. CONVERTIMOS LOS REGISTROS LIMPIOS EN UN DATAFRAME DE PANDAS
        df = pd.DataFrame(clean_records)
        
        # --- SOLUCIÓN AL ERROR DE ZONA HORARIA ---
        # Recorremos cada columna buscando tipos de datos de fecha (datetime)
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                if debug:
                    print(f"{DEBUG_MARK} Stripping timezone from column: {col}")
                # Removemos la zona horaria convirtiéndola a "local/unaware"
                df[col] = df[col].dt.tz_localize(None)
        # -----------------------------------------
        
        # 3. EXPORTAMOS A EXCEL
        output_excel_path = "crypto_market_data.xlsx"
        df.to_excel(output_excel_path, index=False)
        
        if debug:
            print(f"{DEBUG_MARK} Excel document created successfully at: {output_excel_path}")
        
        # Copia de respaldo en la .db (opcional)
        saver.save_records(clean_records)
        # =========================================================================

        print(f"{SUCCESS_MARK} ETL execution completed seamlessly. Data exported to Excel.")
        
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
