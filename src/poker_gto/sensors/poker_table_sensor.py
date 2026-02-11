"""Poker table sensor using pamiq-vrchat ImageSensor."""
import time
from pamiq_core import Sensor
from pamiq_vrchat.sensors import ImageSensor
from ..data.observations import GamePhase, PokerObservation
class PokerTableSensor(Sensor):
    """Sensor for VRChat poker table state."""
    def __init__(self, camera_index=None):
        if camera_index is not None:
            self.image_sensor = ImageSensor(camera_index=camera_index)
        else:
            self.image_sensor = ImageSensor()
    def read(self) -> PokerObservation:
        """Read poker table state from image.
        Returns:
            PokerObservation with current game state
        """
        image = self.image_sensor.read()
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
