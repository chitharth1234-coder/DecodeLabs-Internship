"""
Project 2: Data Classification Using AI
DecodeLabs Industrial Training Kit

Pipeline (per slide deck):
  INPUT   -> Iris dataset + Feature Scaling (StandardScaler)
  PROCESS -> Train-Test Split + KNN Algorithm (k=5)
  OUTPUT  -> Confusion Matrix + F1 Score
"""

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report, f1_score, accuracy_score

# ---------------------------------------------------------------
# INPUT: Load and understand the dataset
# ---------------------------------------------------------------
iris = load_iris()
X = iris.data                      # features: sepal/petal length & width
y = iris.target                    # labels: 0=setosa, 1=versicolor, 2=virginica
class_names = iris.target_names

df = pd.DataFrame(X, columns=iris.feature_names)
df["species"] = [class_names[i] for i in y]

print("=== Dataset Overview ===")
print(f"Samples: {df.shape[0]}, Features: {X.shape[1]}, Classes: {len(class_names)}")
print("\nClass distribution:")
print(df["species"].value_counts())
print("\nFirst 5 rows:")
print(df.head())

# ---------------------------------------------------------------
# INPUT (cont.): Feature Scaling -- "The Gatekeeper Rule"
# StandardScaler -> mean = 0, variance = 1
# ---------------------------------------------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ---------------------------------------------------------------
# PROCESS: Train-Test Split (80% train / 20% test, shuffled)
# ---------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, shuffle=True, stratify=y
)
print(f"\n=== Train/Test Split ===")
print(f"Training samples: {len(X_train)}, Testing samples: {len(X_test)}")

# ---------------------------------------------------------------
# PROCESS (cont.): KNN Algorithm (k=5)
# ---------------------------------------------------------------
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

# ---------------------------------------------------------------
# OUTPUT: Confusion Matrix + F1 Score (accuracy alone is a "mirage")
# ---------------------------------------------------------------
accuracy = accuracy_score(y_test, predictions)
f1 = f1_score(y_test, predictions, average="weighted")
cm = confusion_matrix(y_test, predictions)

print("\n=== Output Validation ===")
print(f"Accuracy: {accuracy * 100:.1f}%")
print(f"F1 Score (weighted): {f1:.3f}")

print("\nConfusion Matrix:")
cm_df = pd.DataFrame(cm, index=class_names, columns=class_names)
print(cm_df)

print("\nClassification Report:")
print(classification_report(y_test, predictions, target_names=class_names))