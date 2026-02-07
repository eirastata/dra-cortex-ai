import pandas as pd


def dataset_completo():
    df = pd.read_csv("dados/dataset_texto_livre_limpo.csv")
    return df