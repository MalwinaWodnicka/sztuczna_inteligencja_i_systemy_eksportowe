import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from help import prepare_dataset
from MLP import NeuralNet as network


def get_input(prompt, cast_type=int, cond=lambda x: True):
    while True:
        try:
            val = cast_type(input(prompt))
            if cond(val): return val
        except:
            pass


if __name__ == "__main__":

    while True:
        print("1 - Iris Dataset\n2 - Autoencoder Example\n3 - Quit")
        dataset_choice = get_input("Select dataset: ", int)
        if dataset_choice not in [1, 2, 3]:
            print("Invalid choice")
        else:
            break

    if dataset_choice == 1:
        df = pd.read_csv("data/data.csv", header=None)
        df = df.sample(frac=1, random_state=45).reset_index(drop=True)
        train_data = prepare_dataset(df.tail(120).values, 3)
        test_data = prepare_dataset(df.head(30).values, 3)
        input_size = 4
        output_size = 3
        print(train_data)
    else:
        train_data = [(np.array([[1], [0], [0], [0]]), np.array([[1], [0], [0], [0]])),
                      (np.array([[0], [1], [0], [0]]), np.array([[0], [1], [0], [0]])),
                      (np.array([[0], [0], [1], [0]]), np.array([[0], [0], [1], [0]])),
                      (np.array([[0], [0], [0], [1]]), np.array([[0], [0], [0], [1]]))]

        test_data = [(np.array([[1], [0], [0], [0]]), np.array([[1], [0], [0], [0]])),
                     (np.array([[0], [1], [0], [0]]), np.array([[0], [1], [0], [0]])),
                     (np.array([[0], [0], [1], [0]]), np.array([[0], [0], [1], [0]])),
                     (np.array([[0], [0], [0], [1]]), np.array([[0], [0], [0], [1]]))]
        input_size = 4
        output_size = 4

    isNetwork = False
    while True:
        if isNetwork:
            print("1. Train mode")
            print("2. Test mode")
            print("3. Save network")
            print("4. Quit")
            option = get_input("Choose an option: ")
        else:
            print("What do you want to do?")
            print("1. Create new network")
            print("2. Load network")
            print("4. Quit")
            option = get_input("Choose an option: ")
        if option == 1 and isNetwork:
            stop_type = get_input("Stop condition: 1 - Epochs, 2 - Error threshold: ", int)
            epochs, stop_error = (get_input("Epochs: "), -1.0) if stop_type == 1 else (10000,
                    get_input("Error threshold: ", float))
            log_step = get_input("Log step: ", int)
            # trening
        if option == 2 and isNetwork:
            correct = [0] * output_size
            predicted_labels = []
            true_labels = []

            with open("trainStats.txt", "w") as file:
                for index in range(len(test_data)):
                    inputs, expected = test_data[index]
                    inputs = inputs.reshape(-1)
                    expected = expected.reshape(-1)

                    output = network.forward(inputs)
                    output = np.array(output).reshape(-1)

                    true_label = np.argmax(expected)
                    predicted_label = np.argmax(output)

                    true_labels.append(true_label)
                    predicted_labels.append(predicted_label)

                    if predicted_label == true_label:
                        correct[true_label] += 1

                    error = network.calculateError(expected, output)

                    neuronWeights = []
                    neuronOutputs = []
                    for layer in network.layers:
                        layerWeights = [neuron.weights for neuron in layer.neurons]
                        layerOutputs = [neuron.output for neuron in layer.neurons]
                        neuronWeights.append(layerWeights)
                        neuronOutputs.append(layerOutputs)

                    file.write(f"Wzorzec numer: {index}, {inputs}\n")
                    file.write(f"Popelniony blad dla wzorca: {error}\n")
                    file.write(f"Pozadany wzorzec odpowiedzi: {expected}\n")
                    for i in range(len(output)):
                        file.write(f"Blad popelniony na {i} wyjsciu: {output[i] - expected[i]}\n")
                        file.write(f"Wartosc na {i} wyjsciu: {output[i]}\n")
                    file.write(f"Wartosci wag neuronow wyjsciowych\n {neuronWeights[-1]}\n")
                    for i in reversed(range(len(network.layers) - 1)):
                        file.write(f"Wartosci wyjsciowe neuronow ukrytych warstwy {i}: {neuronOutputs[i]}\n")
                        file.write(f"Wartosci wag neuronow ukrytych warstwy {i}:\n {neuronWeights[i]}\n")
                    file.write("\n\n")

            print("Confusion Matrix:")
            print(confusion_matrix(true_labels, predicted_labels))
            print("\nClassification Report:")
            print(classification_report(true_labels, predicted_labels))





