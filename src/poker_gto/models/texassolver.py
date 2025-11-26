"""TexasSolver model implementation for pamiq-core.

This module wraps the TexasSolver CLI as a pamiq-core InferenceWrappedModel.
"""

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any, override

from pamiq_core import InferenceWrappedModel

from ..data.observations import PokerObservation


class TexasSolverModel(InferenceWrappedModel[PokerObservation, dict[str, float]]):
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
        super().__init__()
        self.solver_path = solver_path
        self.iterations = iterations
        self.threads = threads

    def _generate_config(self, obs: PokerObservation, config_path: Path) -> None:
        """Generate TexasSolver configuration file."""
        # Note: This is a simplified config generation for MVP.
        # In a real scenario, we need to map ranges and board cards accurately.

        # Convert board cards list to string
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
    def infer(self, input_data: PokerObservation) -> dict[str, float]:
        """Run TexasSolver and return strategy."""

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            config_path = tmp_path / "solver_config.txt"
            _ = Path("output_result.json")  # TexasSolver dumps to CWD usually

            self._generate_config(input_data, config_path)

            subprocess.run(
                [self.solver_path, "--config", str(config_path)],
                capture_output=True,
                text=True,
                cwd=tmp_path,  # Run in temp dir to avoid clutter
                check=True,  # Raise an exception for non-zero exit codes
            )

            # Read result from the temp dir (since we changed CWD)
            result_file = tmp_path / "output_result.json"
            if result_file.exists():
                with open(result_file) as f:
                    data = json.load(f)
                    strategy = data.get("strategy", {})
                    return strategy
            else:
                raise FileNotFoundError(f"TexasSolver output file not found: {result_file}")

    @override
    def get_state_dict(self) -> dict[str, Any]:
        return {
            "solver_path": self.solver_path,
            "iterations": self.iterations,
            "threads": self.threads,
        }

    @override
    def load_state_dict(self, state_dict: dict[str, Any]) -> None:
        self.solver_path = state_dict.get("solver_path", self.solver_path)
        self.iterations = state_dict.get("iterations", self.iterations)
        self.threads = state_dict.get("threads", self.threads)
