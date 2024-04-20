import numpy as np

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0
    return dot_product / (norm_vec1 * norm_vec2)

def string_to_np_array(array_string):
    # Check if the input is already a numpy array
    if isinstance(array_string, np.ndarray):
        return array_string
    # Otherwise, assume it's a string and convert
    try:
        # Strip the brackets and split the string into float values
        array_list = array_string.replace('[', '').replace(']', '').split(',')
        # Convert to a numpy array of type float
        return np.array(array_list, dtype=np.float32)
    except Exception as e:
        print("Error converting string to numpy array:", e)
        return np.zeros(1)  # return a default value in case of error
