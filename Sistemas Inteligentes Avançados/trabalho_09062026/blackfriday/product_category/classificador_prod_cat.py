# ============================================================
# IMPORTS
# ============================================================
# stdlib
from pathlib import Path
import pickle

# third-party (data & viz)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# third-party (sklearn)
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    f1_score,
)
from sklearn.model_selection import (
    cross_validate,
    RandomizedSearchCV,
    train_test_split,
)
from sklearn.preprocessing import LabelEncoder, StandardScaler

# third-party (imbalanced-learn)
from imblearn.over_sampling import SMOTE

# stdlib (pretty-print)
from pprint import pprint

# ============================================================
# CONSTANTS
# ============================================================
SEED = 42
TEST_SIZE = 0.2
CV_FOLDS_RF = 3
CV_FOLDS_FINAL = 10
N_ITER_RANDOM_SEARCH = 10

# ============================================================
# 0. Path configuration
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent  # blackfriday/
MODEL_DIR = Path(__file__).resolve().parent        # blackfriday/product_category/

# ============================================================
# 1. Leitura da base de dados
# ============================================================
df = pd.read_csv(BASE_DIR / 'retail_black_friday_sales_100k.csv')

# ============================================================
# 2. Exclusão de colunas não-generalizáveis
# ============================================================
cols_to_drop = [
    'transaction_id', 'customer_id', 'product_id',
    'purchase_date', 'purchase_hour',
]
df = df.drop(columns=cols_to_drop)

# ============================================================
# 3. Classificação das features por tipo e definição do target
# ============================================================
num_features = [
    'original_price', 'discount_pct', 'final_price', 'quantity',
    'purchase_amount', 'is_weekend', 'is_black_friday',
]

ordinal_features = ['age_group']

nominal_features = [
    'gender', 'city', 'customer_segment', 'payment_method',
]

target_col = 'product_category'

# ============================================================
# 4. Separação treino/teste
# ============================================================
X = df.drop(columns=[target_col])
y = df[target_col]
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=TEST_SIZE,
    random_state=SEED,
)

# ============================================================
# 5. Pré-processamento & encoding
# ============================================================
# --- numéricas: padronização (z-score) ---
std_scaler = StandardScaler()
X_train_num_scaled = pd.DataFrame(
    std_scaler.fit_transform(X_train[num_features]),
    columns=num_features,
    index=X_train.index,
)
X_test_num_scaled = pd.DataFrame(
    std_scaler.transform(X_test[num_features]),
    columns=num_features,
    index=X_test.index,
)
pickle.dump(std_scaler, open(MODEL_DIR / 'normalizador_num.pkl', 'wb'))

# --- categóricas ordinais: label encoding ---
ordinal_encoders = {}
X_train_ord_enc = X_train[ordinal_features].copy()
X_test_ord_enc  = X_test[ordinal_features].copy()

for col in ordinal_features:
    encoder = LabelEncoder()
    X_train_ord_enc[col] = encoder.fit_transform(X_train[col])
    X_test_ord_enc[col]  = encoder.transform(X_test[col])
    ordinal_encoders[col] = encoder
pickle.dump(ordinal_encoders, open(MODEL_DIR / 'normalizador_cat_ord.pkl', 'wb'))

# --- categóricas nominais: one-hot encoding ---
X_train_nom_enc = pd.get_dummies(
    X_train[nominal_features],
    prefix=nominal_features,
    dtype=int,
)
X_test_nom_enc = pd.get_dummies(
    X_test[nominal_features],
    prefix=nominal_features,
    dtype=int,
)

X_train_nom_enc, X_test_nom_enc = X_train_nom_enc.align(
    X_test_nom_enc, join='left', axis=1, fill_value=0,
)
pickle.dump(
    X_train_nom_enc.columns.to_list(),
    open(MODEL_DIR / 'normalizador_cat_nom.pkl', 'wb'),
)

# --- concatenação dos blocos ---
X_train_processed = pd.concat(
    [X_train_num_scaled, X_train_ord_enc, X_train_nom_enc], axis=1,
)
X_test_processed = pd.concat(
    [X_test_num_scaled, X_test_ord_enc, X_test_nom_enc], axis=1,
)

# ============================================================
# 6. Balanceamento com SMOTE
# ============================================================
smote_balancer = SMOTE(random_state=SEED)
X_train_bal, y_train_bal = smote_balancer.fit_resample(
    X_train_processed, y_train,
)

