import numpy as np
import pickle


def sigmoid(x): return 1 / (1 + np.exp(-x))
def sigmoid_grad(x): return x * (1 - x)

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / np.sum(e_x, axis=0, keepdims=True)

def cross_entropy_loss(y_true, y_pred):
    return -np.sum(y_true * np.log(y_pred + 1e-8))  # CHANGED

def cross_entropy_deriv(y_true, y_pred):
    return y_pred - y_true


class NeuralNet:
    def __init__(self, layers, use_bias=True):
        self.layers = layers
        self.use_bias = use_bias
        self.biases = [np.random.uniform(-1, 1, (y, 1)) if use_bias else np.zeros((y, 1))
                       for y in layers[1:]]
        self.weights = [np.random.uniform(-1, 1, (y, x)) for x, y in zip(layers[:-1], layers[1:])]
        self.velocity = [np.zeros_like(w) for w in self.weights]

    def forward(self, x):
        for i, (b, w) in enumerate(zip(self.biases, self.weights)):
            z = np.dot(w, x) + b if self.use_bias else np.dot(w, x)
            if i == len(self.weights) - 1:
                x = softmax(z)  # CHANGED
            else:
                x = sigmoid(z)
        return x

    def backward(self, x, y):
        grads_b = [np.zeros_like(b) for b in self.biases]
        grads_w = [np.zeros_like(w) for w in self.weights]
        activations = [x]
        zs = []

        for i, (b, w) in enumerate(zip(self.biases, self.weights)):
            z = np.dot(w, x) + b if self.use_bias else np.dot(w, x)
            zs.append(z)
            if i == len(self.weights) - 1:
                x = softmax(z)
            else:
                x = sigmoid(z)
            activations.append(x)

        delta = cross_entropy_deriv(y, activations[-1])
        grads_b[-1] = delta
        grads_w[-1] = delta @ activations[-2].T

        for l in range(2, len(self.layers)):
            z = zs[-l]
            delta = (self.weights[-l + 1].T @ delta) * sigmoid_grad(sigmoid(z))
            grads_b[-l] = delta
            grads_w[-l] = delta @ activations[-l - 1].T

        return grads_b, grads_w

    def update(self, batch, lr, momentum):
        batch_size = len(batch)
        total_b = [np.zeros_like(b) for b in self.biases]
        total_w = [np.zeros_like(w) for w in self.weights]

        for x, y in batch:
            db, dw = self.backward(x, y)
            total_b = [tb + db_i for tb, db_i in zip(total_b, db)]
            total_w = [tw + dw_i for tw, dw_i in zip(total_w, dw)]

        for i in range(len(self.weights)):
            self.velocity[i] = momentum * self.velocity[i] - (lr / batch_size) * total_w[i]
            self.weights[i] += self.velocity[i]

        if self.use_bias:
            self.biases = [b - (lr / batch_size) * db for b, db in zip(self.biases, total_b)]

    def get_hidden_output(self, x):
        a = x
        for i in range(len(self.weights) - 1):
            z = np.dot(self.weights[i], a)
            if self.use_bias:
                z += self.biases[i]
            a = sigmoid(z)
        return a

    def train(self, data, epochs, stop_error, lr, momentum, shuffle=True, log_step=10):
        logs = []
        for epoch in range(epochs):
            if shuffle:
                np.random.shuffle(data)

            self.update(data, lr, momentum)

            total_loss = np.mean([
                cross_entropy_loss(y, self.forward(x)) for x, y in data
            ])

            if (epoch + 1) % log_step == 0 or epoch == 0:
                print(f"Epoch {epoch + 1}, Error: {total_loss:.6f}")
                logs.append((epoch + 1, total_loss))

            if stop_error != -1 and total_loss <= stop_error:
                print(f"OTarget error ({stop_error}) reached. Training completed.")
                break
        with open("data/train_logs.csv", "w") as f:
            for ep, err in logs:
                f.write(f"{ep},{err}\n")


    def save(self, path):
        with open(path, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(path):
        with open(path, "rb") as f:
            return pickle.load(f)
