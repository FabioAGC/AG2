"""
Classificação de Espécies de Pinguins
Projeto AG2 – Inatel
"""

import warnings

import pandas as pd
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

warnings.filterwarnings("ignore")

# Passo 1: Baixar o dataset
URL = "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/master/inst/extdata/penguins.csv"
df = pd.read_csv(URL)

# Passo 2: Pré-processamento
df = df.drop(columns=["year"]).dropna()
df = df.rename(columns={"bill_length_mm": "culmen_length_mm", "bill_depth_mm": "culmen_depth_mm"})

island_mapping = {"Biscoe": 0, "Dream": 1, "Torgersen": 2}
sex_mapping = {"FEMALE": 0, "MALE": 1}
species_mapping = {"Adelie": 0, "Chinstrap": 1, "Gentoo": 2}

df["island"] = df["island"].replace(island_mapping).astype(int)
df["sex"] = df["sex"].str.upper().replace(sex_mapping).astype(int)
df["species"] = df["species"].replace(species_mapping).astype(int)

df = df.reindex(columns=["island", "sex", "culmen_length_mm", "culmen_depth_mm", "flipper_length_mm", "body_mass_g", "species"])

# Passo 3: Divisão treino/teste (80/20)
X = df.drop("species", axis=1)
y = df["species"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Passo 4: Pipeline SVM com GridSearchCV
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", SVC(random_state=42, probability=True)),
])

param_grid = {
    "clf__C": [0.1, 1, 10, 100],
    "clf__kernel": ["rbf", "poly", "linear"],
    "clf__gamma": ["scale", "auto"],
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
grid = GridSearchCV(pipe, param_grid, cv=cv, scoring="accuracy", n_jobs=-1, refit=True)

# Passo 5: Treinar e avaliar o modelo
grid.fit(X_train, y_train)
model = grid.best_estimator_
y_pred = model.predict(X_test)

print("=" * 55)
print("  SVM – Classificador de Espécies de Pinguins")
print("=" * 55)
print(f"Melhores parâmetros : {grid.best_params_}")
print(f"Acurácia (CV)       : {grid.best_score_:.4f}")
print(f"Acurácia (teste)    : {(y_pred == y_test).mean():.4f}")
print()
print("Relatório de Classificação (conjunto de teste):")
print(classification_report(y_test, y_pred, target_names=["Adelie", "Chinstrap", "Gentoo"]))


# Passo 6: Classificação interativa
def classificar_pinguim():
    print("\n--- Classificar Novo Pinguim ---")
    try:
        ilha = int(input("Ilha          (0: Biscoe | 1: Dream | 2: Torgersen): "))
        sexo = int(input("Sexo          (0: Fêmea  | 1: Macho)               : "))
        comp_culmen = float(input("Comprimento do cúlmen (mm)                         : "))
        prof_culmen = float(input("Profundidade do cúlmen (mm)                        : "))
        comp_nadadeira = float(input("Comprimento da nadadeira (mm)                      : "))
        massa = float(input("Massa corporal (g)                                 : "))

        entrada = pd.DataFrame(
            [[ilha, sexo, comp_culmen, prof_culmen, comp_nadadeira, massa]],
            columns=X.columns,
        )

        codigo = model.predict(entrada)[0]
        especie = {v: k for k, v in species_mapping.items()}[codigo]
        print(f"\n  Espécie prevista: {especie}")

    except ValueError:
        print("Entrada inválida. Por favor, insira valores numéricos conforme solicitado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


if __name__ == "__main__":
    while True:
        classificar_pinguim()
        novamente = input("\nClassificar outro pinguim? (s/n): ").strip().lower()
        if novamente != "s":
            break
    print("Falou , valeu!")
