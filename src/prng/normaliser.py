def normaliser(sequence: list, m: int):
    normalized_sequence = []
    for num in sequence:
        normalized_sequence.append(num/m)
    return normalized_sequence