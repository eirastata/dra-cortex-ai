import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer


# =============================
# Caminhos
# =============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATASET = os.path.join(BASE_DIR, "dados", "dataset_ml.csv")

MODEL_PATH = os.path.join(BASE_DIR, "model", "modelo.pkl")
VECT_PATH = os.path.join(BASE_DIR, "model", "vectorizer.pkl")


# =============================
# Treinamento
# =============================

def treinar():

    print("📥 Lendo dataset ML...")

    df = pd.read_csv(DATASET)

    print("📊 Colunas:", list(df.columns))


    # =============================
    # Separar X e Y
    # =============================

    X = df["texto"].astype(str)
    y = df["diagnostico"].astype(str)


    # =============================
    # Vetorização
    # =============================

    print("🔁 Vetorizando texto...")

    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1,2),
        stop_words=None
    )

    X_vec = vectorizer.fit_transform(X)


    # =============================
    # Treino
    # =============================

    print("🤖 Treinando modelo...")

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=42
    )

    model.fit(X_vec, y)


    # =============================
    # Salvar
    # =============================

    print("💾 Salvando modelo...")

    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECT_PATH)


    print("✅ Treinamento finalizado!")
    print("📁 Modelo:", MODEL_PATH)
    print("📁 Vetor:", VECT_PATH)



# =============================
# Start
# =============================

if __name__ == "__main__":
    treinar()
