"""Gluon Reactor abstract base class."""

from abc import ABC, abstractmethod
from typing import Any


class GluonReactor(ABC):
    """Abstract base class for Gluon Reactors.

    Subclasses must implement all abstract methods.
    """
    def __init__(self) -> None:
        #TODO
        ... 
        
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the reactor."""
        #TODO
        ...
        
    @abstractmethod
    def fission(self) -> None:
        #TODO 
        ...
        
    @abstractmethod
    def fusion(self) -> None:
        #TODO
        ...
        
    @abstractmethod
    def beta_decay_plus(self) -> None:
        #TODO
        ...
         
    @abstractmethod
    def beta_decay_minus(self) -> None:
        #TODO
        ...