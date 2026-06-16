# BIBLIOTECAS
from pathlib import Path
from pickle import load

import pandas as pd

# Constantes
CLASS_MAP = {
    'e': 'Edible (Comestivel)',
    'p': 'Poisonous (Venenoso)',
}

# Diretorio base
MODEL_DIR = Path(__file__).resolve().parent

# 1. Novos cogumelos pra classificar
FEATURE_NAMES = [
    'cap-shape', 'cap-surface', 'cap-color', 'bruises',
    'odor', 'gill-attachment', 'gill-spacing', 'gill-size',
    'gill-color', 'stalk-shape', 'stalk-root',
    'stalk-surface-above-ring', 'stalk-surface-below-ring',
    'stalk-color-above-ring', 'stalk-color-below-ring',
    'veil-color', 'ring-number', 'ring-type',
    'spore-print-color', 'population', 'habitat',
]

# Amostra 1: odor pungente — forte indicio de venenoso
# Amostra 2: odor de amendoa — forte indicio de comestivel
# Amostra 3: sem odor marcante + stalk-root desconhecido (?)
new_samples = [
    # Amostra 1 — Venenoso esperado (odor=p = pungent)
    [
        'x',  # cap-shape: convex
        's',  # cap-surface: smooth
        'n',  # cap-color: brown
        't',  # bruises: true
        'p',  # odor: pungent ← FORTE INDICADOR DE VENENOSO
        'f',  # gill-attachment: free
        'c',  # gill-spacing: close
        'n',  # gill-size: narrow
        'k',  # gill-color: black
        'e',  # stalk-shape: enlarging
        'e',  # stalk-root: equal
        's',  # stalk-surface-above-ring: smooth
        's',  # stalk-surface-below-ring: smooth
        'w',  # stalk-color-above-ring: white
        'w',  # stalk-color-below-ring: white
        'w',  # veil-color: white
        'o',  # ring-number: one
        'p',  # ring-type: pendant
        'k',  # spore-print-color: black
        's',  # population: scattered
        'u',  # habitat: urban
    ],
    # Amostra 2 — Comestivel esperado (odor=a = almond)
    [
        'x',  # cap-shape: convex
        's',  # cap-surface: smooth
        'y',  # cap-color: yellow
        't',  # bruises: true
        'a',  # odor: almond ← FORTE INDICADOR DE COMESTIVEL
        'f',  # gill-attachment: free
        'c',  # gill-spacing: close
        'b',  # gill-size: broad
        'k',  # gill-color: black
        'e',  # stalk-shape: enlarging
        'c',  # stalk-root: club
        's',  # stalk-surface-above-ring: smooth
        's',  # stalk-surface-below-ring: smooth
        'w',  # stalk-color-above-ring: white
        'w',  # stalk-color-below-ring: white
        'w',  # veil-color: white
        'o',  # ring-number: one
        'p',  # ring-type: pendant
        'n',  # spore-print-color: brown
        'n',  # population: numerous
        'g',  # habitat: grasses
    ],
    # Amostra 3 — Dado faltante em stalk-root (?), sem odor marcante
    [
        'f',  # cap-shape: flat
        'y',  # cap-surface: scaly
        'w',  # cap-color: white
        't',  # bruises: true
        'n',  # odor: none ← SEM ODOR MARCANTE
        'f',  # gill-attachment: free
        'c',  # gill-spacing: close
        'b',  # gill-size: broad
        'p',  # gill-color: pink
        't',  # stalk-shape: tapering
        '?',  # stalk-root: DESCONHECIDO ← MESMO PADRAO DO DATASET
        's',  # stalk-surface-above-ring: smooth
        's',  # stalk-surface-below-ring: smooth
        'w',  # stalk-color-above-ring: white
        'w',  # stalk-color-below-ring: white
        'w',  # veil-color: white
        'o',  # ring-number: one
        'e',  # ring-type: evanescent
        'w',  # spore-print-color: white
        'v',  # population: several
        'd',  # habitat: woods
    ],
    # Amostra 4 — Odor de creosoto (venenoso) + stalk-root bulbous
    [
        'x',  # cap-shape: convex
        'f',  # cap-surface: fibrous
        'w',  # cap-color: white
        'f',  # bruises: false
        'c',  # odor: creosote ← INDICADOR DE VENENOSO
        'f',  # gill-attachment: free
        'w',  # gill-spacing: crowded
        'n',  # gill-size: narrow
        'w',  # gill-color: white
        'e',  # stalk-shape: enlarging
        'b',  # stalk-root: bulbous
        's',  # stalk-surface-above-ring: smooth
        's',  # stalk-surface-below-ring: smooth
        'w',  # stalk-color-above-ring: white
        'w',  # stalk-color-below-ring: white
        'w',  # veil-color: white
        'o',  # ring-number: one
        'p',  # ring-type: pendant
        'w',  # spore-print-color: white
        'c',  # population: clustered
        'p',  # habitat: pastures
    ],
]

input_df = pd.DataFrame(new_samples, columns=FEATURE_NAMES)

print('\n' + '=' * 60)
print('AMOSTRAS PARA PREDICAO')
print('=' * 60)
print(input_df.to_string())

# 2. Carregando modelo e colunas salvas
print('\n' + '=' * 60)
print('CARREGANDO ARTEFATOS')
print('=' * 60)

cat_columns_loaded = load(open(MODEL_DIR / 'cat_columns.pkl', 'rb'))
model = load(open(MODEL_DIR / 'modelo_rf.pkl', 'rb'))

print(f'Colunas encoded carregadas: {len(cat_columns_loaded)}')
print(f'Modelo carregado: {type(model).__name__}')
print(f'Classes do modelo: {model.classes_}')

# 3. Pre-processamento
print('\n' + '=' * 60)
print('PRE-PROCESSAMENTO')
print('=' * 60)

# veil-type ja foi removida no treino — nao precisa fazer nada aqui

# One-hot encoding
input_encoded = pd.get_dummies(
    input_df[FEATURE_NAMES],
    prefix=FEATURE_NAMES,
    dtype=int,
)

print(f'Features apos one-hot: {input_encoded.shape[1]}')

# Garantindo que as colunas batem com as do treino
input_aligned = pd.DataFrame(
    0, index=input_df.index, columns=cat_columns_loaded,
)
for col in cat_columns_loaded:
    if col in input_encoded.columns:
        input_aligned[col] = input_encoded[col]

missing_cols = set(cat_columns_loaded) - set(input_encoded.columns)
extra_cols = set(input_encoded.columns) - set(cat_columns_loaded)
print(f'Colunas preenchidas com 0 (nao presentes na amostra): {len(missing_cols)}')
print(f'Colunas extras ignoradas (nao vistas no treino): {len(extra_cols)}')

# 4. Classificando
print('\n' + '=' * 60)
print('RESULTADOS DA PREDICAO')
print('=' * 60)

predictions = model.predict(input_aligned)
probabilities = model.predict_proba(input_aligned)

for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
    class_name = CLASS_MAP[pred]
    prob_dict = dict(zip(model.classes_, prob))

    print(f'\n--- Amostra {i + 1} ---')
    print(f'  Predicao: {pred} ({class_name})')
    print(f'  Confianca:')
    for cls, pct in prob_dict.items():
        bar = '█' * int(pct * 40) + '░' * (40 - int(pct * 40))
        print(f'    {cls} ({CLASS_MAP[cls]}): {pct:.4f}  {bar}')

print('\n' + '=' * 60)
print('INFERENCIA CONCLUIDA!')
print('=' * 60)
