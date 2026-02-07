import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# ===============================
# CONFIG
# ===============================

DATASET_PATH = "dados/dataset_medico_v3.csv"

MODEL_PATH = "model/modelo.pkl"
VECT_PATH = "model/vectorizer.pkl"


# ===============================
# LOAD DATA
# ===============================

print("📊 Carregando dataset...")

df = pd.read_csv(DATASET_PATH)

print("Registros:", len(df))


# ===============================
# FEATURES / TARGET
# ===============================

X = df["texto"].astype(str)
y = df["doenca"]


# ===============================
# SPLIT
# ===============================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)


# ===============================
# VECTORIZER
# ===============================

vectorizer = TfidfVectorizer(
    ngram_range=(1,2),
    max_features=5000,
    stop_words=None
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)


# ===============================
# MODEL
# ===============================

model = LogisticRegression(
    max_iter=2000,
    class_weight="balanced"
)

model.fit(X_train_vec, y_train)


# ===============================
# EVALUATION
# ===============================

y_pred = model.predict(X_test_vec)

acc = accuracy_score(y_test, y_pred)

print("\n============================")
print("ACURÁCIA:", round(acc*100,2), "%")
print("============================\n")

print(classification_report(y_test, y_pred))


# ===============================
# SAVE
# ===============================

joblib.dump(model, MODEL_PATH)
joblib.dump(vectorizer, VECT_PATH)

print("💾 Modelo salvo em:", MODEL_PATH)
print("💾 Vetorizador salvo em:", VECT_PATH)
