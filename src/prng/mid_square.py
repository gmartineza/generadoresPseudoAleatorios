import math

def extract_middle_digits(squared, d):
    """Extract d digits from the middle of squared number, padding with zeros if needed."""
    squared_str = str(squared)
    # Pad with leading zeros if length is odd
    if (len(squared_str) % 2) != (d % 2):
        squared_str = '0' + squared_str
    # Ensure squared has at least d digits
    if len(squared_str) < d:
        raise ValueError(f"Squared number {squared} has fewer digits than required {d}")
    # Calculate middle position
    middle_start = (len(squared_str) - d) // 2
    return int(squared_str[middle_start:middle_start + d])

def generate_sequence(n, d, x1):
    """
    Generate a sequence of n random numbers using von Neumann's middle-square method.
    
    Args:
        n (int): Number of random numbers to generate
        d (int): Number of digits in each random number
        x1 (int): Initial seed number with d digits
    
    Returns:
        list: Sequence of generated random numbers
    """
    # Validate input
    if len(str(x1)) != d:
        raise ValueError(f"Initial number x1 must have exactly {d} digits")
    
    series = [x1]  # Step 2: Append x1 to series
    
    for _ in range(n):  # Step 8: Repeat n times
        squared = x1 * x1  # Step 3: Calculate square
        x2 = extract_middle_digits(squared, d)  # Step 4: Get middle digits
        series.append(x2)  # Step 5: Append to series
        x1 = x2  # Step 7: Update x1
    
    return series[2:]