# AG2 – Classificação de Espécies de Pinguins

Projeto desenvolvido para a **Avaliação Global 2 (AG2)** – Inatel.

## Descrição

Este projeto implementa um classificador de espécies de pinguins utilizando **Support Vector Machine (SVM)** com otimização de hiperparâmetros via **GridSearchCV**. O dataset utilizado é o [Palmer Penguins](https://github.com/allisonhorst/palmerpenguins), que contém medições físicas de pinguins de três espécies coletadas nas Ilhas Palmer, na Antártida.

## Dataset

O dataset é carregado diretamente do repositório público e contém as seguintes colunas:

| Coluna | Descrição |
|---|---|
| `species` | Espécie do pinguim (Adelie, Chinstrap, Gentoo) |
| `island` | Ilha de origem (Biscoe, Dream, Torgersen) |
| `culmen_length_mm` | Comprimento do cúlmen (mm) |
| `culmen_depth_mm` | Profundidade do cúlmen (mm) |
| `flipper_length_mm` | Comprimento da nadadeira (mm) |
| `body_mass_g` | Massa corporal (g) |
| `sex` | Sexo do pinguim (MALE, FEMALE) |

## Como funciona

### 1. Pré-processamento
- Remoção da coluna `year` e linhas com valores nulos
- Codificação das variáveis categóricas:
  - Ilha: Biscoe → 0, Dream → 1, Torgersen → 2
  - Sexo: Fêmea → 0, Macho → 1
  - Espécie: Adelie → 0, Chinstrap → 1, Gentoo → 2

### 2. Divisão dos dados
- 80% para treino e 20% para teste
- Divisão estratificada para manter a proporção das classes

### 3. Pipeline de classificação
- **StandardScaler**: normaliza as features antes do treinamento
- **SVC**: classificador SVM com busca pelos melhores hiperparâmetros

### 4. Otimização de hiperparâmetros (GridSearchCV)
Os seguintes parâmetros são testados via validação cruzada estratificada com 5 folds:

| Parâmetro | Valores testados |
|---|---|
| `C` | 0.1, 1, 10, 100 |
| `kernel` | rbf, poly, linear |
| `gamma` | scale, auto |

### 5. Avaliação
O modelo exibe:
- Melhores hiperparâmetros encontrados
- Acurácia média na validação cruzada
- Acurácia no conjunto de teste
- Relatório completo de classificação (precisão, recall, F1-score por espécie)

### 6. Classificação interativa
Após o treinamento, o programa permite classificar novos pinguins interativamente. O usuário informa as medições físicas e o modelo retorna a espécie prevista.

## Requisitos

```
pandas
scikit-learn
```

Instale as dependências com:

```bash
pip install pandas scikit-learn
```

## Como executar

```bash
python penguim.py
```

## Estrutura do projeto

```
AG2_143/
├── penguim.py               # Código principal
├── AG2_1Sem26_GEC_GES.pdf   # Enunciado da avaliação
└── README.md                # Este arquivo
```
