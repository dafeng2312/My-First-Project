import pytest
from core.transformers.data_transformer import DataTransformer

def test_transformer_calculates_high_volume_tier():
    """Prueba que un activo con más de 1B de volumen sea catalogado como 'High Volume'"""
    transformer = DataTransformer()
    mock_raw_data = {
        "bitcoin": {
            "usd": 65000.0,
            "usd_24h_vol": 1500000000.0  # 1.5 Billones
        }
    }

    result = transformer.transform(mock_raw_data)

    assert len(result) == 1
    assert result[0]["asset_name"] == "bitcoin"
    assert result[0]["market_tier"] == "High Volume"

def test_transformer_skips_invalid_prices():
    """Prueba que el transformador ignore datos corruptos con precios negativos o cero"""
    transformer = DataTransformer()
    mock_corrupted_data = {
        "scam_coin": {
            "usd": -10.0,
            "usd_24h_vol": 500.0
        }
    }

    result = transformer.transform(mock_corrupted_data)
    assert len(result) == 0  # Debe saltarse el registro corrupto
