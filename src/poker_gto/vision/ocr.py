"""OCR engine for text recognition."""

import numpy as np


class OCREngine:
    """OCR engine using EasyOCR."""

    def __init__(self):
        import easyocr

        self.reader = easyocr.Reader(["en"], gpu=False)

    def recognize_text(self, image: np.ndarray, whitelist: str = None) -> str:
        """Recognize text from image region.

        Args:
            image: Image region as numpy array
            whitelist: Optional whitelist of allowed characters

        Returns:
            Recognized text string
        """
        results = self.reader.readtext(image, detail=0, allowlist=whitelist)
        return "".join(results) if results else ""

    def recognize_number(self, image: np.ndarray) -> float:
        """Recognize numeric value from image region.

        Args:
            image: Image region as numpy array

        Returns:
            Recognized number as float, or 0.0 if recognition fails
        """
        text = self.recognize_text(image, whitelist="0123456789.,")
        text = text.replace(",", "")
        try:
            return float(text)
        except ValueError:
            return 0.0
