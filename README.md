# VRChat Poker GTO Agent (powered by pamiq-core)

Autonomous VRChat poker play built on the `pamiq-core` Agent–Environment loop. The agent captures the
VRChat poker table, infers GTO actions with TexasSolver, and sends decisions back via OSC or overlay.

## Quick Start

### Prerequisites
- Python 3.12+
- [`uv`](https://github.com/astral-sh/uv) (or `pip install -e .`)
- TexasSolver binary (see `TexasSolver/` or supply your own)

### Install
```bash
uv sync
# or: pip install -e .
```

### Configure
Set the solver path and optional VRChat I/O knobs before running:
```bash
export TEXASSOLVER_PATH=/absolute/path/to/TexasSolver
export VRCHAT_CAPTURE_REGION='{"top":120,"left":80,"width":1280,"height":720}'  # JSON or top=,left=...
export VRCHAT_OSC_IP=127.0.0.1
export VRCHAT_OSC_PORT=9000
```
`TEXASSOLVER_PATH` is required; capture/OSC settings fall back to sane defaults for local dev.

### Run the agent
```bash
uv run vrpoker
# or: uv run python -m poker_gto.launch
# task runner: task run
```
Loop: **observe** the table via screen capture + OCR → **think** with `TexasSolverModel` →
**act** through OSC/overlay actuators.

## Development
- Lint/format: `uv run ruff check src tests --fix` then `uv run ruff format src tests`
- Tests: `uv run pytest`
- Full check pipeline: `task check`
- Clean artifacts: `task clean`

### Project layout
- `src/poker_gto/agents/`: decision logic (`PokerAgent`)
- `src/poker_gto/environments/`: sensors (capture/OCR) and actuators (OSC/overlay)
- `src/poker_gto/models/`: `TexasSolverModel` wrapper for inference
- `src/poker_gto/data/`: shared observation/action shapes
- `src/poker_gto/launch.py`: entrypoint wiring the loop
- `tests/`: pytest suites (see `test_smoke.py` template)

## Architecture docs
- `docs/ARCHITECTURE.md` — system diagram and data flow
- `docs/PAMIQ_TEXASSOLVER_INTEGRATION.md` — how the solver is wrapped as an inference model

## Notes & tips
- External solver builds live in `TexasSolver/`; override with `TEXASSOLVER_PATH`.
- Keep lines ≤100 chars and favor typed, small functions with logging via `launch.setup_logging`.
- When adding features, cover sensor parsing, solver parsing, and agent decision branches with tests.
