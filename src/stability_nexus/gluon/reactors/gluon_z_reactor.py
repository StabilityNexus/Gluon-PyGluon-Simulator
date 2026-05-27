from .gluon_reactor import GluonReactor
from .types import (
    Basecoin,
    BasecoinPerNeutron,
    BasecoinPerProton,
    GluonExecution,
    GluonReaction,
    GluonZReactorParameters,
    GluonZReactorState,
    Neutron,
    Proton,
    Tokeons,
)

class GluonZReactor(GluonReactor[GluonZReactorState]):
    
    def __init__(self, parameters: GluonZReactorParameters, state: GluonZReactorState):
        super().__init__(state)
        self._parameters = parameters
        self._state = state
        assert state.prev_reaction_time == 0
        assert state.prev_volume_delta == 0
    
    @property
    def parameters(self) -> GluonZReactorParameters:
        return self._parameters
    
    @property
    def state(self) -> GluonZReactorState:
        return self._state
    
    def neutron_ratio(self, neutron_target_price: float) -> float:
        return (neutron_target_price * self._state.neutron_circulating_supply) / self._state.reserves
    
    def normalized_neutron_ratio(self, neutron_target_price: BasecoinPerNeutron) -> float:
        
        q = self.neutron_ratio(neutron_target_price)
        q_star = self._parameters.critical_neutron_ratio
        
        return min(q, q / (1 + (q - q_star)))
    
    def neutron_price(self, neutron_target_price: BasecoinPerNeutron) -> BasecoinPerNeutron:
        return self.normalized_neutron_ratio(neutron_target_price) * (self._state.reserves / self._state.neutron_circulating_supply)
    
    def proton_price(self, neutron_target_price: BasecoinPerNeutron) -> BasecoinPerProton:
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
        assert reaction_time > 0
        return (self._state.prev_volume_delta * (self._parameters.volume_decay_factor ** (reaction_time - self._state.prev_reaction_time))) + volume
    
    def beta_decay_plus_fee(self, reaction_time: float, volume: Basecoin) -> float:
        assert reaction_time > 0
        v = self.volume_delta(volume, reaction_time)
        return min(1, self._parameters.beta_decay_fee_intercept + self._parameters.beta_decay_fee_slope*(max(v, 0) / self._state.reserves))
        
    def beta_decay_minus_fee(self, reaction_time: float, volume: Basecoin) -> float:
        assert reaction_time > 0
        v = self.volume_delta(volume, reaction_time)
        return min(1, self._parameters.beta_decay_fee_intercept + self._parameters.beta_decay_fee_slope*(max(-1*v, 0) / self._state.reserves))
    
    def beta_decay_plus(self, neutron_target_price: BasecoinPerNeutron, reaction_time: float, protons: Proton) -> Neutron:
        assert reaction_time > 0
        v = self.proton_volume(neutron_target_price, protons)
        fee = self.beta_decay_plus_fee(reaction_time, v)
        pn = self.neutron_price(neutron_target_price)
        pp = self.proton_price(neutron_target_price)
                
        return (1 - fee) * protons * (pp / pn)

    def beta_decay_minus(self, neutron_target_price: BasecoinPerNeutron, reaction_time: float, neutrons: Neutron) -> Proton:
        assert reaction_time > 0
        v = self.neutron_volume(neutron_target_price, neutrons)
        fee = self.beta_decay_minus_fee(reaction_time, v)
        pn = self.neutron_price(neutron_target_price)
        pp = self.proton_price(neutron_target_price)
        
        return (1 - fee) * neutrons * (pn / pp)
    
    def execute(self, reaction: GluonReaction, balance: Basecoin | Tokeons | Proton | Neutron, neutron_target_price: BasecoinPerNeutron, reaction_time: float) -> GluonExecution[GluonZReactorState]:
        assert reaction_time > 0
        
        match reaction:
           
           case GluonReaction.FISSION:
               tokeons = self.fission(balance)
               self._state.reserves += balance
               self._state.neutron_circulating_supply += tokeons.neutrons
               self._state.proton_circulating_supply += tokeons.protons
               return GluonExecution(tokeons, self.state) 
                             
           case GluonReaction.FUSION:
               basecoins = self.fusion(balance)
               self._state.reserves -= basecoins
               self._state.neutron_circulating_supply -= balance.neutrons
               self._state.proton_circulating_supply -= balance.protons
               return GluonExecution(basecoins, self.state)
               
           case GluonReaction.BETA_DECAY_PLUS:
               neutrons = self.beta_decay_plus(neutron_target_price, reaction_time, balance)
               self._state.neutron_circulating_supply += neutrons
               self._state.proton_circulating_supply -= balance
               pv = self.proton_volume(neutron_target_price, balance)
               self._state.prev_volume_delta = self.volume_delta(pv, reaction_time)
               self._state.prev_reaction_time = reaction_time
               return GluonExecution(neutrons, self.state)            
            
           case GluonReaction.BETA_DECAY_MINUS:
               protons = self.beta_decay_minus(neutron_target_price, reaction_time, balance)
               self._state.neutron_circulating_supply -= balance
               self._state.proton_circulating_supply += protons
               nv = -1 * self.neutron_volume(neutron_target_price, balance)
               self._state.prev_volume_delta = self.volume_delta(nv, reaction_time)
               self._state.prev_reaction_time = reaction_time
               return GluonExecution(protons, self.state)
