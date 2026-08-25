"""Tests for data normalization."""
import pytest
from datetime import datetime
from data.normalizer import DataNormalizer


def test_is_missing():
    """Test missing value detection."""
    assert DataNormalizer.is_missing(None)
    assert DataNormalizer.is_missing("")
    assert DataNormalizer.is_missing("   ")
    assert DataNormalizer.is_missing("-")
    assert DataNormalizer.is_missing("N/A")
    assert DataNormalizer.is_missing("NA")
    assert not DataNormalizer.is_missing("valid value")
    assert not DataNormalizer.is_missing(0)
    assert not DataNormalizer.is_missing(False)


def test_normalize_number():
    """Test number normalization."""
    assert DataNormalizer.normalize_number("1,234,567.50") == 1234567.50
    assert DataNormalizer.normalize_number("₹1,234") == 1234.0
    assert DataNormalizer.normalize_number("$500") == 500.0
    assert DataNormalizer.normalize_number("  1000  ") == 1000.0
    assert DataNormalizer.normalize_number(42) == 42.0
    assert DataNormalizer.normalize_number("N/A") is None
    assert DataNormalizer.normalize_number("") is None


def test_normalize_percentage():
    """Test percentage normalization."""
    assert DataNormalizer.normalize_percentage("70%") == 0.70
    assert DataNormalizer.normalize_percentage("15") == 0.15
    assert DataNormalizer.normalize_percentage(0.5) == 0.5
    assert DataNormalizer.normalize_percentage(80) == 0.80
    assert DataNormalizer.normalize_percentage("N/A") is None


def test_probability_category_to_value():
    """Test probability category conversion."""
    assert DataNormalizer.probability_category_to_value("High") == 0.70
    assert DataNormalizer.probability_category_to_value("high") == 0.70
    assert DataNormalizer.probability_category_to_value("Medium") == 0.40
    assert DataNormalizer.probability_category_to_value("Low") == 0.15
    assert DataNormalizer.probability_category_to_value("Unknown") is None


def test_normalize_customer_code():
    """Test customer code normalization."""
    assert DataNormalizer.normalize_customer_code("ABC 123") == "ABC123"
    assert DataNormalizer.normalize_customer_code("  xyz-456  ") == "XYZ-456"
    assert DataNormalizer.normalize_customer_code("") is None


def test_normalize_text():
    """Test text normalization."""
    assert DataNormalizer.normalize_text("  multiple   spaces  ") == "multiple spaces"
    assert DataNormalizer.normalize_text("Normal Text") == "Normal Text"
    assert DataNormalizer.normalize_text("") is None
    assert DataNormalizer.normalize_text("N/A") is None
