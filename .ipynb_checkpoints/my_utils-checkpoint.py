import numpy as np


def get_char_dict(raw_text, stop_set=None):
    chars = sorted(list(set(raw_text)))
    
    if stop_set is None:
        stop_set = {}

    return dict((c, i) for i, c in enumerate(chars) if c not in stop_set)


def get_int_dict(raw_text, stop_set=None):
    chars = sorted(list(set(raw_text)))
    
    if stop_set is None:
        stop_set = {}

    return dict((i, c) for i, c in enumerate(chars) if c not in stop_set)



def text_encode(raw_text, char_to_int, seq_length=100):
    n_chars = len(raw_text)
    data_len = n_chars - seq_length
    
    data_X = np.empty((data_len, seq_length))
    data_y = np.empty(data_len)

    for i in range(0, n_chars - seq_length):
        seq_in = raw_text[i:i + seq_length] # берём символы с i по i + 1
        seq_out = raw_text[i + seq_length] # берём следующий символ
        # кодируем символы  для X
        data_X[i,:] = np.array([char_to_int[char] for char in seq_in])
        data_y[i] = char_to_int[seq_out] # кодируем символы для y

    return data_X, data_y