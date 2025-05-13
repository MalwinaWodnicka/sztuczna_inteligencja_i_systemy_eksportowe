import pandas as pd
from MLP_module import NeuralNet
from helper import prepare_dataset, plot_training_error
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix

def get_input(prompt, cast_type=int, cond=lambda x: True):
    while True:
        try:
            val = cast_type(input(prompt))
            if cond(val): return val
        except: pass


if __name__ == "__main__":


    while True:
        print("1 - Iris Dataset\n2 - Autoencoder Example")
        dataset_choice = get_input("Select dataset: ", int)
        if dataset_choice not in [1, 2]:
            print("Niepoprawny wybor, sprobuj jeszcze raz.")
        else:
            break


    if dataset_choice == 1:
        df = pd.read_csv("data/data.csv", header=None)
        df = df.sample(frac=1, random_state=45).reset_index(drop=True)
        train_data = prepare_dataset(df.tail(120).values, 3)
        test_data = prepare_dataset(df.head(30).values, 3)
        input_size = 4
        output_size = 3
    else:
        train_data = [(np.eye(4)[i].reshape(4, 1), np.eye(4)[i].reshape(4, 1)) for i in range(4)]
        test_data = train_data[:]
        input_size = 4
        output_size = 4


    while True:
        print("1 - Train Mode\n2 - Test Mode")
        mode = get_input("Choose mode: ", int)
        if mode not in [1, 2]:
            print("Niepoprawny wybor, sprobuj jeszcze raz.")
        else:
            break

    if mode == 1:
        while True:
            print("1 - Load from file\n2 - Create new network")
            variable = get_input("Choose: ",int)
            if variable not in [1, 2]:
                print("Niepoprawny wybor, sprobuj jeszcze raz.")
            else:
                break

        if variable == 1:
            net = NeuralNet.load("data/network.pkl")
        else:
            hidden_layers = [get_input(f"Neurons in hidden layer {i+1}: ") for i in range(
                get_input("Number of hidden layers: "))]


            use_bias = get_input("Use bias? (1-yes / 0-no): ", int) == 1
            net = NeuralNet([input_size] + hidden_layers + [output_size], use_bias)

        stop_type = get_input("Stop condition: 1 - Epochs, 2 - Error threshold: ", int)
        epochs, stop_error = (get_input("Epochs: "), -1.0) if stop_type == 1 else (10000, get_input("Error threshold: ", float))

        lr = get_input("Learning rate (0-1): ", float, lambda x: 0 <= x <= 1)
        dec = get_input("Do you want momentum? 1-yes/0-no: ")
        if dec == 1:
            momentum = get_input("Momentum (0-1): ", float, lambda x: 0 <= x <= 1)
        else:
            momentum = 0.0
        log_step = get_input("Log step: ", int)
        shuffle = get_input("Shuffle data? (1-yes / 0-no): ", int) == 1

        net.train(train_data, epochs, stop_error, lr, momentum, shuffle, log_step)
        net.save("data/network.pkl")

    else:
        net = NeuralNet.load("data/network.pkl")
        correct = 0

        y_true = []
        y_pred = []
        for x, y in test_data:
            pred = np.argmax(net.forward(x))
            hidden_outputs = net.get_hidden_output(x)
            print(f"Wejście: {x.ravel()} -> Ukryte: {hidden_outputs.ravel()}")
            actual = np.argmax(y)
            y_true.append(actual)
            y_pred.append(pred)
            if pred == actual:
                correct += 1
            print(f"Expected: {actual}, Predicted: {pred}")
        print(f"Accuracy: {correct / len(test_data):.2%}")
        plot_training_error("data/train_logs.csv")

        print("\nConfusion Matrix:")
        cm = confusion_matrix(y_true, y_pred)
        print(cm)

        print("\nClassification Report:")
        print(classification_report(y_true, y_pred, digits=4))

        print("\nCorrect classifications per class:")
        for i in range(len(cm)):
            print(f"Class {i}: {cm[i][i]} correctly classified")

        total_correct = sum(cm[i][i] for i in range(len(cm)))
        print(f"\nTotal correct classifications: {total_correct}/{len(y_true)}")
