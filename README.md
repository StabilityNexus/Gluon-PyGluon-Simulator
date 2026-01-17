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

---

<!-- Don't delete it -->
<div name="readme-top"></div>

<!-- Organization Logo -->
<div align="center" style="display: flex; align-items: center; justify-content: center; gap: 16px;">
  <img alt="Stability Nexus" src="public/stability.svg" width="175">
  <img src="public/todo-project-logo.svg" width="175" />
</div>

&nbsp;

<!-- Organization Name -->
<div align="center">

[![Static Badge](https://img.shields.io/badge/Stability_Nexus-/TODO-228B22?style=for-the-badge&labelColor=FFC517)](https://TODO.stability.nexus/)

<!-- Correct deployed url to be added -->

</div>

<!-- Organization/Project Social Handles -->
<p align="center">
<!-- Telegram -->
<a href="https://t.me/StabilityNexus">
<img src="https://img.shields.io/badge/Telegram-black?style=flat&logo=telegram&logoColor=white&logoSize=auto&color=24A1DE" alt="Telegram Badge"/></a>
&nbsp;&nbsp;
<!-- X (formerly Twitter) -->
<a href="https://x.com/StabilityNexus">
<img src="https://img.shields.io/twitter/follow/StabilityNexus" alt="X (formerly Twitter) Badge"/></a>
&nbsp;&nbsp;
<!-- Discord -->
<a href="https://discord.gg/YzDKeEfWtS">
<img src="https://img.shields.io/discord/995968619034984528?style=flat&logo=discord&logoColor=white&logoSize=auto&label=Discord&labelColor=5865F2&color=57F287" alt="Discord Badge"/></a>
&nbsp;&nbsp;
<!-- Medium -->
<a href="https://news.stability.nexus/">
  <img src="https://img.shields.io/badge/Medium-black?style=flat&logo=medium&logoColor=black&logoSize=auto&color=white" alt="Medium Badge"></a>
&nbsp;&nbsp;
<!-- LinkedIn -->
<a href="https://linkedin.com/company/stability-nexus">
  <img src="https://img.shields.io/badge/LinkedIn-black?style=flat&logo=LinkedIn&logoColor=white&logoSize=auto&color=0A66C2" alt="LinkedIn Badge"></a>
&nbsp;&nbsp;
<!-- Youtube -->
<a href="https://www.youtube.com/@StabilityNexus">
  <img src="https://img.shields.io/youtube/channel/subscribers/UCZOG4YhFQdlGaLugr_e5BKw?style=flat&logo=youtube&logoColor=white&logoSize=auto&labelColor=FF0000&color=FF0000" alt="Youtube Badge"></a>
</p>

---

<div align="center">
<h1>TODO: Project Name</h1>
</div>

[TODO](https://TODO.stability.nexus/) is a ... TODO: Project Description.

---

## Project Maturity

TODO: In the checklist below, mark the items that have been completed and delete items that are not applicable to the current project:

* [ ] The project has a logo.
* [ ] The project has a favicon.
* [ ] The protocol:
   - [ ] has been described and formally specified in a paper.
   - [ ] has had its main properties mathematically proven.
   - [ ] has been formally verified.
* [ ] The smart contracts:
   - [ ] were thoroughly reviewed by at least two knights of The Stable Order.
   - [ ] were deployed to:
      - [ ] Ergo
      - [ ] Cardano
      - [ ] EVM Chains:
        - [ ] Ethereum Classic
        - [ ] Ethereum
        - [ ] Polygon
        - [ ] BSC
        - [ ] Base
* [ ] The mobile app:
   - [ ] has an _About_ page containing the Stability Nexus's logo and pointing to the social media accounts of the Stability Nexus.
   - [ ] is available for download as a release in this repo.
   - [ ] is available in the relevant app stores.
* [ ] The web frontend:
   - [ ] has proper title and metadata.
   - [ ] has proper open graph metadata, to ensure that it is shown well when shared in social media (Discord, Telegram, Twitter, LinkedIn).
   - [ ] has a footer, containing the Stability Nexus's logo and pointing to the social media accounts of the Stability Nexus.
   - [ ] is fully static and client-side.
   - [ ] is deployed to Github Pages via a Github Workflow.
   - [ ] is accessible through the https://TODO:PROJECT-NAME.stability.nexus domain.
* [ ] the project is listed in [https://stability.nexus/protocols](https://stability.nexus/protocols).

---

## Tech Stack

TODO:

### Frontend

TODO:

- Next.js 14+ (React)
- TypeScript
- TailwindCSS
- shadcn/ui

### Blockchain

TODO:

- Wagmi
- Solidity Smart Contracts
- Ethers.js

---

## Getting Started

### Prerequisites

TODO

- Node.js 18+
- npm/yarn/pnpm
- MetaMask or any other web3 wallet browser extension

### Installation

TODO

#### 1. Clone the Repository

```bash
git clone https://github.com/StabilityNexus/TODO.git
cd TODO
```

#### 2. Install Dependencies

Using your preferred package manager:

```bash
npm install
# or
yarn install
# or
pnpm install
```

#### 3. Run the Development Server

Start the app locally:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

#### 4. Open your Browser

Navigate to [http://localhost:3000](http://localhost:3000) to see the application.

---

## Contributing

We welcome contributions of all kinds! To contribute:

1. Fork the repository and create your feature branch (`git checkout -b feature/AmazingFeature`).
2. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
3. Run the development workflow commands to ensure code quality:
   - `npm run format:write`
   - `npm run lint:fix`
   - `npm run typecheck`
4. Push your branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request for review.

If you encounter bugs, need help, or have feature requests:

- Please open an issue in this repository providing detailed information.
- Describe the problem clearly and include any relevant logs or screenshots.

We appreciate your feedback and contributions!

© 2025 The Stable Order.
