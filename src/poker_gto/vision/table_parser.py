"""Table information parser."""

import cv2
import numpy as np

from .ocr import OCREngine


class TableParser:
    """Parse pot and stack information from table images."""

    def __init__(self):
        self.ocr = OCREngine()

    def parse_pot(self, image: np.ndarray) -> float:
        """Parse pot amount from image.

        Args:
            image: Full poker table image

        Returns:
            Pot amount as float
        """
        h, w = image.shape[:2]
        pot_region = image[int(h * 0.3) : int(h * 0.4), int(w * 0.4) : int(w * 0.6)]

        pot_region_gray = cv2.cvtColor(pot_region, cv2.COLOR_BGR2GRAY)
        _, pot_region_binary = cv2.threshold(
            pot_region_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        return self.ocr.recognize_number(pot_region_binary)

    def parse_stack(self, image: np.ndarray) -> float:
        """Parse stack amount from image.

        Args:
            image: Full poker table image

        Returns:
            Stack amount as float
        """
        h, w = image.shape[:2]
        stack_region = image[int(h * 0.7) : int(h * 0.9), int(w * 0.7) :]

        stack_region_gray = cv2.cvtColor(stack_region, cv2.COLOR_BGR2GRAY)
        _, stack_region_binary = cv2.threshold(
            stack_region_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        return self.ocr.recognize_number(stack_region_binary)
