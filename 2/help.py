import numpy as np
import matplotlib.pyplot as plt

def one_hot_encode(index, num_classes):
    vec = np.zeros((num_classes, 1))
    vec[index] = 1
    return vec

def prepare_dataset(raw_data, num_classes):
    dataset = []
    for row in raw_data:
        features = np.array(row[:-1], dtype=float).reshape(-1, 1)
        label = one_hot_encode(int(row[-1]), num_classes)
        dataset.append((features, label))
    return dataset

