import numpy as np
import abc
from typing import List, Any
import warnings


class BaseDistribution(abc.ABC):
    """
    Abstract base class for all parameter distributions. This defines
    the methods a standard or custom parameter distribution must implement.

    Attributes
    ----------
    name: str
        Name of the parameter.
    
    Methods
    -------
    sample:
        draw n a sample from the parameter space.
    
    sample_unique:
        Draw n unique samples from the parameter space.

    """
    def __init__(self, name:str) -> None:
        self.name = name


    @abc.abstractmethod
    def sample(self, n:int=1) -> Any|List[Any]:
        """
        Draws n samples from the parameter space
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
        Draws n unique samples from the parameter space
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
    


class FloatDist(BaseDistribution):
    """
    Distribution class for parameters of type float.

    Attributes
    ----------
    name: str
        Name of the parameter.

    min_val: float
        Minimum allowed value of the parameter.

    max_val: float
        Maximum allowed value of the parameter.

    step: float (default is None)
        Minumum difference between different sample values.

    log: bool (default is False)
        If True, samples are drawn from a log-uniform distribution, if False,
        samples are drawn from a regular uniform distribution.
    
    max_attempts: int
        Maximum number of attempts at finding a sample of unique values.

        
    Methods
    -------
    sample
        Returns a requested number of samples from a uniform or log-uniform
        distribution between min_val and max_val. If step is specified, all
        non-identical sampled values are separated by at least step.

    sample_unique
        Returns unique sampled values from a uniform or log-uniform distribution
        between min_val and max_val. If step is specified, all sampled values are
        separated by at least step.
        
    """

    def __init__(self, name:str, min_val:float, max_val:float,
                    step:float|None=None, log:bool=False, max_attempts:int=1000) -> None:
        
        super().__init__(name)
        self.min_val = min_val
        self.max_val = max_val
        self.step = step
        self.log = log
        self.max_attempts = max_attempts

        # If a step is specified, find the maximum number of unique values 
        # between min_val and max_val separated by step. 
        if step:
            self.max_unique_sample_size = ((max_val - min_val)//step)*step + 1
        


    def sample(self, n:int) -> List[float]:
        """
        Samples a uniform or log-uniform distribution between self.min_val and self.max_val.
        If self.log is True, values are sampled from a log-uniform distribution and from a
        regular uniform distribution otherwise. If self.step is True, all sampled values are
        rounded to the nearest multiple of self.step greater than or equal to self.min_val. 

        Parameters
        ----------
        n: int
            number of samples to draw.

        Returns
        -------
        sample: list of floats
            The sampled parameter values. If self.log is True, values are sampled from
            a log-uniform distribution and from a regular uniform distribution otherwise.
            If self.step is True, all sampled values are rounded to the nearest multiple
            of self.step greater than or equal to self.min_val. 
        """
        if self.log:
            sample = np.random.uniform(np.log(self.min_val), np.log(self.max_val), n)
        else:
            sample = np.random.uniform(self.min_val, self.max_val, n)

        if self.step:
            sample = ((sample - self.min_val) // self.step) * self.step + self.min_val
        
        return list(sample)
    

    def sample_unique(self, n:int) -> List[float]:
        """
        Attempts to find n unique samples of the parameter by repeatedly calling self.sample 
        up to self.max_unique_sample_size. If self.step does not allow n unique values between
        self.min_val and self.max_val, the method attemps to find the maximum possible unique samples,
        self.max_unique_sample_size. If self.max_unique_sample_size have not been found,
        whatever has been found is returned with a warning message.

        Parameters
        ----------
        n: int
            Number of values to find.
        
        Returns
        -------
        sample: list[floats]
            len(sample) <= self.max_unique_sample_size.
        """
        if self.step and (self.max_unique_sample_size < n):
            n_allowed = int(self.max_unique_sample_size)
            warnings.warn(f"{n} unique samples are impossible with step={self.step}. "
                          f"{self.max_unique_sample_size} is the maximum possible number of unique samples.")
        else:
            n_allowed = n

        sample = set()
        attempts = 0

        while (len(sample) < n_allowed) and (attempts<self.max_attempts):
            s = self.sample(n_allowed)
            sample.update(s)
            attempts += 1
        
        if (attempts == self.max_attempts) and (len(sample) < n_allowed):
            warnings.warn(f"Failed to find maximum possible unique samples. "
                          f"Maximum is {n_allowed} but only found {len(sample)}")
            
        return list(sample)