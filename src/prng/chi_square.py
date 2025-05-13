from math import sqrt
from scipy.stats import chi2

def chi_square_test(normalized_sequence, k=10):
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