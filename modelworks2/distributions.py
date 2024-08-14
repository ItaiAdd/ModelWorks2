import numpy as np
import abc
from typing import List, Any


class BaseDistribution(abc.ABC):

    @abc.abstractmethod
    def sample(self, n:int=1) -> Any|List[Any]:
        """
        draws n samples from the parameter space
        and returns them as a list.

        Parameters
        ----------
        n: int
            The number of samples to draw.
        
        Returns
        -------
        samples:
            If n is 1 samples is a single value and if n>1 samples
            is a list of values.
        """

        raise NotImplementedError
    

    @abc.abstractmethod
    def sample_unique(self, n:int) -> List[Any]:
        """
        draws n unique samples from the parameter space
        and returns them as a list.

        Parameters
        ----------
        n: int
            The number of samples to draw.
        
        Returns
        -------
        samples: list[Any]
            List of n sampled values.
        """

        raise NotImplementedError