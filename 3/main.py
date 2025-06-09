from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.svm import SVC
import seaborn as sns
import matplotlib.pyplot as plt



file_path = Path(__file__).parent / 'data' / 'bupa.data'
columns = ['Mcv', 'Alkphos', 'Sgpt', 'Sgot', 'Gammagt', 'Drinks', 'Selector']
data = pd.read_csv(file_path, header=None, names=columns)

X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values
y = np.where(y == 2, 0, 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = SVC(kernel='rbf', C=1.0, gamma='scale')
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)

print("\nWyniki dla: SVM (RBF Kernel)")
print(classification_report(y_test, y_pred, digits=3))

cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Zdrowy', 'Chory'], yticklabels=['Zdrowy', 'Chory'])
plt.title('Macierz pomyłek – SVM (RBF)')
plt.xlabel('Predykcja')
plt.ylabel('Rzeczywistość')
plt.tight_layout()
plt.show()

accuracy = accuracy_score(y_test, y_pred)
print(f"Dokładność (accuracy): {accuracy * 100:.2f}%")

