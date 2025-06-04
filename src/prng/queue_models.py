"""
Queue models implementation for M/M/1, M/M/2 and M/M/1/K
"""
import math
from typing import List, Dict, Tuple

class QueueModel:
    """Base class for queue models"""
    def __init__(self, lambda_rate: float, mu_rate: float):
        """
        Initialize queue model with arrival and service rates
        
        Args:
            lambda_rate: Arrival rate (customers per time unit)
            mu_rate: Service rate (customers per time unit)
        """
        self.lambda_rate = lambda_rate
        self.mu_rate = mu_rate
        self.rho = lambda_rate / mu_rate  # Traffic intensity

    def get_metrics(self) -> Dict[str, float]:
        """Get queue metrics"""
        raise NotImplementedError

class MM1Queue(QueueModel):
    """M/M/1 Queue Model"""
    def __init__(self, lambda_rate: float, mu_rate: float):
        super().__init__(lambda_rate, mu_rate)
        if self.rho >= 1:
            raise ValueError("System is unstable: ρ >= 1")

    def get_metrics(self) -> Dict[str, float]:
        """Calculate M/M/1 queue metrics"""
        return {
            "L": self.rho / (1 - self.rho),  # Average number of customers in system
            "Lq": self.rho * self.rho / (1 - self.rho),  # Average number of customers in queue
            "W": 1 / (self.mu_rate - self.lambda_rate),  # Average time in system
            "Wq": self.rho / (self.mu_rate - self.lambda_rate),  # Average time in queue
            "P0": 1 - self.rho,  # Probability of system being empty
            "rho": self.rho  # Traffic intensity
        }

class MM2Queue(QueueModel):
    """M/M/2 Queue Model"""
    def __init__(self, lambda_rate: float, mu_rate: float):
        super().__init__(lambda_rate, mu_rate)
        if self.rho >= 2:
            raise ValueError("System is unstable: ρ >= 2")

    def get_metrics(self) -> Dict[str, float]:
        """Calculate M/M/2 queue metrics"""
        # Probability of system being empty
        P0 = 1 / (1 + self.rho + (self.rho * self.rho) / (2 * (1 - self.rho/2)))
        
        return {
            "L": self.rho + (self.rho * self.rho * self.rho) / (2 * (2 - self.rho) * (2 - self.rho)) * P0,
            "Lq": (self.rho * self.rho * self.rho) / (2 * (2 - self.rho) * (2 - self.rho)) * P0,
            "W": 1 / self.mu_rate + self.rho / (self.mu_rate * (2 - self.rho)),
            "Wq": self.rho / (self.mu_rate * (2 - self.rho)),
            "P0": P0,
            "rho": self.rho
        }

class MM1KQueue(QueueModel):
    """M/M/1/K Queue Model (Finite Queue)"""
    def __init__(self, lambda_rate: float, mu_rate: float, K: int):
        """
        Initialize M/M/1/K queue
        
        Args:
            lambda_rate: Arrival rate
            mu_rate: Service rate
            K: Maximum number of customers in system
        """
        super().__init__(lambda_rate, mu_rate)
        self.K = K

    def get_metrics(self) -> Dict[str, float]:
        """Calculate M/M/1/K queue metrics"""
        if self.rho == 1:
            P0 = 1 / (self.K + 1)
            L = self.K / 2
        else:
            P0 = (1 - self.rho) / (1 - self.rho ** (self.K + 1))
            L = (self.rho * (1 - (self.K + 1) * self.rho ** self.K + self.K * self.rho ** (self.K + 1))) / \
                ((1 - self.rho) * (1 - self.rho ** (self.K + 1)))

        # Effective arrival rate
        lambda_eff = self.lambda_rate * (1 - P0 * self.rho ** self.K)
        
        return {
            "L": L,  # Average number of customers in system
            "Lq": L - (1 - P0),  # Average number of customers in queue
            "W": L / lambda_eff,  # Average time in system
            "Wq": (L - (1 - P0)) / lambda_eff,  # Average time in queue
            "P0": P0,  # Probability of system being empty
            "PK": P0 * self.rho ** self.K,  # Probability of system being full
            "rho": self.rho,  # Traffic intensity
            "lambda_eff": lambda_eff  # Effective arrival rate
        }

def create_queue_model(model_type: str, params: Dict) -> QueueModel:
    """
    Factory function to create queue models
    
    Args:
        model_type: Type of queue model ('MM1', 'MM2', or 'MM1K')
        params: Dictionary containing model parameters
        
    Returns:
        QueueModel instance
    """
    lambda_rate = params.get('lambda_rate')
    mu_rate = params.get('mu_rate')
    
    if not lambda_rate or not mu_rate:
        raise ValueError("lambda_rate and mu_rate are required parameters")
    
    if model_type == 'MM1':
        return MM1Queue(lambda_rate, mu_rate)
    elif model_type == 'MM2':
        return MM2Queue(lambda_rate, mu_rate)
    elif model_type == 'MM1K':
        K = params.get('K')
        if not K:
            raise ValueError("K parameter is required for M/M/1/K model")
        return MM1KQueue(lambda_rate, mu_rate, K)
    else:
        raise ValueError(f"Unknown queue model type: {model_type}") 