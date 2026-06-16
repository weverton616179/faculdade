# BIBLIOTECAS
from pathlib import Path
from pickle import dump

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

from imblearn.over_sampling import SMOTE
from pprint import pprint

# Constantes
SEED = 42
TEST_SIZE = 0.2
CV_FOLDS_RF = 3
CV_FOLDS_FINAL = 10
N_ITER_RANDOM_SEARCH = 10

# Diretorio base
BASE_DIR = Path(__file__).resolve().parent

# 1. Carregando os dados
print('\n' + '=' * 60)
print('1. CARREGANDO DADOS')
print('=' * 60)

df = pd.read_csv(BASE_DIR / 'mushroom.csv', sep=';')
print(f'Shape original: {df.shape}')
print(f'Classes (mushroom_type):')
print(df['mushroom_type'].value_counts())

# 2. Dados faltantes na coluna stalk-root
print('\n' + '=' * 60)
print('2. TRATAMENTO DE DADOS FALTANTES (stalk-root)')
print('=' * 60)

missing_count = (df['stalk-root'] == '?').sum()
print(f'Valores "?" em stalk-root: {missing_count} '
      f'({missing_count / len(df) * 100:.2f}%)')
print('Estrategia: Manter "?" como categoria propria (one-hot encoding)')

# 3. Removendo colunas inuteis
print('\n' + '=' * 60)
print('3. COLUNAS NAO-INFORMATIVAS')
print('=' * 60)

# veil-type so tem 'p' o tempo todo — nao agrega nada
cols_to_drop = ['veil-type']
print(f'Colunas removidas (constantes): {cols_to_drop}')
df = df.drop(columns=cols_to_drop)
print(f'Shape apos remocao: {df.shape}')

# 4. Separando features do target
print('\n' + '=' * 60)
print('4. SEPARACAO FEATURES / TARGET')
print('=' * 60)

target_col = 'mushroom_type'
X = df.drop(columns=[target_col])
y = df[target_col]

# Tudo categorico — codigos de letra unica
cat_features = X.columns.tolist()
print(f'Features categoricas ({len(cat_features)}): {cat_features}')
print(f'Target: {target_col}')
print(f'Classes: {y.unique()}')

# 5. Separando treino e teste (com estratificacao)
print('\n' + '=' * 60)
print('5. TRAIN/TEST SPLIT')
print('=' * 60)

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=TEST_SIZE,
    random_state=SEED,
    stratify=y,
)
print(f'Treino: {X_train.shape[0]} amostras')
print(f'Teste : {X_test.shape[0]} amostras')
print(f'Dist. treino:\n{y_train.value_counts()}')
print(f'Dist. teste:\n{y_test.value_counts()}')

# 6. One-hot encoding (tudo categorico, sem scaling)
print('\n' + '=' * 60)
print('6. ONE-HOT ENCODING (todas as features sao categoricas)')
print('=' * 60)

# One-hot em tudo
X_train_enc = pd.get_dummies(
    X_train[cat_features],
    prefix=cat_features,
    dtype=int,
)
X_test_enc = pd.get_dummies(
    X_test[cat_features],
    prefix=cat_features,
    dtype=int,
)

# Garantindo que treino e teste tenham as mesmas colunas
X_train_enc, X_test_enc = X_train_enc.align(
    X_test_enc, join='left', axis=1, fill_value=0,
)

print(f'Features apos one-hot encoding: {X_train_enc.shape[1]}')

# Salvando as colunas pra usar na inferencia depois
cat_columns = X_train_enc.columns.tolist()
dump(cat_columns, open(BASE_DIR / 'cat_columns.pkl', 'wb'))
print(f'Colunas encoded salvas em: cat_columns.pkl ({len(cat_columns)} colunas)')

# 7. Balanceando as classes com SMOTE
print('\n' + '=' * 60)
print('7. BALANCEAMENTO COM SMOTE')
print('=' * 60)

print(f'Distribuicao antes do SMOTE:\n{y_train.value_counts()}')

smote_balancer = SMOTE(random_state=SEED)
X_train_bal, y_train_bal = smote_balancer.fit_resample(
    X_train_enc, y_train,
)

print(f'\nDistribuicao apos SMOTE:\n{y_train_bal.value_counts()}')
print(f'Shape apos balanceamento: {X_train_bal.shape}')

