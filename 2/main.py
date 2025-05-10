import pandas as pd
from MLP_module import NeuralNet
from helper import prepare_dataset, plot_training_error
import numpy as np


def get_input(prompt, cast_type=int, cond=lambda x: True):
    while True:
        try:
            val = cast_type(input(prompt))
            if cond(val): return val
        except: pass


if __name__ == "__main__":
    print("1 - Iris Dataset\n2 - Autoencoder Example")
    dataset_choice = get_input("Select dataset: ", int, lambda x: x in [1, 2])

    if dataset_choice == 1:
        df = pd.read_csv("data/data.csv", header=None)
        df = df.sample(frac=1).reset_index(drop=True)
        train_data = prepare_dataset(df.tail(120).values, 3)
        test_data = prepare_dataset(df.head(30).values, 3)
        input_size = 4
        output_size = 3
    else:
        train_data = [(np.eye(4)[i].reshape(4, 1), np.eye(4)[i].reshape(4, 1)) for i in range(4)]
        test_data = train_data[:]
        input_size = 4
        output_size = 4

    print("1 - Train Mode\n2 - Test Mode")
    mode = get_input("Choose mode: ", int, lambda x: x in [1, 2])

    if mode == 1:
        print("1 - Load from file\n2 - Create new network")
        load_mode = get_input("Load or new: ", int)

        if load_mode == 1:
            net = NeuralNet.load("data/network.pkl")
        else:
            hidden_layers = [get_input(f"Neurons in hidden layer {i+1}: ") for i in range(
                get_input("Number of hidden layers: "))]

            use_bias = get_input("Use bias? (1-yes / 0-no): ", int) == 1
            net = NeuralNet([input_size] + hidden_layers + [output_size], use_bias)

        stop_type = get_input("Stop condition: 1 - Epochs, 2 - Error threshold: ", int)
        epochs, stop_error = (get_input("Epochs: "), -1.0) if stop_type == 1 else (10000, get_input("Error threshold: ", float))

        lr = get_input("Learning rate (0-1): ", float, lambda x: 0 <= x <= 1)
        momentum = get_input("Momentum (0-1): ", float, lambda x: 0 <= x <= 1)
        log_step = get_input("Log step: ", int)
        shuffle = get_input("Shuffle data? (1-yes / 0-no): ", int) == 1

        net.train(train_data, epochs, stop_error, lr, momentum, shuffle, log_step)
        net.save("data/network.pkl")

    else:
        net = NeuralNet.load("data/network.pkl")
        correct = 0
        for x, y in test_data:
            pred = np.argmax(net.forward(x))
            actual = np.argmax(y)
            if pred == actual:
                correct += 1
            print(f"Expected: {actual}, Predicted: {pred}")
        print(f"Accuracy: {correct / len(test_data):.2%}")
        plot_training_error("data/train_logs.csv")
