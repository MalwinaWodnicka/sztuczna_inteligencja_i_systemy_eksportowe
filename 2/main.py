import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from help import prepare_dataset, plot_training_error
from MLP import NeuralNet as network
import MLP


def get_input(prompt, cast_type=int, cond=lambda x: True, default=None):
    while True:
        try:
            user_input = input(prompt)
            if not user_input and default is not None:
                return default
            val = cast_type(user_input)
            if cond(val):
                return val
            else:
                print(f"Value must satisfy: {cond.__doc__}")
        except ValueError:
            print(f"Please enter a valid {cast_type.__name__}")
        except Exception as e:
            print(f"Error: {str(e)}")


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

    current_network = None
    isNetwork = False

    while True:
        if isNetwork:
            print("\n1. Train mode")
            print("2. Test mode")
            print("3. Save network")
            print("4. Load different network")
            print("5. Quit")
            option = get_input("Choose an option [1]: ", int, lambda x: 1 <= x <= 5, default=1)
        else:
            print("\nNo network loaded. What do you want to do?")
            print("1. Create new network")
            print("2. Load network")
            print("3. Quit")
            option = get_input("Choose an option [1]: ", int, lambda x: 1 <= x <= 3, default=1)

            if option == 3:
                break

        if option == 1 and not isNetwork:  # Create new network
            isNetwork = True
            hidden_layers = [get_input(f"Neurons in hidden layer {i + 1}: ") for i in range(
                get_input("Number of hidden layers: "))]
            network_architecture = [input_size] + hidden_layers + [output_size]

            use_bias = get_input("Use bias? (1 - Yes, 0 - No) [1]: ", int, lambda x: x in [0, 1], default=1)

            current_network = network([input_size] + hidden_layers + [output_size], use_bias)

            stop_type = get_input("Stop condition (1 - Epochs, 2 - Error threshold) [1]: ",
                                  int, lambda x: x in [1, 2], default=1)

            if stop_type == 1:
                epochs = get_input("Enter number of epochs [1000]: ",
                                   int, lambda x: x > 0, default=1000)
                stop_error = None
            else:
                stop_error = get_input("Enter error threshold [0.01]: ",
                                       float, lambda x: x > 0, default=0.01)
                epochs = 10000  # Large number as upper bound

            lr = get_input("Enter learning rate (0.01-1.0) [0.1]: ",
                           float, lambda x: 0 < x <= 1, default=0.1)
            momentum = get_input("Enter momentum (0.0-0.9) [0.9]: ",
                                 float, lambda x: 0 <= x < 1, default=0.9)
            log_step = get_input("Enter log interval (epochs) [10]: ",
                                 int, lambda x: x > 0, default=10)
            shuffle = get_input("Shuffle data each epoch? (1 - Yes, 0 - No) [1]: ",
                                int, lambda x: x in [0, 1], default=1)

            print("\nStarting training...")
            current_network.train(
                train_data,
                lr=lr,
                momentum=momentum,
                max_epochs=epochs,
                min_error=stop_error,
                shuffle=bool(shuffle),
                log_path="training_log.csv",
                log_interval=log_step
            )
            print("Training completed!")

        elif option == 2 and not isNetwork:  # Load network
            isNetwork = True
            hidden_layers = [get_input(f"Neurons in hidden layer {i + 1}: ") for i in range(
                get_input("Number of hidden layers: "))]

            use_bias = get_input("Use bias? (1 - Yes, 0 - No) [1]: ", int, lambda x: x in [0, 1], default=1)

            default_path = "network.json"
            path = input(f"Enter path to network file [{default_path}]: ") or default_path
            try:
                current_network = network([input_size] + hidden_layers + [output_size], use_bias=True)
                current_network.loadFromFile(path)
                isNetwork = True
                print("Network loaded successfully!")
            except Exception as e:
                print(f"Error loading network: {str(e)}")

        elif option == 1 and isNetwork:  # Train mode
            hidden_layers = [get_input(f"Neurons in hidden layer {i + 1}: ") for i in range(
                get_input("Number of hidden layers: "))]
            network_architecture = [input_size] + hidden_layers + [output_size]
            print("\nTraining options:")
            stop_type = get_input("Stop condition (1 - Epochs, 2 - Error threshold) [1]: ",
                                  int, lambda x: x in [1, 2], default=1)
            use_bias = get_input("Use bias? (1 - Yes, 0 - No) [1]: ", int, lambda x: x in [0, 1], default=1)
            current_network = network([input_size] + hidden_layers + [output_size], use_bias)
            if stop_type == 1:
                epochs = get_input("Enter number of epochs [1000]: ",
                                   int, lambda x: x > 0, default=1000)
                stop_error = None
            else:
                stop_error = get_input("Enter error threshold [0.01]: ",
                                       float, lambda x: x > 0, default=0.01)
                epochs = 10000

            lr = get_input("Enter learning rate (0.01-1.0) [0.1]: ",
                           float, lambda x: 0 < x <= 1, default=0.1)
            momentum = get_input("Enter momentum (0.0-0.9) [0.9]: ",
                                 float, lambda x: 0 <= x < 1, default=0.9)
            log_step = get_input("Enter log interval (epochs) [10]: ",
                                 int, lambda x: x > 0, default=10)
            shuffle = get_input("Shuffle data each epoch? (1 - Yes, 0 - No) [1]: ",
                                int, lambda x: x in [0, 1], default=1)

            print("\nStarting training...")
            current_network.train(
                train_data,
                lr=lr,
                momentum=momentum,
                max_epochs=epochs,
                min_error=stop_error,
                shuffle=bool(shuffle),
                log_path="training_log.csv",
                log_interval=log_step
            )
            print("Training completed!")

        elif option == 2 and isNetwork:  # Test mode
            print("\nTesting network...")
            current_network.test(test_data)

            if dataset_choice == 1:  # Only for classification problems
                y_true = []
                y_pred = []
                for x, y in test_data:
                    output = current_network.forward(x)[-1]
                    y_true.append(np.argmax(y))
                    y_pred.append(np.argmax(output))

                print("\nClassification Report:")
                print(classification_report(y_true, y_pred))
                print("\nConfusion Matrix:")
                print(confusion_matrix(y_true, y_pred))

            plot_training_error("training_log.csv")


        elif option == 3 and isNetwork:  # Save network
            default_path = "network.json"
            path = input(f"Enter path to save network [{default_path}]: ") or default_path
            try:
                current_network.saveToFile(path)
                print(f"Network saved successfully to {path}!")
            except Exception as e:
                print(f"Error saving network: {str(e)}")

        elif option == 4 and isNetwork:  # Load different network
            default_path = "network.json"
            path = input(f"Enter path to network file [{default_path}]: ") or default_path
            try:
                current_network.loadFromFile(path)
                print("Network loaded successfully!")
            except Exception as e:
                print(f"Error loading network: {str(e)}")

        elif option == 5 and isNetwork:  # Quit
            break
