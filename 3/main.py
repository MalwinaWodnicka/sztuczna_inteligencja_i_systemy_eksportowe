import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.svm import SVC
import seaborn as sns
import matplotlib.pyplot as plt


file_path = Path(__file__).parent / 'data' / 'bupa.data'
columns = ['Mcv', 'Alkphos', 'Sgpt', 'Sgot', 'Gammagt', 'Drinks', 'Selector']
data = pd.read_csv(file_path, header=None, names=columns)

# 2. Przygotowanie danych
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values
y = np.where(y == 2, 0, 1)  # 1 = chory, 0 = zdrowy

# 3. Podział na dane treningowe i testowe
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Normalizacja cech
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train) # liczy średnią i odchylenie standardowe
X_test_scaled = scaler.transform(X_test) # odejmuje od każdej wartości średnią i wynik dzieli na odchylenie standardowe

# 5. Optymalizacja parametrów za pomocą GridSearchCV
param_grid = {
    'C': [0.1, 1, 10, 100],
    'gamma': ['scale', 0.01, 0.1, 1, 10],
    'kernel': ['rbf']
}

# super vector classifier
grid = GridSearchCV(SVC(), param_grid, cv=5, scoring='accuracy') # testuje wszystkie kombinacje parametrów
# cv -> walidacja krzyżowa. Dzieli dane treningowe na 5 i na 4 z nich trenuje 5 jest dla testów
# scoring -> accuracy oznacza że prównuje modele na podstawie ich dokładności – czyli procentu poprawnych przewidywań
grid.fit(X_train_scaled, y_train)

print("Najlepsze parametry:", grid.best_params_)
print("Najlepszy wynik walidacji:", grid.best_score_)

# 6. Użycie najlepszego modelu do predykcji
best_model = grid.best_estimator_
y_pred = best_model.predict(X_test_scaled)

# 7. Wyniki
print("\nWyniki dla: Najlepszy SVM")
print(classification_report(y_test, y_pred, digits=3))

accuracy = accuracy_score(y_test, y_pred)
print(f"Dokładność na zbiorze testowym: {accuracy * 100:.2f}%")

# 8. Macierz pomyłek
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Zdrowy', 'Chory'], yticklabels=['Zdrowy', 'Chory'])
plt.title('Macierz pomyłek – SVM (najlepszy)')
plt.xlabel('Predykcja')
plt.ylabel('Rzeczywistość')
plt.tight_layout()
plt.show()

# 9. Wykres błędu w zależności od C
# C_values = np.logspace(-3, 2, 10)
# errors = []
#
# for C in C_values:
#     model = SVC(kernel='rbf', C=C, gamma=grid.best_params_['gamma'])
#     model.fit(X_train_scaled, y_train)
#     y_pred_temp = model.predict(X_test_scaled)
#     error = 1 - accuracy_score(y_test, y_pred_temp)
#     errors.append(error)
#
# plt.figure()
# plt.semilogx(C_values, errors, marker='o', color='purple')
# plt.title('Wykres błędu w zależności od C')
# plt.xlabel('Wartość C (log scale)')
# plt.ylabel('Błąd klasyfikacji')
# plt.grid(True)
# plt.tight_layout()
# plt.ylim(bottom=0)
# plt.show()