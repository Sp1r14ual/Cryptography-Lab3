import numpy as np


def hamming_encode(message, generator_matrix):
    # Convert the message to a numpy array
    message_array = np.array(message)

    # Check if the message length is compatible with the generator matrix
    if len(message_array) != generator_matrix.shape[0]:
        raise ValueError(
            "Message length is not compatible with the generator matrix")

    # Encode the message using matrix multiplication
    codeword = np.dot(message_array, generator_matrix) % 2
    return codeword


def hamming_decode(received_codeword, parity_check_matrix):
    # Convert the received codeword to a numpy array
    received_array = np.array(received_codeword)

    # Check if the received codeword length is compatible with the parity-check matrix
    if len(received_array) != parity_check_matrix.shape[1]:
        raise ValueError(
            "Received codeword length is not compatible with the parity-check matrix")

    # Compute the syndrome by multiplying the received codeword with the transpose of the parity-check matrix
    syndrome = np.dot(received_array, parity_check_matrix.T) % 2

    # If the syndrome is non-zero, there is an error in the received codeword
    if np.any(syndrome):
        # Find the column in the parity-check matrix that corresponds to the syndrome
        error_position = np.where(
            (parity_check_matrix.T == syndrome).all(axis=1))[0]

        # Flip the bit at the error position to correct the error
        received_array[error_position] = (
            received_array[error_position] + 1) % 2

    # Extract and return the original message
    original_message = received_array[:parity_check_matrix.shape[1] -
                                      parity_check_matrix.shape[0]]
    return original_message


# Example usage
G_matrix = np.array([[1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1]])
# H_matrix = np.array(sympy.Matrix(G_Matrix).nullspace()) % 2
H_matrix = np.array([[1, 0, 1, 0, 0, 0], [0, 1, 0, 1, 0, 0], [
                    1, 0, 0, 0, 1, 0], [0, 1, 0, 0, 0, 1]])

messages_to_encode = [
    np.array([1, 1]),
    np.array([1, 0]),
    np.array([0, 0]),
    np.array([0, 1]),
]

for i, message in enumerate(messages_to_encode):
    # Encoding the message
    encoded_codeword = hamming_encode(message, G_matrix)
    print(f"Encoded Codeword {i+1}:", encoded_codeword)

    # Simulate an error in the received codeword
    received_codeword_with_error = encoded_codeword.copy()
    received_codeword_with_error[2] = (
        received_codeword_with_error[2] + 1) % 2  # introducing an error

    # Decoding the received codeword
    decoded_message = hamming_decode(received_codeword_with_error, H_matrix)
    print(f"Original Message {i+1}:", message)
    print(f"Decoded Message {i+1}:", decoded_message)
    print()
