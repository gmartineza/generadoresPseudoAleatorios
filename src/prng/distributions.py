from typing import Dict, List, Union, Tuple
import math
from scipy.stats import binom, poisson

class Distribution:
    """Base class for probability distributions."""
    
    def __init__(self, params: Dict[str, Union[int, float, Dict[str, float]]]):
        self.params = params
    
    def generate(self, random_numbers: List[float]) -> List[Union[int, str]]:
        """Generate values according to the distribution using random numbers."""
        raise NotImplementedError("Subclasses must implement generate()")
    
    def get_theoretical_probabilities(self) -> Dict[Union[int, str], float]:
        """Get theoretical probabilities for each possible value."""
        raise NotImplementedError("Subclasses must implement get_theoretical_probabilities()")

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
    
    def get_theoretical_probabilities(self) -> Dict[str, float]:
        """Get theoretical probabilities from the table."""
        return dict(zip(self.values, self.probabilities))

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
    
    def get_theoretical_probabilities(self) -> Dict[int, float]:
        """Get theoretical probabilities for each possible value."""
        return {k: binom.pmf(k, self.n, self.p) for k in range(self.n + 1)}

class PoissonDistribution(Distribution):
    """Handles Poisson distribution."""
    
    def __init__(self, params: Dict[str, float]):
        super().__init__(params)
        self.lambda_ = params["lambda"]  # average number of events
        
        if self.lambda_ <= 0:
            raise ValueError("Lambda must be positive")
    
    def generate(self, random_numbers: List[float]) -> List[int]:
        """Generate values using the Poisson distribution."""
        result = []
        for r in random_numbers:
            # Use inverse CDF method
            x = 0
            cdf = 0
            while True:  # Poisson is unbounded, but we'll stop at a reasonable point
                cdf += poisson.pmf(x, self.lambda_)
                if r <= cdf:
                    result.append(x)
                    break
                x += 1
                if x > 3 * self.lambda_:  # Stop if we're far from the mean
                    result.append(x)
                    break
        return result
    
    def get_theoretical_probabilities(self) -> Dict[int, float]:
        """Get theoretical probabilities for each possible value."""
        # Calculate probabilities up to 3 standard deviations from mean
        max_k = int(self.lambda_ + 3 * math.sqrt(self.lambda_))
        return {k: poisson.pmf(k, self.lambda_) for k in range(max_k + 1)}

def create_distribution(params: Dict) -> Distribution:
    """Factory function to create appropriate distribution object."""
    tipo = params["tipo"]
    if tipo == "tabla":
        return TableDistribution(params)
    elif tipo == "binomial":
        return BinomialDistribution(params)
    elif tipo == "poisson":
        return PoissonDistribution(params)
    else:
        raise ValueError(f"Unknown distribution type: {tipo}") 