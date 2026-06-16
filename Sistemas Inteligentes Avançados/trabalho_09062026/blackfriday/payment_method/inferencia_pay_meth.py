# ============================================================
# IMPORTS
# ============================================================
# stdlib
from pathlib import Path
from pickle import load

# third-party
import numpy as np
import pandas as pd

# ============================================================
# 1. Dados de entrada para predição
# ============================================================
FEATURE_NAMES = [
    'original_price', 'discount_pct', 'final_price', 'quantity',
    'purchase_amount', 'is_weekend', 'is_black_friday',
    'age_group',
    'gender', 'city', 'customer_segment', 'product_category',
]

new_samples = [[
    153.73,            # original_price
    35,                # discount_pct
    99.92,             # final_price
    1,                 # quantity
    99.92,             # purchase_amount
    0,                 # is_weekend
    0,                 # is_black_friday
    '26-35',           # age_group (ordinal)
    'Male',            # gender (nominal)
    'San Francisco',   # city (nominal)
    'Loyal',           # customer_segment (nominal)
    'Footwear',        # product_category (nominal)
]]

input_df = pd.DataFrame(new_samples, columns=FEATURE_NAMES)

# ============================================================
# 2. Carregamento dos artefatos salvos
# ============================================================
MODEL_DIR = Path(__file__).resolve().parent

num_features = [
    'original_price', 'discount_pct', 'final_price', 'quantity',
    'purchase_amount', 'is_weekend', 'is_black_friday',
]
ordinal_features = ['age_group']
nominal_features = [
    'gender', 'city', 'customer_segment', 'product_category',
]

scaler_loaded = load(open(MODEL_DIR / 'normalizador_num.pkl', 'rb'))
ord_encoders_loaded = load(open(MODEL_DIR / 'normalizador_cat_ord.pkl', 'rb'))
nom_columns_loaded = load(open(MODEL_DIR / 'normalizador_cat_nom.pkl', 'rb'))
model = load(open(MODEL_DIR / 'modelo_rf.pkl', 'rb'))

# ============================================================
# 3. Pré-processamento
# ============================================================
# --- numéricas: padronização ---
num_scaled = pd.DataFrame(
    scaler_loaded.transform(input_df[num_features]),
    columns=num_features,
    index=input_df.index,
)

# --- categóricas ordinais: label encoding ---
ord_encoded = input_df[ordinal_features].copy()
for col in ordinal_features:
    encoder = ord_encoders_loaded[col]
    ord_encoded[col] = encoder.transform(input_df[col])

# --- categóricas nominais: one-hot + alinhamento ---
nom_encoded = pd.get_dummies(
    input_df[nominal_features],
    prefix=nominal_features,
    dtype=int,
)

nom_aligned = pd.DataFrame(
    0, index=input_df.index, columns=nom_columns_loaded,
)
for col in nom_columns_loaded:
    if col in nom_encoded.columns:
        nom_aligned[col] = nom_encoded[col]

# --- concatenação ---
features_final = pd.concat(
    [num_scaled, ord_encoded, nom_aligned], axis=1,
)

# ============================================================
# 4. Predição
# ============================================================
prediction = model.predict(features_final)

print('\n--- PREDICTION RESULT ---')
print(f'Predicted class: {prediction[0]}')
print('\nKnown classes:')
print(model.classes_)
print('\nClass probabilities:')
print(model.predict_proba(features_final))