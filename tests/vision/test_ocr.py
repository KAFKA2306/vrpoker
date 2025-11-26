"""Test OCR engine."""

import numpy as np
import pytest

from poker_gto.vision.ocr import OCREngine


@pytest.fixture
def ocr_engine():
    """Create OCR engine fixture."""
    return OCREngine()


def test_recognize_number(ocr_engine):
    """Test number recognition."""
    # This is a placeholder test - would need actual test images
    # For now, just verify the OCR engine can be instantiated
    assert ocr_engine is not None
    assert hasattr(ocr_engine, "recognize_number")
    assert hasattr(ocr_engine, "recognize_text")


def test_ocr_whitelist(ocr_engine):
    """Test OCR with character whitelist."""
    # Placeholder - would test with actual images
    assert hasattr(ocr_engine, "reader")
