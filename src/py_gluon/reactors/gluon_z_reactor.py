from .gluon_reactor import GluonReactor
from .types import BasecoinsPerNeutrons, Tokeons
from .gluon_reactor import *

class GluonZReactor(GluonReactor):
    
    def __init__(self, parameters: GluonZReactorParameters, state: GluonZReactorState):
        self._parameters = parameters
        self._state = state
        assert(state.neutron_circulating_supply > 0)
        assert(state.proton_circulating_supply > 0)
        assert(state.reserves > 0)
        assert(state.prev_reaction_time == 0)
        assert(state.prev_volume_delta == 0)
    
    @property
    def parameters(self) -> GluonZReactorParameters:
        return self._parameters
    
    @property
    def state(self) -> GluonZReactorState:
        return self._state
    
    def neutron_ratio(self, neutron_target_price: float) -> float:
        return (neutron_target_price * self._state.neutron_circulating_supply) / self._state.reserves
    
    def normalized_neutron_ratio(self, neutron_target_price: BasecoinsPerNeutrons) -> float:
        
        q = self.neutron_ratio(neutron_target_price)
        q_star = self._parameters.critical_neutron_ratio
        
        return min(q, q / (1 + (q - q_star)))
    
    def neutron_price(self, neutron_target_price: BasecoinsPerNeutrons) -> BasecoinsPerNeutrons:
        return self.normalized_neutron_ratio(neutron_target_price) * (self._state.reserves / self._state.neutron_circulating_supply)
    
    def proton_price(self, neutron_target_price: BasecoinsPerNeutrons) -> BasecoinsPerProtons:
        return (1 - self.normalized_neutron_ratio(neutron_target_price)) * (self._state.reserves / self._state.proton_circulating_supply)
    
    def fission(self, basecoins: Basecoin) -> Tokeons:
        fee = self._parameters.fission_fee
        sn = self._state.neutron_circulating_supply
        sp = self._state.proton_circulating_supply
        r = self._state.reserves

        neutrons = (1 - fee) * basecoins * (sn / r)
        protons = (1 - fee) * basecoins * (sp / r)
        
        return Tokeons(neutrons, protons)
    
    def fusion(self, tokeons: Tokeons) -> Basecoin:
        fee = self._parameters.fusion_fee
        sn = self._state.neutron_circulating_supply
        sp = self._state.proton_circulating_supply
        r = self._state.reserves
        
        m_n = tokeons.neutrons * (r / sn)
        m_p = tokeons.protons * (r / sp)
        assert(m_n == m_p)
        
        return (1 - fee) * m_n 
   
    def volume_delta(self, volume: Basecoin, reaction_time: float) -> Basecoin:
        return (self._state.prev_volume_delta * (self._parameters.volume_decay_factor ** (reaction_time - self._state.prev_reaction_time))) + volume
    
    def beta_decay_plus_fee(self, reaction_time: float, volume: Basecoin) -> float:
        v = self.volume_delta(volume, reaction_time)
        return min(1, self._parameters.beta_decay_fee_intercept + self._parameters.beta_decay_fee_slope*(max(v, 0) / self._state.reserves))
        
    def beta_decay_minus_fee(self, reaction_time: float, volume: Basecoin) -> float:
        v = self.volume_delta(volume, reaction_time)
        return min(1, self._parameters.beta_decay_fee_intercept + self._parameters.beta_decay_fee_slope*(max(-1*v, 0) / self._state.reserves))
    
    def beta_decay_plus(self, neutron_target_price: BasecoinsPerNeutrons, reaction_time: BasecoinsPerNeutrons, protons: Proton) -> Neutron:
        v = self.proton_volume(neutron_target_price, protons)
        fee = self.beta_decay_plus_fee(reaction_time, v)
        pn = self.neutron_price(neutron_target_price)
        pp = self.proton_price(neutron_target_price)
                
        return (1 - fee) * protons * (pp / pn)

    def beta_decay_minus(self, neutron_target_price: BasecoinsPerNeutrons, reaction_time: BasecoinsPerNeutrons, neutrons: Neutron) -> Proton:
        v = self.neutron_volume(neutron_target_price, neutrons)
        fee = self.beta_decay_minus_fee(reaction_time, v)
        pn = self.neutron_price(neutron_target_price)
        pp = self.proton_price(neutron_target_price)
        
        return (1 - fee) * neutrons * (pn / pp)
    
    def execute(self, reaction: GluonReaction, balance: GluonUserState, neutron_target_price: BasecoinsPerNeutrons, reaction_time: float) -> Tuple[GluonUserState, GluonZReactorState]:
        
       match reaction:
           
           case GluonReaction.FISSION:
               
               tokeons = self.fission(balance.basecoins)
               
               self._state.reserves += balance.basecoins
               self._state.neutron_circulating_supply += tokeons.neutrons
               self._state.proton_circulating_supply += tokeons.protons
               
               return (GluonUserState(0, tokeons.neutrons, tokeons.protons), self.state) 
                             
           case GluonReaction.FUSION:
               
               basecoins = self.fusion(Tokeons(balance.neutrons, balance.neutrons))
               
               self._state.reserves -= basecoins
               self._state.neutron_circulating_supply -= balance.neutrons
               self._state.proton_circulating_supply -= balance.protons
               
               return (GluonUserState(basecoins, 0, 0), self.state)
               
           case GluonReaction.BETA_DECAY_PLUS:
                
               neutrons = self.beta_decay_plus(neutron_target_price, reaction_time, balance.protons)
               
               self._state.neutron_circulating_supply += neutrons
               self._state.proton_circulating_supply -= balance.protons
               
               pv = self.proton_volume(neutron_target_price, balance.protons)
               self._state.prev_volume_delta = self.volume_delta(pv, reaction_time)
               self._state.prev_reaction_time = reaction_time
               
               return (GluonUserState(0, neutrons, 0), self.state)            
            
           case GluonReaction.BETA_DECAY_MINUS:
               protons = self.beta_decay_minus(neutron_target_price, reaction_time, balance.neutrons)
               
               self._state.neutron_circulating_supply -= balance.neutrons
               self._state.proton_circulating_supply += protons
               
               nv = -1 * self.neutron_volume(neutron_target_price, balance.neutrons)
               self._state.prev_volume_delta = self.volume_delta(nv, reaction_time)
               self._state.prev_reaction_time = reaction_time
               
               return (GluonUserState(0, 0, protons), self.state)          