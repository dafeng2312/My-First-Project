import os
import sys

# Append parent directory to system path to enable clean module resolution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from core.transformers.data_transformer import DataTransformer


def test_transformer_calculates_high_volume_tier():
    """Asserts that an asset with a 24h volume exceeding 1B USD is accurately classified as 'High Volume'."""
    transformer = DataTransformer()
    mock_raw_data = {
        "bitcoin": {
            "usd": 65000.0,
            "usd_24h_vol": 1500000000.0  # 1.5 Billion USD
        }
    }

    result = transformer.transform(mock_raw_data)

    assert len(result) == 1
    assert result[0]["asset_name"] == "bitcoin"
    assert result[0]["market_tier"] == "High Volume"


def test_transformer_skips_invalid_prices():
    """Asserts that the transformer bypasses corrupted market payloads containing negative or zero prices."""
    transformer = DataTransformer()
    mock_corrupted_data = {
        "scam_coin": {
            "usd": -10.0,
            "usd_24h_vol": 500.0
        }
    }

    result = transformer.transform(mock_corrupted_data)
    assert len(result) == 0  # Enforce clean execution and structural filtering
