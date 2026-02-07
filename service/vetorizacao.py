from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

from service.datasetService import dataset_completo


def vetorizar():
    df = dataset_completo()

    textos = df["sintomas_limpo"].astype(str)

    vectorizer = TfidfVectorizer(max_features=1000)

    X = vectorizer.fit_transform(textos)

    return X, vectorizer


def encode_y():
    df = dataset_completo()

    y = df["diagnostico_limpo"].astype(str)

    encoder = LabelEncoder()

    y_encoded = encoder.fit_transform(y)

    return y_encoded, encoder
