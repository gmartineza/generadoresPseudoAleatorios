def generate_sequence(n, x0, c, m):
    if not all(x > 0 for x in [x0, c]):
        raise ValueError("x0 and c must be positive numbers")
    if not m > max(x0, c):
        raise ValueError("m must be greater than x0 and c")
    
    sequence = [x0]  # Start with seed
    xn = x0
    
    for _ in range(n):
        xn = (xn + c) % m
        sequence.append(xn)
    
    return sequence[1:]