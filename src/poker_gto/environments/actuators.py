"""Actuators for VRChat Poker Environment."""

from __future__ import annotations

import os
from typing import override

from pamiq_core import Actuator
from pythonosc import udp_client

from ..data.actions import ActionType, PokerAction


class OSCActuator(Actuator[PokerAction]):
    """Sends actions to VRChat via OSC."""

    def __init__(self, ip: str | None = None, port: int | None = None):
        super().__init__()

        # Allow override via env so users can point to a remote VRChat instance
        ip = ip or os.getenv("VRCHAT_OSC_IP", "127.0.0.1")
        port = int(port or os.getenv("VRCHAT_OSC_PORT", 9000))

        self.client = udp_client.SimpleUDPClient(ip, port)

    @override
    def operate(self, action: PokerAction) -> None:
        """Send action to VRChat."""
        # Example mapping: /avatar/parameters/poker_action (int)
        # 1: Fold, 2: Check/Call, 3: Bet/Raise

        action_val = 0
        if action.type == ActionType.FOLD:
            action_val = 1
        elif action.type in (ActionType.CHECK, ActionType.CALL):
            action_val = 2
        elif action.type in (ActionType.BET, ActionType.RAISE, ActionType.ALLIN):
            action_val = 3

        self.client.send_message("/avatar/parameters/poker_action", action_val)

        if action.amount:
            self.client.send_message("/avatar/parameters/poker_amount", action.amount)

        # Also send to chatbox for visibility
        self.client.send_message(
            "/chatbox/input", [f"GTO Recommends: {action.type.name} ({action.frequency:.2f})", True]
        )
