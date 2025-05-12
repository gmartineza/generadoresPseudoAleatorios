def generate_sequence(n, x0, a, c, m):
    # Xn+1 = (a * Xn + c) mod m
    if not all(x > 0 for x in [x0, a, c]):
        raise ValueError("x0, a, and c must be positive numbers")
    if not m > max(x0, a, c):
        raise ValueError("m must be greater than x0, a, and c")
    
    sequence = [x0]
    xn = x0
    
    for _ in range(n):
        xn = (a * xn + c) % m
        sequence.append(xn)
    
    return sequence

def main():
    n = int(input("Enter number of random numbers to generate: "))
    x0 = int(input("Enter initial seed (X0): "))
    a = int(input("Enter multiplier (a): "))
    c = int(input("Enter additive constant (c): "))
    m = int(input("Enter module (m): "))
    
    sequence = generate_sequence(n, x0, a, c, m)
    print("\nGenerated sequence:")
    print(sequence)

if __name__ == "__main__":
    main() 