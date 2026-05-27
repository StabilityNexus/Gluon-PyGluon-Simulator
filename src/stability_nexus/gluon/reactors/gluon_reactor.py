from abc import ABC, abstractmethod
from typing import Generic

from .types import *

class GluonReactor(ABC, Generic[R]):
    
    def __init__(self, state: GluonReactorState):
        assert state.reserves > 0
        assert state.neutron_circulating_supply > 0
        assert state.proton_circulating_supply > 0
    
    @property
    @abstractmethod
    def parameters(self) -> GluonReactorParameters:
        ...
    
    @property
    @abstractmethod
    def state(self) -> GluonReactorState:
        ...
    
    @abstractmethod
    def neutron_ratio(self, neutron_target_price: BasecoinPerNeutron) -> float:
        ...
    
    @abstractmethod
    def normalized_neutron_ratio(self, neutron_target_price: BasecoinPerNeutron) -> float:
        ...
    
    @abstractmethod
    def neutron_price(self, neutron_target_price: BasecoinPerNeutron) -> BasecoinPerNeutron:
        ...
        
    @abstractmethod
    def proton_price(self, neutron_target_price: BasecoinPerNeutron) -> BasecoinPerProton:
        ...
        
    @abstractmethod
    def fission(self, basecoins: Basecoin) -> Tokeons:
        ...
            
    @abstractmethod
    def fusion(self, tokeons: Tokeons) -> Basecoin:
        ...
        
    def neutron_volume(self, neutron_target_price: BasecoinPerNeutron, neutrons: Neutron) -> Basecoin:
        return neutrons * self.neutron_price(neutron_target_price)
    
    def proton_volume(self, neutron_target_price: BasecoinPerNeutron, protons: Proton) -> Basecoin:
        return protons * self.proton_price(neutron_target_price)
    
    @abstractmethod
    def volume_delta(self, volume: Basecoin, reaction_time: float) -> Basecoin:
        ...
    
    @abstractmethod
    def beta_decay_plus_fee(self, reaction_time: float, volume: Basecoin) -> float:
        ...
        
    @abstractmethod
    def beta_decay_minus_fee(self, reaction_time: float, volume: Basecoin) -> float:
        ...
        
    @abstractmethod
    def beta_decay_plus(self, neutron_target_price: BasecoinPerNeutron, reaction_time: float, protons: Proton) -> Neutron:
        ...
         
    @abstractmethod
    def beta_decay_minus(self, neutron_target_price: BasecoinPerNeutron, reaction_time: float, neutrons: Neutron) -> Proton:
        ...
        
    @abstractmethod
    def execute(self, reaction: GluonReaction, balance: Basecoin | Tokeons | Proton | Neutron, neutron_target_price: BasecoinPerNeutron, reaction_time: float) -> GluonExecution[R]:
        ...
