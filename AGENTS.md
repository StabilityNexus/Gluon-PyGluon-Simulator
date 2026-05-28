# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

`stability-nexus` is a Python multi-protocol simulation library. The primary implementation is the Gluon protocol reactor, which models fission, fusion, and beta decay reactions on a two-token (neutron/proton) system backed by basecoin reserves.

## Commands

### Environment

This project uses [pixi](https://pixi.sh) for dependency management per project convention. There is no `pixi.lock` yet — if one is needed, run `pixi install`.

```bash
pixi install          # set up the environment
pixi shell             # activate the environment
```

### Testing

```bash
pixi run pytest                    # run all tests
pixi run pytest tests/test_gluon.py -x -v  # single file, fail fast, verbose
pixi run pytest tests/test_gluon.py::test_version -x -v  # single test
```

### Build

The project uses the `hatchling` build backend. Build artifacts are just the package wheel, installed in editable mode via pixi. To build:

```bash
pixi run python -m build
```

### Linting / formatting

No linter or formatter is configured yet. If adding one, use the project convention (pixi tasks in `[tool.pixi.tasks]` in `pyproject.toml`).

## Architecture

### Package layout

All source lives under `src/stability_nexus/` (`src` layout). `Basecoin = float` is the single global type in `src/stability_nexus/types.py`. Protocols live in subpackages (`src/stability_nexus/gluon/`).

### Reactor pattern

The Gluon module uses an **abstract base class with a `Generic[R]` type parameter** to support multiple reactor variants (currently only concrete: `GluonZReactor`).

- **`GluonReactor`** (`gluon/reactors/gluon_reactor.py`) — abstract base parametrized by `R: GluonReactorState`. Declares the full reaction interface: `fission`, `fusion`, `beta_decay_plus`, `beta_decay_minus`, neutron/proton pricing, volume delta, fees, and the `execute` dispatch method.
- **`GluonZReactor`** (`gluon/reactors/gluon_z_reactor.py`) — concrete implementation typed as `GluonReactor[GluonZReactorState]`. Adds Z-specific parameters (`volume_decay_factor`) and state (`prev_volume_delta`, `prev_reaction_time`) to implement time-decaying volume tracking for beta decay fee calculation.

Key hierarchy: `GluonReactorParameters` → `GluonZReactorParameters` (adds `volume_decay_factor`), and `GluonReactorState` → `GluonZReactorState` (adds `prev_volume_delta`, `prev_reaction_time`). New reactor variants should follow this pattern: subclass both the parameters dataclass and state dataclass, then extend `GluonReactor[YourState]`.

### Reaction dispatch

`execute()` uses Python 3.10+ `match/case` to dispatch on `GluonReaction` enum values. Each case mutates `self._state` in place and returns a `GluonExecution[GluonZReactorState]` containing the reactor output and the updated state snapshot.

### Types

Type aliases (`Basecoin`, `Neutron`, `Proton`, `BasecoinPerNeutron`, `BasecoinPerProton`) are all `float` — they serve as documentation only, not compile-time safety. `Tokeons` is a dataclass bundling `neutrons` + `protons`. These are defined in `gluon/reactors/types.py`.

## Adding a new protocol

1. Create `src/stability_nexus/<protocol>/` with `__init__.py`.
2. If the protocol has shared types beyond `Basecoin`, add them in a `types.py` within that package.
3. Follow the existing Gluon pattern if the protocol involves reactors: abstract base, concrete implementations, parameter/state dataclass hierarchy.
4. Export public symbols through `__init__.py`.
5. Add tests under `tests/test_<protocol>.py`.
