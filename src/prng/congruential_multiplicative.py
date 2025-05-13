import normaliser

def generate_sequence(n, x0, a, m):
    if not all(x > 0 for x in [x0, a]):
        raise ValueError("x0 and a must be positive numbers")
    if not m > max(x0, a):
        raise ValueError("m must be greater than x0 and a")
    
    sequence = [x0]  # Start with seed
    xn = x0
    
    for _ in range(n):
        xn = (a * xn) % m
        sequence.append(xn)
    
    return sequence[1:]