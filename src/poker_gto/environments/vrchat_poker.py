"""VRChat Poker Environment."""

import os
import time
from typing import override

import cv2
from pamiq_core import Environment

from ..actuators import Clicker
from ..config import get_video_source
from ..data.actions import ActionType, PokerAction
from ..data.observations import GamePhase, PokerObservation
from ..vision.button_detector import ButtonDetector
from ..vision.card_detector import CardDetector
from ..vision.table_parser import TableParser

try:
    from pamiq_vrchat.sensors import ImageSensor

    PAMIQ_VRCHAT_AVAILABLE = True
except ImportError:
    PAMIQ_VRCHAT_AVAILABLE = False


class VRChatPokerEnvironment(Environment[PokerObservation, PokerAction]):
    """Environment representing the VRChat Poker world."""

    def __init__(self):
        super().__init__()
        self.button_locations: dict[ActionType, tuple[int, int]] = {}
        self.debug_mode = os.getenv("DEBUG_VISION", "0") == "1"

        if PAMIQ_VRCHAT_AVAILABLE:
            video_source = get_video_source()
            try:
                if video_source is not None:
                    print(f"Initializing ImageSensor with source: {video_source}")
                    self.image_sensor = ImageSensor(camera_index=video_source)
                else:
                    print("Initializing ImageSensor with default source (OBS Virtual Camera)")
                    self.image_sensor = ImageSensor()
            except RuntimeError as e:
                print(f"Warning: Failed to initialize ImageSensor: {e}")
                self.image_sensor = None
        else:
            self.image_sensor = None

        self.actuator = Clicker()

        if self.image_sensor:
            self.card_detector = CardDetector()
            self.button_detector = ButtonDetector()
            self.table_parser = TableParser()
        else:
            self.card_detector = None
            self.button_detector = None
            self.table_parser = None

    @override
    def observe(self) -> PokerObservation:
        """Get current state from VRChat."""
        hole_cards = None
        pot_size = 100.0
        effective_stack = 1000.0

        if self.image_sensor and self.card_detector:
            image = self.image_sensor.read()

            if image is not None:
                if self.debug_mode:
                    os.makedirs("states/debug", exist_ok=True)
                    cv2.imwrite(
                        f"states/debug/frame_{int(time.time())}.png",
                        cv2.cvtColor(image, cv2.COLOR_RGB2BGR),
                    )

                cards = self.card_detector.detect_cards(image)
                if len(cards) >= 2:
                    hole_cards = [f"{rank}{suit}" for rank, suit in cards[:2]]

                buttons = self.button_detector.detect_buttons(image)
                self.button_locations = buttons

                pot_size = self.table_parser.parse_pot(image) or 100.0
                effective_stack = self.table_parser.parse_stack(image) or 1000.0

        return PokerObservation(
            game_phase=GamePhase.PREFLOP,
            pot_size=pot_size,
            effective_stack=effective_stack,
            hole_cards=hole_cards,
            board_cards=[],
            position="IP",
            action_history=[],
            timestamp=time.time(),
        )

    @override
    def affect(self, action: PokerAction) -> None:
        """Execute action in VRChat."""
        coords = self.button_locations.get(action.type)

        if coords:
            x, y = coords
            duration = 0.1

            self.actuator.click(x, y, duration=duration)
        else:
            print(
                f"[MOCK] Action: {action.type.name}, Amount: {action.amount} (No coordinates found)"
            )
