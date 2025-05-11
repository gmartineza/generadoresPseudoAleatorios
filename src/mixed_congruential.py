def generate_sequence(x1, a, c, m):
    sequence = [x1]
    
    for i in range(m):
        x2 = (a * x1 + c) % m
        sequence.append(x2)
        x1 = x2
    
    return sequence

def main():
    a = int(input("a: "))
    c = int(input("c: "))
    x0 = int(input("x0: "))
    m = int(input("m: "))

    if x0 < 0:
        raise ValueError("Input didn't satisfy: x0 > 0")
    elif a < 0:
        raise ValueError("Input didn't satisfy: a > 0")
    elif c < 0:
        raise ValueError("Input didn't satisfy: c > 0")
    elif m < x0:
        raise ValueError("Input didn't satisfy: m > x0")
    elif m < a:
        raise ValueError("Input didn't satisfy: m > a")
    elif m < c:
        raise ValueError("Input didn't satisfy: m > c")
    
    print(generate_sequence(x0, a, c, m))
   

if __name__ == "__main__":
    main()