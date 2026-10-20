import sys
import argparse
from database.connection import init_db, get_db_session
from core.providers.crypto_provider import CryptoProvider
from core.transformers.data_transformer import DataTransformer
from core.data_saver import DataSaver

def run_pipeline(debug: bool):
    if debug:
        print("[DEBUG] Modo detallado activo. Inicializando componentes...")
    
    if debug:
        print("[DEBUG] Inicializando base de datos local SQLite (dataforge.db)...")
    init_db()

    provider = CryptoProvider()
    transformer = DataTransformer()
    session = get_db_session()
    saver = DataSaver(session)

    try:
        if debug:
            print("[DEBUG] Paso 1: Conectando con CoinGecko API...")
        raw_payload = provider.fetch_raw_data()

        if debug:
            print(f"[DEBUG] Paso 2: Transformando carga de datos raw (Tamaño de llaves: {len(raw_payload)})")
        clean_records = transformer.transform(raw_payload)

        if debug:
            print(f"[DEBUG] Paso 3: Volcando {len(clean_records)} registros validados al ORM...")
        saver.save_records(clean_records)

        print("🚀 [SUCCESS] ¡Proceso ETL ejecutado correctamente a través de la CLI!")
    except Exception as e:
        print(f"❌ [CRITICAL] Error fatal en la ejecución del pipeline: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if debug:
            print("[DEBUG] Cerrando sesión limpia de la base de datos.")
        session.close()

if __name__ == "__main__":
    # Configuración de comandos nativos de Linux con argparse
    parser = argparse.ArgumentParser(
        description="DataForge CLI - Motor ETL industrializado de datos Financieros Cripto."
    )
    
    # Añadimos la bandera opcional --debug para flujos detallados
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Muestra trazas detalladas del estado interno durante la ejecución del proceso."
    )

    args = parser.parse_args()
    run_pipeline(debug=args.debug)

