from typing import Dict, List, Union
import math
from scipy.stats import binom

class Distribution:
    """Base class for probability distributions."""
    
    def __init__(self, params: Dict[str, Union[int, float, Dict[str, float]]]):
        self.params = params
    
    def generate(self, random_numbers: List[float]) -> List[Union[int, str]]:
        """Generate values according to the distribution using random numbers."""
        raise NotImplementedError("Subclasses must implement generate()")

class TableDistribution(Distribution):
    """Handles probability distributions defined by a table."""
    
    def __init__(self, params: Dict[str, Dict[str, float]]):
        super().__init__(params)
        self.table = params["tabla_contingencia"]
        self.values = list(self.table.keys())
        self.probabilities = list(self.table.values())
        
        # Validate probabilities sum to 1
        if not math.isclose(sum(self.probabilities), 1.0, rel_tol=1e-5):
            raise ValueError("Probabilities must sum to 1")
    
    def generate(self, random_numbers: List[float]) -> List[str]:
        """Generate values using the probability table."""
        result = []
        for r in random_numbers:
            cumulative = 0
            for value, prob in zip(self.values, self.probabilities):
                cumulative += prob
                if r <= cumulative:
                    result.append(value)
                    break
        return result

class BinomialDistribution(Distribution):
    """Handles binomial distribution."""
    
    def __init__(self, params: Dict[str, Union[int, float]]):
        super().__init__(params)
        self.n = params["n"]  # number of trials
        self.p = params["p"]  # probability of success
        
        if not 0 <= self.p <= 1:
            raise ValueError("Probability p must be between 0 and 1")
        if self.n < 1:
            raise ValueError("Number of trials n must be positive")
    
    def generate(self, random_numbers: List[float]) -> List[int]:
        """Generate values using the binomial distribution."""
        result = []
        for r in random_numbers:
            # Use inverse CDF method
            x = 0
            cdf = 0
            while x <= self.n:
                cdf += binom.pmf(x, self.n, self.p)
                if r <= cdf:
                    result.append(x)
                    break
                x += 1
            if x > self.n:  # Handle numerical precision issues
                result.append(self.n)
        return result

def create_distribution(params: Dict) -> Distribution:
    """Factory function to create appropriate distribution object."""
    tipo = params["tipo"]
    if tipo == "tabla":
        return TableDistribution(params)
    elif tipo == "binomial":
        return BinomialDistribution(params)
    else:
        raise ValueError(f"Unknown distribution type: {tipo}") 