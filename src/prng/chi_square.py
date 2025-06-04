from math import sqrt
from scipy.stats import chi2
from typing import Dict, List, Union, Tuple
from collections import Counter

def chi_square_test_uniform(normalized_sequence: List[float], k: int = 10) -> Tuple[float, float, int]:
    """
    Perform Chi-Square test on normalized sequence.
    
    Args:
        normalized_sequence (list): List of normalized random numbers
        k (int): Number of intervals (default 10)
    
    Returns:
        tuple: (chi_square_value, p_value, degrees_of_freedom)
    """
    n = len(normalized_sequence)
    expected_frequency = n / k
    observed_frequencies = [0] * k
    
    # Count frequencies in each interval
    for num in normalized_sequence:
        interval = int(num * k)
        if interval == k:  # Handle edge case
            interval = k - 1
        observed_frequencies[interval] += 1
    
    # Calculate chi-square value
    chi_square = sum((obs - expected_frequency) ** 2 / expected_frequency 
                    for obs in observed_frequencies)
    
    # Calculate p-value
    degrees_of_freedom = k - 1
    p_value = 1 - chi2.cdf(chi_square, degrees_of_freedom)
    
    return chi_square, p_value, degrees_of_freedom

def chi_square_test_distribution(observed_values: List[Union[int, str]], 
                               theoretical_probs: Dict[Union[int, str], float]) -> Tuple[float, float, int]:
    """
    Perform Chi-Square test comparing observed values against theoretical distribution.
    
    Args:
        observed_values (list): List of observed values
        theoretical_probs (dict): Dictionary mapping values to their theoretical probabilities
    
    Returns:
        tuple: (chi_square_value, p_value, degrees_of_freedom)
    """
    n = len(observed_values)
    
    # Count observed frequencies
    observed_freqs = Counter(observed_values)
    
    # Calculate expected frequencies
    expected_freqs = {value: prob * n for value, prob in theoretical_probs.items()}
    
    # Combine all possible values
    all_values = set(observed_freqs.keys()) | set(expected_freqs.keys())
    
    # Calculate chi-square value
    chi_square = 0
    for value in all_values:
        obs = observed_freqs.get(value, 0)
        exp = expected_freqs.get(value, 0)
        
        # Skip if expected frequency is too small (less than 5)
        if exp < 5:
            continue
            
        chi_square += (obs - exp) ** 2 / exp
    
    # Calculate degrees of freedom (number of categories - 1)
    degrees_of_freedom = len(all_values) - 1
    
    # Calculate p-value
    p_value = 1 - chi2.cdf(chi_square, degrees_of_freedom)
    
    return chi_square, p_value, degrees_of_freedom

def chi_square_test(normalized_sequence: List[float], k: int = 10) -> Tuple[float, float, int]:
    """
    Alias for chi_square_test_uniform for backward compatibility.
    """
    return chi_square_test_uniform(normalized_sequence, k) 