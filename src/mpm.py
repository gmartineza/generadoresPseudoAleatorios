def extract_middle_digits(squared, d): # TODO: update?
    squared_str = str(squared)
    print("squared_str", squared_str)
    if (len(squared_str) % 2) != (d % 2):
        squared_str = '0' + squared_str
    if len(squared_str) < d:
        raise ValueError(f"Squared number {squared} has fewer digits than required {d}")
    middle_start = (len(squared_str) - d) // 2
    print("squared_str", squared_str)
    return int(squared_str[middle_start:middle_start + d])

def generate_sequence(n, d, x1, x2):
    if len(str(x1)) != d:
        raise ValueError(f"Initial number x1 must have exactly {d} digits")
    if len(str(x2)) != d:
        raise ValueError(f"Initial number x2 must have exactly {d} digits")
    
    series = [x1]  # Step 2: Append x1 to series
    
    for _ in range(n):  # Step 8: Repeat n times
        product = x1 * x2
        x3 = extract_middle_digits(product, d)  # Step 4: Get middle digits
        series.append(x3)
        x1 = x2  # TODO: update this
    
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