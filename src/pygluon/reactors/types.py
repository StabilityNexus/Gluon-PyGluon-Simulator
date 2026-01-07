from dataclasses import dataclass
from typing import Sequence, Generic, TypeVar
from enum import Enum, unique

Basecoin = float
Neutron = float
Proton = float
BasecoinPerNeutron = float
BasecoinPerProton = float

@dataclass
class Tokeons:
    neutrons: Neutron
    protons: Proton

@dataclass
class GluonReactorParameters:
    critical_neutron_ratio: float
    fission_fee: float
    fusion_fee: float
    beta_decay_fee_slope: float
    beta_decay_fee_intercept: float
    
@dataclass
class GluonZReactorParameters(GluonReactorParameters):
    volume_decay_factor: float

@dataclass
class GluonReactorState:
    reserves: Basecoin
    neutron_circulating_supply: Neutron
    proton_circulating_supply: Proton
    
@dataclass
class GluonZReactorState(GluonReactorState):
    prev_volume_delta: Basecoin
    prev_reaction_time: float

@dataclass
class GluonUserState:
    basecoins: Basecoin
    neutrons: Neutron
    protons: Proton

@unique
class GluonReaction(Enum):
    FISSION = 1
    FUSION = 2
    BETA_DECAY_PLUS = 3
    BETA_DECAY_MINUS = 4

GluonReactionSequence = Sequence[GluonReaction]

R = TypeVar("R", bound=GluonReactorState)

@dataclass
class GluonExecution(Generic[R]):
    reactor_output: Tokeons | Basecoin | Neutron | Proton
    reactor_state: R