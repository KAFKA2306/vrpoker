"""VRChat Poker Environment."""

import time
from typing import override

from pamiq_core import Environment

from ..data.actions import ActionType, PokerAction
from ..data.observations import GamePhase, PokerObservation

try:
    from pamiq_vrchat.actuators import OscActuator
    from pamiq_vrchat.sensors import ImageSensor

    PAMIQ_VRCHAT_AVAILABLE = True
except ImportError:
    PAMIQ_VRCHAT_AVAILABLE = False


class VRChatPokerEnvironment(Environment[PokerObservation, PokerAction]):
    """Environment representing the VRChat Poker world."""

    def __init__(self):
        super().__init__()
        if PAMIQ_VRCHAT_AVAILABLE:
            self.image_sensor = ImageSensor()
            self.osc_actuator = OscActuator()
        else:
            self.image_sensor = None
            self.osc_actuator = None

    @override
    def observe(self) -> PokerObservation:
        """Get current state from VRChat."""
        if self.image_sensor:
            _ = self.image_sensor.read()

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
        if not self.osc_actuator:
            print(f"[MOCK] Action: {action.type.name}, Amount: {action.amount}")
            return

        action_val = 0
        if action.type == ActionType.FOLD:
            action_val = 1
        elif action.type in (ActionType.CHECK, ActionType.CALL):
            action_val = 2
        elif action.type in (ActionType.BET, ActionType.RAISE, ActionType.ALLIN):
            action_val = 3

        self.osc_actuator.operate({"buttons": {action_val: True}})
