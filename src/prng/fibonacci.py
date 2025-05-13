def generate_sequence(n, x0, x1, m):
    if not all(x > 0 for x in [x0, x1]):
        raise ValueError("x0 and x1 must be positive numbers")
    if not m > max(x0, x1):
        raise ValueError("m must be greater than x0 and x1")
    
    sequence = [x0, x1]  # Start with both seeds
    
    for _ in range(n):
        next_num = (sequence[-1] + sequence[-2]) % m
        sequence.append(next_num)
    
    return sequence[2:]