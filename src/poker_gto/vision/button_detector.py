"""Button detection from poker table images."""

import cv2
import numpy as np

from ..data.actions import ActionType
from .ocr import OCREngine


class ButtonDetector:
    """Detect poker action buttons in images."""

    def __init__(self):
        self.ocr = OCREngine()
        self.button_keywords = {
            ActionType.FOLD: ["FOLD", "F0LD"],
            ActionType.CALL: ["CALL", "CHECK"],
            ActionType.BET: ["BET", "RAISE", "R41SE"],
        }

    def detect_buttons(self, image: np.ndarray) -> dict[ActionType, tuple[int, int]]:
        """Detect button positions from image.

        Args:
            image: Full poker table image

        Returns:
            Dictionary mapping ActionType to (x, y) coordinates
        """
        h, w = image.shape[:2]
        bottom_region = image[int(h * 0.7) :, :]

        gray = cv2.cvtColor(bottom_region, cv2.COLOR_BGR2GRAY)

        results = self.ocr.reader.readtext(gray, detail=1)

        buttons = {}
        for bbox, text, confidence in results:
            text_upper = text.upper()

            for action_type, keywords in self.button_keywords.items():
                if any(keyword in text_upper for keyword in keywords):
                    (top_left, _, bottom_right, _) = bbox
                    center_x = int((top_left[0] + bottom_right[0]) / 2)
                    center_y = int((top_left[1] + bottom_right[1]) / 2) + int(h * 0.7)
                    buttons[action_type] = (center_x, center_y)
                    break

        return buttons
