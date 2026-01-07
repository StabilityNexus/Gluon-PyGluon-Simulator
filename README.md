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
    Basecoin,
    BasecoinPerNeutron,
    GluonReaction,
    GluonZReactorParameters,
    GluonZReactorState,
    Neutron,
    Proton,
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
    reserves=Basecoin(1000.0),
    neutron_circulating_supply=Neutron(500.0),
    proton_circulating_supply=Proton(500.0),
    prev_volume_delta=Basecoin(0.0),
    prev_reaction_time=0.0,
)

# Create reactor instance
reactor = GluonZReactor(params, state)

# Execute a fission reaction (basecoins -> neutrons + protons)
result = reactor.execute(
    GluonReaction.FISSION,
    Basecoin(100.0),
    BasecoinPerNeutron(1.0),
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

The library uses wrapper classes for type safety:

- `Basecoin` - Reserve currency amounts
- `Neutron` - Neutron token amounts
- `Proton` - Proton token amounts
- `BasecoinPerNeutron` - Price ratio (basecoin/neutron)
- `BasecoinPerProton` - Price ratio (basecoin/proton)
- `Tokeons` - A pair of neutrons and protons

## License

MIT
