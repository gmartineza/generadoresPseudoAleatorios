def extract_middle_digits(malcolm, d): # TODO: update?
    malcolm_str = str(malcolm)
    if (len(malcolm_str) % 2) != (d % 2):
        malcolm_str = '0' + malcolm_str
    if len(malcolm_str) < d:
        raise ValueError(f"extract_middle_digits: Number {malcolm} has fewer digits than required {d}")
    middle_start = (len(malcolm_str) - d) // 2
    return int(malcolm_str[middle_start:middle_start + d])

def generate_sequence(n, d, x1, x2):
    if len(str(x1)) != d:
        raise ValueError(f"Initial number x1 must have exactly {d} digits")
    if len(str(x2)) != d:
        raise ValueError(f"Initial number x2 must have exactly {d} digits")
    
    series = [x1, x2]
    
    for _ in range(n):
        product = x1 * x2
        x3 = extract_middle_digits(product, d)
        series.append(x3)
        x1 = x2
        x2 = x3
    
    return series

def main():
    n = int(input("Enter number of random numbers to generate: "))
    d = int(input("Enter number of digits for each number: "))
    x1 = int(input(f"Enter initial {d}-digit number: "))
    x2 = int(input(f"Enter initial {d}-digit number: "))
    
    series = generate_sequence(n, d, x1, x2)
    print("\nGenerated sequence:")
    print(series)

if __name__ == "__main__":
    main()