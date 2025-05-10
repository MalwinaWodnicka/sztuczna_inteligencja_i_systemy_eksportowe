import pickle
import random
import numpy as np
import matplotlib.pyplot as plt
from functions import sigmoid, sigmoid_derivative


class MLP:
    def __init__(self, layer_dims, use_bias):
        self.layer_dims = layer_dims
        self.num_layers = len(layer_dims)
        self.use_bias = use_bias

        self.weights = [np.random.uniform(-1, 1, (y, x))
                        for x, y in zip(layer_dims[:-1], layer_dims[1:])]
        self.biases = [np.random.uniform(-1, 1, (y, 1)) if use_bias else np.zeros((y, 1))
                       for y in layer_dims[1:]]

        self.previous_weight_updates = [np.zeros_like(w) for w in self.weights]

    def train(self, data, epochs, stop_error, lr, momentum, shuffle_data, log_interval):
        logs = []
        for epoch in range(epochs):
            if shuffle_data:
                random.shuffle(data)
            self._train_epoch(data, lr, momentum)

            current_error = self._compute_total_error(data)
            if stop_error != -1 and current_error <= stop_error:
                print("Osiagnieto pozadany poziom bledu.")
                break
            if epoch % log_interval == 0:
                print(f"Epoka: {epoch}, Błąd: {current_error:.6f}")
                logs.append(f"{epoch}, {current_error}\n")

        with open('data/train_logs.csv', 'w') as f:
            f.writelines(logs)

    def _train_epoch(self, batch, lr, momentum):
        bias_deltas = [np.zeros_like(b) for b in self.biases]
        weight_deltas = [np.zeros_like(w) for w in self.weights]

        for x, y in batch:
            b_delta, w_delta = self._backward(x, y)
            bias_deltas = [bd + d for bd, d in zip(bias_deltas, b_delta)]
            weight_deltas = [wd + d for wd, d in zip(weight_deltas, w_delta)]

        self.previous_weight_updates = [momentum * pwu - (lr / len(batch)) * wd
                                         for pwu, wd in zip(self.previous_weight_updates, weight_deltas)]
        self.weights = [w + dw for w, dw in zip(self.weights, self.previous_weight_updates)]

        if self.use_bias:
            self.biases = [b - (lr / len(batch)) * bd for b, bd in zip(self.biases, bias_deltas)]

    def _forward(self, input_vector):
        for w, b in zip(self.weights, self.biases):
            input_vector = sigmoid(np.dot(w, input_vector) + b)
        return input_vector

    def _backward(self, x, y):
        bias_grad = [np.zeros_like(b) for b in self.biases]
        weight_grad = [np.zeros_like(w) for w in self.weights]

        activations = [x]
        z_values = []
        for w, b in zip(self.weights, self.biases):
            z = np.dot(w, activations[-1]) + b
            z_values.append(z)
            activations.append(sigmoid(z))

        delta = (activations[-1] - y) * sigmoid_derivative(activations[-1])
        bias_grad[-1] = delta
        weight_grad[-1] = np.dot(delta, activations[-2].T)

        for l in range(2, self.num_layers):
            z = z_values[-l]
            sp = sigmoid_derivative(activations[-l])
            delta = np.dot(self.weights[-l + 1].T, delta) * sp
            bias_grad[-l] = delta
            weight_grad[-l] = np.dot(delta, activations[-l - 1].T)

        return bias_grad, weight_grad

    def _compute_total_error(self, data):
        return np.mean([np.mean(np.square(self._forward(x) - y)) for x, y in data])

    def predict(self, x):
        return self._forward(x)

    def save(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(path):
        with open(path, 'rb') as f:
            return pickle.load(f)

    def plot_errors(self):
        with open('data/train_logs.csv', 'r') as f:
            entries = f.readlines()
        epochs, errors = zip(*[map(float, entry.strip().split(',')) for entry in entries])
        plt.plot(epochs, errors, label='Błąd treningowy', color='purple')
        plt.xlabel('Epoka')
        plt.ylabel('Błąd')
        plt.title('Przebieg błędu treningowego')
        plt.grid(True)
        plt.legend()
        plt.show()
