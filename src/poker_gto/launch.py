"""Main entry point for VRChat Poker GTO System."""

import logging
import os
from pathlib import Path

from pamiq_core import Interaction, LaunchConfig, launch

from .agents import PokerAgent
from .environments import VRChatPokerEnvironment
from .models import TexasSolverModel


def setup_logging() -> None:
    """Configure logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def main() -> None:
    """Launch the system."""
    setup_logging()

    # Initialize components
    agent = PokerAgent()
    environment = VRChatPokerEnvironment()

    # Initialize models
    # Allow overriding solver path via TEXASSOLVER_PATH
    solver_path = os.getenv("TEXASSOLVER_PATH")
    if not solver_path:
        # Fallback to a local TexasSolver build inside repo
        solver_path = str(Path.cwd() / "TexasSolver" / "TexasSolver")

    models = {"texassolver": TexasSolverModel(solver_path=solver_path)}

    # Launch configuration
    config = LaunchConfig(
        states_dir="./states",
        web_api_address=("localhost", 8391),  # pamiq-console support
    )

    print("Starting VRChat Poker GTO System...")
    print("Connect via pamiq-console at http://localhost:8391")

    launch(
        interaction=Interaction(agent, environment),
        models=models,
        buffers={},  # No data collection for now
        trainers={},
        config=config,
    )


if __name__ == "__main__":
    main()
