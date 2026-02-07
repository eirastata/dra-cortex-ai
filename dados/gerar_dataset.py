import csv
import random

# ================================
# CONFIG
# ================================

ARQUIVO_SAIDA = "dados/dataset_medico_v3.csv"
LINHAS_POR_DOENCA = 15   # quanto maior, melhor o modelo


# ================================
# BASE DE DOENÇAS
# ================================

DOENCAS = {

    "Infarto": {
        "sintomas": ["dor no peito", "falta de ar", "suor frio", "nausea", "dor no braço", "tontura"],
        "gravidade": "alta",
        "urgencia": "sim",
        "especialidade": "Cardiologia",
        "orientacao": "Procure emergência imediatamente"
    },

    "Otite": {
        "sintomas": ["dor no ouvido", "ouvido tampado", "coceira", "secrecao", "febre leve"],
        "gravidade": "media",
        "urgencia": "nao",
        "especialidade": "Otorrino",
        "orientacao": "Procure um otorrinolaringologista"
    },

    "Pneumonia": {
        "sintomas": ["tosse", "falta de ar", "febre alta", "dor no peito", "cansaco"],
        "gravidade": "alta",
        "urgencia": "sim",
        "especialidade": "Pneumologia",
        "orientacao": "Procure atendimento médico urgente"
    },

    "Gripe": {
        "sintomas": ["febre", "dor no corpo", "tosse", "coriza", "fraqueza"],
        "gravidade": "baixa",
        "urgencia": "nao",
        "especialidade": "Clinico Geral",
        "orientacao": "Repouso e hidratação"
    },

    "Covid-19": {
        "sintomas": ["febre", "tosse seca", "perda de olfato", "falta de ar", "dor no corpo"],
        "gravidade": "media",
        "urgencia": "sim",
        "especialidade": "Pneumologia",
        "orientacao": "Isolamento e avaliação médica"
    },

    "Sinusite": {
        "sintomas": ["dor facial", "nariz entupido", "secrecao nasal", "dor de cabeca", "pressao no rosto"],
        "gravidade": "media",
        "urgencia": "nao",
        "especialidade": "Otorrino",
        "orientacao": "Consultar especialista"
    },

    "Rinite": {
        "sintomas": ["espirros", "coriza", "coceira no nariz", "nariz entupido"],
        "gravidade": "baixa",
        "urgencia": "nao",
        "especialidade": "Alergologia",
        "orientacao": "Evitar alergenos"
    },

    "Enxaqueca": {
        "sintomas": ["dor de cabeca forte", "fotofobia", "nausea", "tontura"],
        "gravidade": "media",
        "urgencia": "nao",
        "especialidade": "Neurologia",
        "orientacao": "Repouso e medicação"
    },

    "Depressao": {
        "sintomas": ["tristeza", "falta de energia", "desanimo", "insônia", "isolamento"],
        "gravidade": "alta",
        "urgencia": "nao",
        "especialidade": "Psiquiatria",
        "orientacao": "Procurar acompanhamento psicológico"
    },

    "Ansiedade": {
        "sintomas": ["palpitacao", "nervosismo", "falta de ar", "medo", "sudorese"],
        "gravidade": "media",
        "urgencia": "nao",
        "especialidade": "Psicologia",
        "orientacao": "Terapia e acompanhamento"
    },

    "Diabetes": {
        "sintomas": ["sede excessiva", "urinar muito", "fome excessiva", "fraqueza", "visao turva"],
        "gravidade": "alta",
        "urgencia": "nao",
        "especialidade": "Endocrinologia",
        "orientacao": "Controle glicêmico"
    },

    "Hipertensao": {
        "sintomas": ["dor de cabeca", "tontura", "palpitacao", "visao borrada"],
        "gravidade": "media",
        "urgencia": "nao",
        "especialidade": "Cardiologia",
        "orientacao": "Controle da pressão"
    },

    "Gastrite": {
        "sintomas": ["dor no estomago", "azia", "queimacao", "nausea", "estufamento"],
        "gravidade": "media",
        "urgencia": "nao",
        "especialidade": "Gastroenterologia",
        "orientacao": "Ajuste alimentar"
    },

    "Refluxo": {
        "sintomas": ["azia", "queimacao", "regurgitacao", "tosse", "rouquidao"],
        "gravidade": "media",
        "urgencia": "nao",
        "especialidade": "Gastroenterologia",
        "orientacao": "Mudança alimentar"
    },

    "ITU": {
        "sintomas": ["ardor ao urinar", "urina turva", "dor abdominal", "urgencia urinaria"],
        "gravidade": "media",
        "urgencia": "nao",
        "especialidade": "Urologia",
        "orientacao": "Uso de antibiótico"
    },

    "Calculo Renal": {
        "sintomas": ["dor lombar forte", "nausea", "vomito", "urina com sangue"],
        "gravidade": "alta",
        "urgencia": "sim",
        "especialidade": "Urologia",
        "orientacao": "Emergência médica"
    }
}


# ================================
# GERADOR DE TEXTO
# ================================

def gerar_texto(sintomas):
    qtd = random.randint(2, min(5, len(sintomas)))
    escolhidos = random.sample(sintomas, qtd)

    modelos = [
        "Estou com {}",
        "Tenho sentido {}",
        "Apresento {}",
        "Sinto {} há dias",
        "Ando com {} recentemente",
        "Venho apresentando {}"
    ]

    frase = random.choice(modelos)
    return frase.format(", ".join(escolhidos))


# ================================
# MAIN
# ================================

linhas = []

for doenca, dados in DOENCAS.items():

    sintomas = dados["sintomas"]

    for _ in range(LINHAS_POR_DOENCA):

        texto = gerar_texto(sintomas)

        linhas.append([
            doenca,
            texto,
            dados["gravidade"],
            dados["urgencia"],
            dados["especialidade"],
            dados["orientacao"]
        ])


# ================================
# SALVAR CSV
# ================================

with open(ARQUIVO_SAIDA, "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "doenca",
        "texto",
        "gravidade",
        "urgencia",
        "especialidade",
        "orientacao"
    ])

    writer.writerows(linhas)


print("✅ Dataset criado!")
print("📊 Total linhas:", len(linhas))
print("📁 Arquivo:", ARQUIVO_SAIDA)