# 8. Procurando os melhores hiperparametros
print('\n' + '=' * 60)
print('8. RANDOMIZED SEARCH CV — HIPERPARAMETROS')
print('=' * 60)

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

print('\nMelhores hiperparametros encontrados:')
pprint(random_search.best_params_)
print(f'\nMelhor score (validation): {random_search.best_score_:.4f}')

# 9. Treinando o modelo final
print('\n' + '=' * 60)
print('9. TREINO DO MODELO FINAL')
print('=' * 60)

tuned_rf = RandomForestClassifier(
    **random_search.best_params_,
    random_state=SEED,
)
tuned_rf.fit(X_train_bal, y_train_bal)
dump(tuned_rf, open(BASE_DIR / 'modelo_rf.pkl', 'wb'))
print('Modelo salvo em: modelo_rf.pkl')

# 10. Validacao cruzada com 10 folds
print('\n' + '=' * 60)
print('10. VALIDACAO CRUZADA (10-FOLD)')
print('=' * 60)

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

print('\nResultados da validacao cruzada:')
for metric in scoring:
    key = f'test_{metric}'
    mean_val = cv_results[key].mean()
    std_val = cv_results[key].std()
    print(f'  {metric:20s}: {mean_val:.4f} (+/- {std_val:.4f})')

# 11. Avaliando no teste
print('\n' + '=' * 60)
print('11. METRICAS NO CONJUNTO DE TESTE')
print('=' * 60)

y_pred = tuned_rf.predict(X_test_enc)
test_accuracy = accuracy_score(y_test, y_pred)
test_f1 = f1_score(y_test, y_pred, average='macro')

print(f'Accuracy (teste): {test_accuracy:.4f}')
print(f'F1-Score  (teste): {test_f1:.4f}')

# 12. Matriz de confusao
print('\n' + '=' * 60)
print('12. MATRIZ DE CONFUSAO')
print('=' * 60)

cm = confusion_matrix(y_test, y_pred)
class_labels = tuned_rf.classes_

print('\nMatriz de Confusao:')
print(cm)

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_labels)
disp.plot(cmap='Blues', values_format='d', xticks_rotation=45)
plt.title('Matriz de Confusao — Random Forest (Mushroom)')
plt.tight_layout()
plt.savefig(BASE_DIR / 'matriz_confusao.png', dpi=300, bbox_inches='tight')
plt.close()
print('Matriz de confusao salva em: matriz_confusao.png')

# 13. Desempenho classe a classe
print('\n' + '=' * 60)
print('13. METRICAS POR CLASSE')
print('=' * 60)

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
    spec_val = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    acc_val = (tp + tn) / cm.sum()
    prec_val = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    f1_val = (
        2 * (prec_val * recall_val) / (prec_val + recall_val)
        if (prec_val + recall_val) > 0 else 0.0
    )

    sensitivity_per_class.append(recall_val)
    specificity_per_class.append(spec_val)
    accuracy_per_class.append(acc_val)
    f1_per_class.append(f1_val)

    print(f'\nClasse: {class_labels[i]}')
    print(f'  Accuracy              : {acc_val:.4f}')
    print(f'  Recall (Sensitivity)  : {recall_val:.4f}')
    print(f'  Specificity           : {spec_val:.4f}')
    print(f'  Precision             : {prec_val:.4f}')
    print(f'  F1-Score              : {f1_val:.4f}')

print('\n--- Metricas Medias (Macro) ---')
print(f'  Avg Sensitivity : {np.mean(sensitivity_per_class):.4f}')
print(f'  Avg Specificity : {np.mean(specificity_per_class):.4f}')
print(f'  Avg Accuracy    : {np.mean(accuracy_per_class):.4f}')
print(f'  Avg F1-Score    : {np.mean(f1_per_class):.4f}')

# 14. Features mais importantes (top 20)
print('\n' + '=' * 60)
print('14. IMPORTANCIA DAS FEATURES (TOP 20)')
print('=' * 60)

importances = tuned_rf.feature_importances_
indices = np.argsort(importances)[::-1]

print('\nTop 20 features mais importantes:')
for rank, idx in enumerate(indices[:20], 1):
    print(f'  {rank:2d}. {X_train_enc.columns[idx]:45s} '
          f'{importances[idx]:.4f}')

print('\n' + '=' * 60)
print('CLASSIFICADOR CONCLUIDO COM SUCESSO!')
print('=' * 60)
