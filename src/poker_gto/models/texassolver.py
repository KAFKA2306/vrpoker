"""TexasSolver model implementation for pamiq-core.

This module wraps the TexasSolver CLI as a pamiq-core InferenceModel.
"""

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any, override

from pamiq_core.model.interface import InferenceModel

from ..data.observations import PokerObservation


class TexasSolverModel(InferenceModel):
    """TexasSolver wrapper model.

    Takes a PokerObservation and returns a strategy dictionary (action -> frequency).
    """

    def __init__(
        self,
        solver_path: str = "./TexasSolver",
        iterations: int = 20,
        threads: int = 4,
    ):
        """Initialize the model.

        Args:
            solver_path: Path to TexasSolver executable
            iterations: Number of CFR iterations
            threads: Number of threads to use
        """
        self.solver_path = solver_path
        self.iterations = iterations
        self.threads = threads

    def _generate_config(self, obs: PokerObservation, config_path: Path) -> None:
        """Generate TexasSolver configuration file."""
        board_str = ",".join(obs.board_cards) if obs.board_cards else ""

        config_content = f"""set_pot {obs.pot_size}
set_effective_stack {obs.effective_stack}
set_board {board_str}
set_range_ip AA,KK,QQ,JJ,TT,99,88,77,AK,AQ,AJ
set_range_oop AA,KK,QQ,JJ,TT,99,88,77,AK,AQ,AJ
set_bet_sizes oop,flop,bet,50
set_bet_sizes ip,flop,bet,50
set_allin_threshold 0.67
build_tree
set_thread_num {self.threads}
set_accuracy 0.5
set_max_iteration {self.iterations}
start_solve
dump_result output_result.json
"""
        config_path.write_text(config_content)

    @override
    def infer(self, *args: Any, **kwds: Any) -> dict[str, float]:
        """Run TexasSolver and return strategy."""
        if len(args) > 0:
            input_data = args[0]
        else:
            input_data = kwds.get("input_data")

        if not isinstance(input_data, PokerObservation):
            return {"fold": 1.0}

        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                tmp_path = Path(tmp_dir)
                config_path = tmp_path / "solver_config.txt"

                self._generate_config(input_data, config_path)

                subprocess.run(
                    [self.solver_path, "--config", str(config_path)],
                    capture_output=True,
                    text=True,
                    cwd=tmp_path,
                    check=True,
                )

                result_file = tmp_path / "output_result.json"
                if result_file.exists():
                    with open(result_file) as f:
                        data = json.load(f)
                        return data.get("strategy", {"fold": 1.0})

                return {"fold": 1.0}
        except Exception:
            return {"fold": 1.0}
