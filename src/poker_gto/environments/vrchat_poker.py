"""VRChat Poker Environment."""

import os
import time
from typing import override

import cv2
from pamiq_core import Environment

from ..config import get_video_source
from ..data.actions import ActionType, PokerAction
from ..data.observations import GamePhase, PokerObservation

try:
    from pamiq_io.mouse import InputtinoMouseOutput

    PAMIQ_IO_AVAILABLE = True
except ImportError:
    PAMIQ_IO_AVAILABLE = False
    InputtinoMouseOutput = None

try:
    from pamiq_vrchat.sensors import ImageSensor

    PAMIQ_VRCHAT_AVAILABLE = True
except ImportError:
    PAMIQ_VRCHAT_AVAILABLE = False
    ImageSensor = None


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
        if PAMIQ_IO_AVAILABLE:
            try:
                self.actuator = InputtinoMouseOutput(fps=100)
                print("InputtinoMouseOutput initialized successfully")
            except RuntimeError as e:
                print(f"Warning: Failed to initialize InputtinoMouseOutput: {e}")
                print("Running in mock actuator mode")
                self.actuator = None
        else:
            print("Warning: pamiq-io not available, using mock actuator")
            self.actuator = None

    @override
    def observe(self) -> PokerObservation:
        """Get current state from VRChat."""
        hole_cards = None
        pot_size = 100.0
        effective_stack = 1000.0
        if self.image_sensor:
            image = self.image_sensor.read()
            if image is not None and self.debug_mode:
                os.makedirs("states/debug", exist_ok=True)
                cv2.imwrite(
                    f"states/debug/frame_{int(time.time())}.png",
                    cv2.cvtColor(image, cv2.COLOR_RGB2BGR),
                )
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
        if self.actuator:
            print(f"[ACTUATOR] Action: {action.type.name}, Amount: {action.amount}")
        else:
            print(f"[MOCK] Action: {action.type.name}, Amount: {action.amount}")
