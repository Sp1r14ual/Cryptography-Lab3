import math


def to_binary(n):
    if n == 0.0:
        return "00000000000"
    if n >= 1 or n < 0:
        return "ERROR"

    answer = ""
    while n > 0:
        b = n * 2
        if b >= 1:
            answer += "1"
            n = b - 1
        else:
            answer += "0"
            n = b

    return answer


def generate_assembly(alphabet, p):
    assembly = [(alphabet[i], p[i]) for i in range(len(alphabet))]
    return assembly


def generate_shannon_codes(alphabet, p):
    assembly = generate_assembly(alphabet, p)
    assembly.sort(key=lambda x: x[1], reverse=True)

    bx = [(assembly[0][0], 0.0)]
    for i in range(1, len(assembly)):
        pair_to_be_pushed = (assembly[i][0], bx[i - 1][1] + assembly[i - 1][1])
        bx.append(pair_to_be_pushed)

    bins = [(pair[0], to_binary(pair[1])) for pair in bx]

    lx = [(pair[0], math.ceil(-math.log2(pair[1]))) for pair in assembly]

    codes = [(assembly[i][0], bins[i][1][:lx[i][1]])
             for i in range(len(assembly))]

    return codes


# def calculate_average_code_length(codes):
#     sum_lengths = sum(len(code[1]) for code in codes)
#     n = len(codes)
#     return sum_lengths / n


# def entropy(assembly):
#     entropy_val = 0
#     for el in assembly:
#         entropy_val += el[1] * math.log2(el[1])

#     entropy_val = -entropy_val
#     return entropy_val


# def redundancy(assembly, codes):
#     r = calculate_average_code_length(codes) - entropy(assembly)
#     return r


# def kraft_mcmillan_inequality_check(codes):
#     lx = [len(code[1]) for code in codes]
#     kraft_sum = sum(2**(-l) for l in lx)
#     return kraft_sum <= 1, kraft_sum


# def calculate_properties(assembly, codes):
#     avg_code_length = calculate_average_code_length(codes)
#     r = redundancy(assembly, codes)
#     kraft_inequality = kraft_mcmillan_inequality_check(codes)
#     kraft_inequality_string = f"{'Выполняется' if kraft_inequality[0] else 'Не выполняется'}: {
#         kraft_inequality[1]} {'<= 1' if kraft_inequality[0] else '> 1'}"

#     return avg_code_length, r, kraft_inequality_string


def encode(decoded_symbols, codes, with_parity_bit=True):
    encoded_symbols = []

    for symbol in decoded_symbols:
        for code in codes:
            if code[0] == symbol:
                encoded_symbol = code[1]

                # Add parity bit for error detection
                if with_parity_bit:
                    parity_bit = str(encoded_symbol.count('1') % 2)
                    encoded_symbol += parity_bit

                encoded_symbols.append(encoded_symbol)

    with open("output.txt", "w") as writer:
        writer.write("\n".join(encoded_symbols))

    # return encoded_symbols


def decode(encoded_symbols, codes, with_parity_bit=True):
    decoded_symbols = []

    for symbol in encoded_symbols:
        if with_parity_bit:
            # Remove the parity bit
            data_bits = symbol[:-1]
            parity_bit = int(symbol[-1])

            # Check for errors using the parity bit
            if data_bits.count('1') % 2 != parity_bit:
                # Error detected, handle as needed
                decoded_symbols.append("ERROR")
                continue

        found = False
        for code in codes:
            if with_parity_bit:
                # Skip the parity bit when comparing
                if code[1] == symbol[:-1]:
                    decoded_symbols.append(code[0])
                    found = True
                    break
            else:
                if code[1] == symbol:
                    decoded_symbols.append(code[0])
                    found = True
                    break

        if not found:
            # Symbol not found in the codes
            decoded_symbols.append("UNKNOWN")

    with open("output.txt", "w") as writer:
        writer.write("\n".join(decoded_symbols))

    # return decoded_symbols


def start(alphabet, probabilities, text, mode):

    codes = generate_shannon_codes(alphabet, probabilities)

    if mode == "E":
        encode(text, codes)
    else:
        decode(text, codes)
