import os
import random
import requests
import pandas as pd


# ======================================
# CHAVE ELEVENLABS
# ======================================

ELEVEN_API_KEY = "sk_312867707db2fb61dd816d626d35159e410592f79148637d"


# ======================================
# CAMINHOS
# ======================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATASET_PATH = os.path.join(
    BASE_DIR, "dados", "dataset_medico_v3.csv"
)

STATIC_DIR = os.path.join(BASE_DIR, "api", "frontend", "static")
AUDIO_PATH = os.path.join(STATIC_DIR, "voz.mp3")


# ======================================
# CARREGAR DATASET
# ======================================

print("📊 Carregando dataset médico...")

df = pd.read_csv(DATASET_PATH)

# Normalizar textos
for col in [
    "doenca",
    "sintomas_fortes",
    "sintomas_medios",
    "sintomas_leves",
    "gravidade",
    "urgencia",
    "especialidade",
    "orientacao"
]:
    df[col] = df[col].astype(str).str.lower()


print("✅ Registros carregados:", len(df))


# ======================================
# VOZ
# ======================================

VOICE_ID = "21m00Tcm4TlvDq8ikWAM"


def gerar_audio(texto):

    print("🔊 Gerando áudio...")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": texto,
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.8
        }
    }

    r = requests.post(url, json=data, headers=headers)

    if r.status_code != 200:
        print("❌ Erro ElevenLabs:", r.text)
        return

    os.makedirs(os.path.dirname(AUDIO_PATH), exist_ok=True)

    with open(AUDIO_PATH, "wb") as f:
        f.write(r.content)

    print("✅ Áudio salvo")


# ======================================
# PERSONALIDADE
# ======================================

PERSONALIDADE = {

    "baixa": [
        "O quadro parece leve, mas merece atenção.",
        "Nada indica gravidade no momento.",
        "Acompanhe os sintomas."
    ],

    "media": [
        "Esse quadro merece acompanhamento.",
        "É importante observar a evolução.",
        "Não ignore os sinais."
    ],

    "alta": [
        "Procure atendimento médico imediatamente.",
        "A situação exige avaliação urgente.",
        "Não adie a busca por ajuda profissional."
    ]
}


# ======================================
# REGRAS MÉDICAS CRÍTICAS
# ======================================

GATILHOS_INFARTO = [
    "peito", "falta de ar", "pressao",
    "pressão", "braco", "braço", "suor frio"
]


# ======================================
# SCORE DE SINTOMAS
# ======================================

def calcular_score(texto, linha):

    score = 0

    fortes = linha["sintomas_fortes"].split()
    medios = linha["sintomas_medios"].split()
    leves = linha["sintomas_leves"].split()

    for p in fortes:
        if p in texto:
            score += 5

    for p in medios:
        if p in texto:
            score += 3

    for p in leves:
        if p in texto:
            score += 1

    return score


# ======================================
# DIAGNÓSTICO
# ======================================

def diagnosticar(texto: str, nome="Paciente"):

    texto = texto.lower().strip()

    print("🧠 Analisando:", texto)

    melhor_score = 0
    melhor_linha = None


    for _, linha in df.iterrows():

        doenca = linha["doenca"]

        score = calcular_score(texto, linha)


        # 🚫 BLOQUEIO DE INFARTO SEM SINTOMA CARDÍACO
        if doenca == "infarto":

            valido = False

            for g in GATILHOS_INFARTO:
                if g in texto:
                    valido = True
                    break

            if not valido:
                continue


        if score > melhor_score:
            melhor_score = score
            melhor_linha = linha


    # ❌ Nenhum padrão confiável
    if melhor_score < 3:

        mensagem = f"""
{nome}, não foi possível identificar um padrão clínico claro.

Recomendo procurar um profissional de saúde
para avaliação presencial.
"""

        try:
            gerar_audio(mensagem)
        except:
            pass

        return {
            "diagnostico": "Indefinido",
            "gravidade": "desconhecida",
            "especialidade": "Clínico Geral",
            "mensagem": mensagem,
            "audio": "/static/voz.mp3"
        }


    # ===============================
    # RESULTADO
    # ===============================

    doenca = melhor_linha["doenca"].title()
    gravidade = melhor_linha["gravidade"]
    urgencia = melhor_linha["urgencia"]
    especialidade = melhor_linha["especialidade"].title()
    orientacao = melhor_linha["orientacao"]

    frase = random.choice(
        PERSONALIDADE.get(gravidade, PERSONALIDADE["media"])
    )


    mensagem_final = f"""
{nome}, com base nos sintomas informados, há indícios compatíveis com:

{doenca}

Gravidade: {gravidade.upper()}
Urgência: {urgencia.upper()}
Especialidade: {especialidade}

Orientação:
{orientacao}

Observação:
{frase}

Este sistema não substitui avaliação médica presencial.
"""


    try:
        gerar_audio(mensagem_final)
    except Exception as e:
        print("Erro áudio:", e)


    return {
        "diagnostico": doenca,
        "gravidade": gravidade,
        "urgencia": urgencia,
        "especialidade": especialidade,
        "mensagem": mensagem_final,
        "audio": "/static/voz.mp3"
    }
