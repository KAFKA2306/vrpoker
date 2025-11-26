"""Card detection from poker table images."""

import cv2
import numpy as np

from .ocr import OCREngine


class CardDetector:
    """Detect and recognize playing cards from images."""

    def __init__(self):
        self.ocr = OCREngine()
        self.rank_whitelist = "A23456789JQK"
        self.suit_symbols = {"♠": "s", "♥": "h", "♦": "d", "♣": "c"}

    def detect_cards(self, image: np.ndarray) -> list[tuple[str, str]]:
        """Detect cards and recognize their rank and suit.

        Args:
            image: Full poker table image

        Returns:
            List of (rank, suit) tuples, e.g. [('A', 's'), ('K', 'h')]
        """
        contours = self._find_card_contours(image)
        cards = []

        for contour in contours:
            rank, suit = self._extract_rank_suit(image, contour)
            if rank and suit:
                cards.append((rank, suit))

        return cards

    def _find_card_contours(self, image: np.ndarray) -> list[np.ndarray]:
        """Find card contours in image.

        Args:
            image: Input image

        Returns:
            List of contours representing detected cards
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        card_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if 1000 < area < 50000:
                peri = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
                if len(approx) == 4:
                    card_contours.append(contour)

        return card_contours

    def _extract_rank_suit(self, image: np.ndarray, contour: np.ndarray) -> tuple[str, str]:
        """Extract rank and suit from card contour.

        Args:
            image: Full image
            contour: Card contour

        Returns:
            Tuple of (rank, suit), e.g. ('A', 's')
        """
        x, y, w, h = cv2.boundingRect(contour)

        rank_roi = image[y : y + int(h * 0.3), x : x + int(w * 0.3)]

        rank_text = self.ocr.recognize_text(rank_roi, whitelist=self.rank_whitelist + "10")
        rank = rank_text[0] if rank_text else ""

        if rank_text.startswith("10"):
            rank = "T"

        suit_roi = image[y + int(h * 0.15) : y + int(h * 0.3), x : x + int(w * 0.3)]
        suit_text = self.ocr.recognize_text(suit_roi)

        suit = ""
        for symbol, code in self.suit_symbols.items():
            if symbol in suit_text:
                suit = code
                break

        return rank, suit
