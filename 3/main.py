import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Wczytanie danych
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/liver-disorders/bupa.data'
columns = ['Mcv', 'Alkphos', 'Sgpt', 'Sgot', 'Gammagt', 'Drinks', 'Selector']
data = pd.read_csv(url, header=None, names=columns)

# 2. Przygotowanie danych
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values
y = np.where(y == 2, 0, 1)  # Zakoduj klasy: 1 = chory, 0 = zdrowy

# 3. Podział na dane treningowe i testowe
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Normalizacja cech
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5. SVM – trenowanie modelu
model = SVC(kernel='rbf', C=1.0, gamma='scale')
model.fit(X_train_scaled, y_train)

# 6. Predykcja i ocena
y_pred = model.predict(X_test_scaled)

print("\n📊 Wyniki dla: SVM (RBF Kernel)")
print(classification_report(y_test, y_pred, digits=3))

# 7. Macierz pomyłek
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Zdrowy', 'Chory'], yticklabels=['Zdrowy', 'Chory'])
plt.title('Macierz pomyłek – SVM (RBF)')
plt.xlabel('Predykcja')
plt.ylabel('Rzeczywistość')
plt.tight_layout()
plt.show()
