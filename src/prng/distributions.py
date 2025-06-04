from typing import Dict, List, Union, Tuple
import math
from scipy.stats import binom, poisson, expon, norm

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

class ExponentialDistribution(Distribution):
    """Handles exponential distribution."""
    
    def __init__(self, params: Dict[str, float]):
        super().__init__(params)
        self.lambda_ = params["lambda"]  # rate parameter
        
        if self.lambda_ <= 0:
            raise ValueError("Lambda must be positive")
        
        # Optional discretization parameters
        self.discrete_step = params.get("discrete_step")
        self.discrete_min = params.get("discrete_min")
        self.discrete_max = params.get("discrete_max")
    
    def generate(self, random_numbers: List[float]) -> List[float]:
        """Generate values using the exponential distribution."""
        result = []
        for r in random_numbers:
            # Use inverse CDF method: x = -ln(1-r)/lambda
            x = -math.log(1 - r) / self.lambda_
            
            # Apply discretization if parameters are provided
            if self.discrete_step is not None:
                # Round to nearest step
                x = round(x / self.discrete_step) * self.discrete_step
                
                # Apply min/max bounds if provided
                if self.discrete_min is not None:
                    x = max(x, self.discrete_min)
                if self.discrete_max is not None:
                    x = min(x, self.discrete_max)
            
            result.append(x)
        return result
    
    def get_theoretical_probabilities(self) -> Dict[float, float]:
        """Get theoretical probabilities for a range of values."""
        if self.discrete_step is not None:
            # For discrete case, calculate probabilities for each discrete value
            min_x = self.discrete_min if self.discrete_min is not None else 0
            max_x = self.discrete_max if self.discrete_max is not None else 3 / self.lambda_
            values = [min_x + i * self.discrete_step for i in range(int((max_x - min_x) / self.discrete_step) + 1)]
            return {x: expon.pdf(x, scale=1/self.lambda_) for x in values}
        else:
            # For continuous case, use the original implementation
            max_x = 3 / self.lambda_  # 3 standard deviations
            step = max_x / 100  # Divide into 100 intervals
            return {x: expon.pdf(x, scale=1/self.lambda_) for x in [i * step for i in range(101)]}

class NormalDistribution(Distribution):
    """Handles normal (Gaussian) distribution."""
    
    def __init__(self, params: Dict[str, float]):
        super().__init__(params)
        self.mu = params["mu"]  # mean
        self.sigma = params["sigma"]  # standard deviation
        
        if self.sigma <= 0:
            raise ValueError("Sigma must be positive")
        
        # Optional class discretization parameters
        self.num_classes = params.get("num_classes")
        self.class_min = params.get("class_min")
        self.class_max = params.get("class_max")
    
    def generate(self, random_numbers: List[float]) -> List[float]:
        """Generate values using the normal distribution."""
        result = []
        for i in range(0, len(random_numbers), 2):
            if i + 1 >= len(random_numbers):
                break
            # Box-Muller transform
            u1 = random_numbers[i]
            u2 = random_numbers[i + 1]
            z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
            z1 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
            
            # Transform to desired mean and standard deviation
            x0 = z0 * self.sigma + self.mu
            x1 = z1 * self.sigma + self.mu
            
            # Apply class discretization if specified
            if self.num_classes is not None:
                min_val = self.class_min if self.class_min is not None else -3 * self.sigma
                max_val = self.class_max if self.class_max is not None else 3 * self.sigma
                class_width = (max_val - min_val) / self.num_classes
                
                # Assign to class midpoint
                x0 = min_val + (int((x0 - min_val) / class_width) + 0.5) * class_width
                x1 = min_val + (int((x1 - min_val) / class_width) + 0.5) * class_width
                
                # Ensure values are within bounds
                x0 = max(min(x0, max_val), min_val)
                x1 = max(min(x1, max_val), min_val)
            
            result.append(x0)
            result.append(x1)
        return result
    
    def get_theoretical_probabilities(self) -> Dict[float, float]:
        """Get theoretical probabilities for a range of values."""
        if self.num_classes is not None:
            # For discrete classes, calculate probabilities for each class
            min_val = self.class_min if self.class_min is not None else -3 * self.sigma
            max_val = self.class_max if self.class_max is not None else 3 * self.sigma
            class_width = (max_val - min_val) / self.num_classes
            
            # Calculate class midpoints and their probabilities
            class_midpoints = [min_val + (i + 0.5) * class_width for i in range(self.num_classes)]
            return {x: norm.pdf(x, self.mu, self.sigma) for x in class_midpoints}
        else:
            # For continuous case, use the original implementation
            min_x = self.mu - 3 * self.sigma
            max_x = self.mu + 3 * self.sigma
            step = (max_x - min_x) / 100  # Divide into 100 intervals
            return {x: norm.pdf(x, self.mu, self.sigma) for x in [min_x + i * step for i in range(101)]}

def create_distribution(params: Dict) -> Distribution:
    """Factory function to create appropriate distribution object."""
    tipo = params["tipo"]
    if tipo == "tabla":
        return TableDistribution(params)
    elif tipo == "binomial":
        return BinomialDistribution(params)
    elif tipo == "poisson":
        return PoissonDistribution(params)
    elif tipo == "exponencial":
        return ExponentialDistribution(params)
    elif tipo == "normal":
        return NormalDistribution(params)
    else:
        raise ValueError(f"Unknown distribution type: {tipo}") 