# ============================================================
# 7. Busca de hiperparâmetros (RandomizedSearchCV)
# ============================================================
param_grid = {
    'n_estimators': [int(x) for x in np.linspace(10, 100, 10)],
    'criterion': ['gini', 'entropy'],
    'min_samples_split': [int(x) for x in np.linspace(2, 20, 10)],
    'max_depth': [int(x) for x in np.linspace(10, 100, 20)],
    'max_features': ['sqrt', 'log2'],
}

base_rf = RandomForestClassifier(random_state=SEED)
random_search = RandomizedSearchCV(
    estimator=base_rf,
    param_distributions=param_grid,
    n_iter=N_ITER_RANDOM_SEARCH,
    cv=CV_FOLDS_RF,
    verbose=2,
    n_jobs=-1,
    random_state=SEED,
)
random_search.fit(X_train_bal, y_train_bal)

print('\nBest hyperparameters found:')
pprint(random_search.best_params_)

# ============================================================
# 8. Treino do modelo final
# ============================================================
tuned_rf = RandomForestClassifier(
    **random_search.best_params_,
    random_state=SEED,
)
tuned_rf.fit(X_train_bal, y_train_bal)
pickle.dump(tuned_rf, open(MODEL_DIR / 'modelo_rf.pkl', 'wb'))

# ============================================================
# 9. Validação cruzada (10-fold)
# ============================================================
scoring = ['accuracy', 'f1_macro', 'precision_macro', 'recall_macro']
cv_results = cross_validate(
    tuned_rf,
    X_train_bal,
    y_train_bal,
    scoring=scoring,
    n_jobs=-1,
    cv=CV_FOLDS_FINAL,
    verbose=1,
)

print('\nCross-validation scores:', cv_results)
print('\nMean Accuracy :', cv_results['test_accuracy'].mean())
print('Mean Precision:', cv_results['test_precision_macro'].mean())
print('Mean Recall   :', cv_results['test_recall_macro'].mean())
print('Mean F1-Score :', cv_results['test_f1_macro'].mean())

# ============================================================
# 10. Métricas no conjunto de teste
# ============================================================
y_pred = tuned_rf.predict(X_test_processed)
test_accuracy = accuracy_score(y_test, y_pred)
test_f1 = f1_score(y_test, y_pred, average='macro')

print(f'\nTest Set Accuracy : {test_accuracy:.4f}')
print(f'Test Set F1 (macro): {test_f1:.4f}')

# ============================================================
# 11. Matriz de confusão
# ============================================================
cm = confusion_matrix(y_test, y_pred)
class_labels = tuned_rf.classes_

print('\nConfusion Matrix:')
print(cm)

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_labels)
disp.plot(cmap='Blues', values_format='d', xticks_rotation=45)
plt.title('Confusion Matrix – Random Forest')
plt.tight_layout()
plt.savefig(MODEL_DIR / 'matriz_confusao.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# 12. Métricas detalhadas por classe
# ============================================================
n_classes = len(class_labels)
sensitivity_per_class = []
specificity_per_class = []
accuracy_per_class = []
f1_per_class = []

for i in range(n_classes):
    tp = cm[i, i]
    fn = cm[i, :].sum() - tp
    fp = cm[:, i].sum() - tp
    tn = cm.sum() - (tp + fn + fp)

    recall_val = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    spec_val   = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    acc_val    = (tp + tn) / cm.sum()
    prec_val   = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    f1_val     = (
        2 * (prec_val * recall_val) / (prec_val + recall_val)
        if (prec_val + recall_val) > 0 else 0.0
    )

    sensitivity_per_class.append(recall_val)
    specificity_per_class.append(spec_val)
    accuracy_per_class.append(acc_val)
    f1_per_class.append(f1_val)

    print(f'\nClass: {class_labels[i]}')
    print(f'  Accuracy        : {acc_val:.4f}')
    print(f'  Recall (Sensitivity): {recall_val:.4f}')
    print(f'  Specificity     : {spec_val:.4f}')
    print(f'  Precision       : {prec_val:.4f}')
    print(f'  F1-Score        : {f1_val:.4f}')

print('\nOverall Macro-Averaged Metrics:')
print(f'  Avg Sensitivity : {np.mean(sensitivity_per_class):.4f}')
print(f'  Avg Specificity : {np.mean(specificity_per_class):.4f}')
print(f'  Avg Accuracy    : {np.mean(accuracy_per_class):.4f}')
print(f'  Avg F1-Score    : {np.mean(f1_per_class):.4f}')
