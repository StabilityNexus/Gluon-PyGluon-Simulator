# pygluon

Gluon simulator library for Python. Simulates the Gluon protocol's reactor mechanics including fission, fusion, and beta decay reactions.

## Installation

```bash
pip install pygluon
```

## Quick Start

```python
from pygluon.reactors import GluonZReactor
from pygluon.reactors.types import (
    GluonReaction,
    GluonZReactorParameters,
    GluonZReactorState,
    Tokeons,
)

# Configure reactor parameters
params = GluonZReactorParameters(
    critical_neutron_ratio=0.5,
    fission_fee=0.01,
    fusion_fee=0.01,
    beta_decay_fee_slope=0.1,
    beta_decay_fee_intercept=0.005,
    volume_decay_factor=0.99,
)

# Initialize reactor state
state = GluonZReactorState(
    reserves=1000.0,
    neutron_circulating_supply=500.0,
    proton_circulating_supply=500.0,
    prev_volume_delta=0.0,
    prev_reaction_time=0.0,
)

# Create reactor instance
reactor = GluonZReactor(params, state)

# Execute a fission reaction (basecoins -> neutrons + protons)
result = reactor.execute(
    GluonReaction.FISSION,
    balance=100.0,
    neutron_target_price=1.0,
    reaction_time=1.0,
)
print(f"Received: {result.reactor_output}")
print(f"New reserves: {result.reactor_state.reserves}")
```

## Reactions

The Gluon protocol supports four reaction types:

- **FISSION**: Convert basecoins into neutrons and protons
- **FUSION**: Convert neutrons and protons back into basecoins
- **BETA_DECAY_PLUS**: Convert protons into neutrons
- **BETA_DECAY_MINUS**: Convert neutrons into protons

## Types

The library uses type aliases for documentation:

- `Basecoin` - Reserve currency amounts (`float`)
- `Neutron` - Neutron token amounts (`float`)
- `Proton` - Proton token amounts (`float`)
- `BasecoinPerNeutron` - Price ratio (`float`)
- `BasecoinPerProton` - Price ratio (`float`)
- `Tokeons` - A dataclass containing neutrons and protons

## License

MIT
