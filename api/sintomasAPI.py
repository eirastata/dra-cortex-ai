from fastapi import APIRouter
from pydantic import BaseModel

import joblib
import numpy as np


# =========================
# LOAD MODEL
# =========================

model = joblib.load("model/modelo.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")


# =========================
# ROUTER
# =========================

router = APIRouter()


# =========================
# INPUT
# =========================

class SintomaInput(BaseModel):
    texto: str


# =========================
# CORE
# =========================

def diagnosticar(texto):

    X = vectorizer.transform([texto])

    probs = model.predict_proba(X)[0]
    classes = model.classes_

    top_idx = np.argsort(probs)[-3:][::-1]

    resultados = []

    for i in top_idx:
        resultados.append({
            "doenca": classes[i],
            "confianca": round(float(probs[i]) * 100, 2)
        })

    principal = resultados[0]

    return {
        "principal": principal,
        "top3": resultados
    }


# =========================
# ENDPOINT
# =========================

@router.post("/prever")
async def prever(dados: SintomaInput):

    resultado = diagnosticar(dados.texto)

    return resultado
