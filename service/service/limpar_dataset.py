import pandas as pd
import os


# ===============================
# Caminhos
# ===============================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

INPUT = os.path.join(BASE_DIR, "dados", "dataset_diagnostico_medico.csv")
OUTPUT = os.path.join(BASE_DIR, "dados", "dataset_ml.csv")


# ===============================
# Main
# ===============================

def main():

    print("📥 Lendo dataset bruto...")

    if not os.path.exists(INPUT):
        print("❌ Arquivo não encontrado:", INPUT)
        return

    df = pd.read_csv(INPUT)

    print("📊 Colunas encontradas:")
    print(list(df.columns))


    # ===============================
    # Seleção correta
    # ===============================

    print("✂️ Selecionando colunas certas...")

    COLUNAS_NECESSARIAS = [
        "sintomas_relatados",
        "diagnostico_final"
    ]

    for col in COLUNAS_NECESSARIAS:
        if col not in df.columns:
            print(f"❌ Coluna ausente: {col}")
            return


    df_ml = df[COLUNAS_NECESSARIAS].copy()

    df_ml.columns = ["texto", "diagnostico"]


    # ===============================
    # Limpeza
    # ===============================

    print("✨ Limpando texto...")

    df_ml["texto"] = df_ml["texto"].astype(str)

    df_ml["texto"] = (
        df_ml["texto"]
        .str.lower()
        .str.replace(";", " ", regex=False)
        .str.replace(",", " ", regex=False)
        .str.replace(".", " ", regex=False)
        .str.replace("  ", " ", regex=False)
    )

    df_ml["diagnostico"] = df_ml["diagnostico"].astype(str)

    df_ml.dropna(inplace=True)

    df_ml = df_ml.reset_index(drop=True)


    # ===============================
    # Salvar
    # ===============================

    print("💾 Salvando dataset ML...")

    df_ml.to_csv(OUTPUT, index=False, encoding="utf-8")

    print("\n✅ Dataset criado com sucesso!")
    print("📂 Arquivo:", OUTPUT)
    print("📈 Registros:", len(df_ml))


# ===============================
# Start
# ===============================

if __name__ == "__main__":
    main()
