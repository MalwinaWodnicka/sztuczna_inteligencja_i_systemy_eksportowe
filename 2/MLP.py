import random
import numpy as np
import json

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(output):
    return output * (1 - output)

class NeuralNet:
    def __init__(self, layers, use_bias=True):
        self.layers = layers
        self.use_bias = use_bias
        self.biases = [np.random.uniform(-1, 1, (y, 1)) if use_bias else np.zeros((y, 1))
                       for y in layers[1:]]
        self.weights = [np.random.uniform(-1, 1, (y, x)) for x, y in zip(layers[:-1], layers[1:])]
        self.velocity = [np.zeros_like(w) for w in self.weights]

    def forward(self, inputs):
        # Propagacja w przód
        activations = [np.array(inputs).reshape(-1, 1)]

        # Dla każdej warstwy obliczamy z = W * a + b, a następnie aktywację.
        for w, b in zip(self.weights, self.biases):
            z = np.dot(w, activations[-1]) + b  # Suma ważona wejść plus bias
            a = sigmoid(z)  # Przepuszczamy przez funkcję aktywacji sigmoid
            activations.append(a)  # Zapisujemy

        # Zwracamy aktywacje z każdej warstwy (łącznie z wejściem).
        return activations

    def backward(self, targets, activations, lr, momentum):
        # propagacja wsteczna - służy do obliczenia, jak zmienić wagi, żeby zmniejszyć błąd popełniony przez sieć.
        targets = np.array(targets).reshape(-1, 1)
        errors = [None] * len(self.weights) # pusta tablica o długości ilości wag
        # (wyjście sieci - to co powinno wyjść) * pochodna funkcji aktywacji (mówi nam jak bardzo możemy zmieniać wyjście)
        delta = (activations[-1] - targets) * sigmoid_derivative(activations[-1])
        errors[-1] = delta

        for l in range(len(errors) - 2, -1, -1):
            # iloczyn skalarny transponowanej tablicy wag i błędu z następnej warstwy pomnożony przez pochodną fun aktywacji
            delta = np.dot(self.weights[l + 1].T, errors[l + 1]) * sigmoid_derivative(activations[l + 1])
            errors[l] = delta

        for i in range(len(self.weights)):
            # aktualizacja wag i biasu
            grad_w = np.dot(errors[i], activations[i].T)
            self.velocity[i] = momentum * self.velocity[i] - lr * grad_w
            self.weights[i] += self.velocity[i]
            if self.use_bias:
                self.biases[i] -= lr * errors[i]

    def train(self, data, lr=0.1, momentum=0.9, max_epochs=1000, min_error=None, shuffle=False,
              log_path=None, log_interval=10):
        if log_path:
            with open(log_path, 'w') as log:
                log.write("epoch,loss\n")

        for epoch in range(max_epochs):
            if shuffle:
                random.shuffle(data)

            total_loss = 0
            for x, y in data:
                activations = self.forward(x)
                preds = activations[-1]
                loss = np.sum((np.array(y).reshape(-1, 1) - preds) ** 2)
                total_loss += loss
                self.backward(y, activations, lr, momentum)

            avg_loss = total_loss / len(data)
            print(f"Epoch {epoch + 1}, Loss: {avg_loss:.6f}")

            if log_path and (epoch + 1) % log_interval == 0:
                with open(log_path, 'a') as log:
                    log.write(f"{epoch + 1},{avg_loss}\n")

            if min_error is not None and avg_loss <= min_error:
                print("Target error achieved. Training stopped.")
                break

    def saveToFile(self, path):
        data = {
            'weights': [w.tolist() for w in self.weights],
            'biases': [b.tolist() for b in self.biases] if self.use_bias else None
        }
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

    def loadFromFile(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
        self.weights = [np.array(w) for w in data['weights']]
        self.biases = [np.array(b) for b in data['biases']] if self.use_bias and data['biases'] else [np.zeros((w.shape[0], 1)) for w in self.weights]
        self.velocity = [np.zeros_like(w) for w in self.weights]

    def test(self, data):
        print("\n=== TEST RESULTS ===")
        total_loss = 0
        for i, (x, y) in enumerate(data):
            output = self.forward(x)[-1]
            error = np.sum((np.array(y).reshape(-1, 1) - output) ** 2)
            total_loss += error
            print(f"Sample {i + 1}:")
            print(f"  Input:      {[f'{val:.3f}' for val in x]}")
            print(f"  Expected:   {[f'{val:.3f}' for val in y]}")
            print(f"  Predicted:  {[f'{val[0]:.3f}' for val in output]}")
            print(f"  Error: {error:.6f}\n")
        print(f"Average error (MSE): {total_loss / len(data):.6f}")
