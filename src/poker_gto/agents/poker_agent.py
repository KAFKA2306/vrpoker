from typing import override

from pamiq_core import Agent

from ..data.actions import ActionType, PokerAction
from ..data.observations import GamePhase, PokerObservation


class PokerAgent(Agent[PokerObservation, PokerAction]):
    def __init__(self):
        super().__init__()
        self.solver_model = None

    @override
    def on_inference_models_attached(self) -> None:
        self.solver_model = self.get_inference_model("texassolver")

    @override
    def step(self, observation: PokerObservation) -> PokerAction:
        if observation.game_phase == GamePhase.PREFLOP:
            return PokerAction(type=ActionType.FOLD, frequency=1.0)
        strategy = self.solver_model.infer(observation) if self.solver_model else {}
        action_name_str, frequency = max(strategy.items(), key=lambda x: x[1], default=("fold", 1.0))
        action_type = ActionType.FOLD
        try:
            action_type = ActionType[action_name_str.upper()]
        except KeyError:
            pass # Default to FOLD if action name is not recognized
        
        return PokerAction(type=action_type, frequency=frequency)
