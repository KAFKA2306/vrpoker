"""VRChat Poker Environment."""

import time
from typing import override

from pamiq_core import Environment

from ..actuators import Clicker
from ..config import get_video_source
from ..data.actions import ActionType, PokerAction
from ..data.observations import GamePhase, PokerObservation

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

        if PAMIQ_VRCHAT_AVAILABLE:
            # Initialize ImageSensor with configured source
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

        # Initialize Clicker for actions
        self.actuator = Clicker()

    @override
    def observe(self) -> PokerObservation:
        """Get current state from VRChat."""
        if self.image_sensor:
            # Read an image from the sensor.
            image = self.image_sensor.read()

            # Find button locations from the image and cache them.
            # This is a placeholder for the actual image processing logic.
            # We assume a method `find_action_buttons` exists and returns a dict
            # like {ActionType.FOLD: (x, y), ...}.
            if image is not None:
                # TODO: Implement actual button detection
                # self.button_locations = self.image_sensor.find_action_buttons(image)
                pass

        # The rest of the observation is still a placeholder.
        # This should also be populated from image analysis.
        return PokerObservation(
            game_phase=GamePhase.PREFLOP,
            pot_size=100.0,
            effective_stack=1000.0,
            hole_cards=None,
            board_cards=[],
            position="IP",
            action_history=[],
            timestamp=time.time(),
        )

    @override
    def affect(self, action: PokerAction) -> None:
        """Execute action in VRChat."""
        # Get the screen coordinates for the action.
        coords = self.button_locations.get(action.type)

        if coords:
            x, y = coords
            # Determine duration based on action type or amount
            # For BET/RAISE, we might want a longer press if it's a slider,
            # but usually we click a specific amount button or type.
            # For now, use default duration.
            duration = 0.1

            self.actuator.click(x, y, duration=duration)
        else:
            print(
                f"[MOCK] Action: {action.type.name}, Amount: {action.amount} (No coordinates found)"
            )
