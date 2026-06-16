# IMPORTS
import pandas as pd 
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pickle
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, cross_validate
from pprint import pprint
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# 0. Configuração de Caminhos
BASE_DIR = Path(__file__).resolve().parent.parent  # blackfriday/
MODEL_DIR = Path(__file__).resolve().parent        # blackfriday/payment_method/

# 1. Carregar Dataset
dados = pd.read_csv(BASE_DIR / 'retail_black_friday_sales_100k.csv')
#print(dados.head(5))

# 2. Remover Variáveis Não Genéricas + Que Podem Causar Ruído
dados_remov = ['transaction_id', 'customer_id', 'product_id', 'purchase_date', 'purchase_hour']
dados = dados.drop(columns=dados_remov)
#print(dados.columns)

# 3. Separar Atributos Numéricos dos Categóricos e Definir Variável Alvo
# dados numéricos
dados_num = ['original_price', 'discount_pct', 'final_price', 'quantity', 
             'purchase_amount', 'is_weekend', 'is_black_friday']
# dados categóricos ordinais
dados_cat_ord = ['age_group']
# dados categóricos nominais
dados_cat_nom = ['gender', 'city', 'customer_segment', 'product_category']
# variável alvo (Y)
dado_alvo = 'payment_method'

# 4. Separar Atributos (X) e Target (Y)
X = dados.drop(columns=[dado_alvo])
y = dados[dado_alvo]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Normalização 
# numérica
scaler = StandardScaler()
X_train_num = pd.DataFrame(scaler.fit_transform(X_train[dados_num]), columns=dados_num, index=X_train.index)
X_test_num = pd.DataFrame(scaler.transform(X_test[dados_num]), columns=dados_num, index=X_test.index)
pickle.dump(scaler, open(MODEL_DIR / 'normalizador_num.pkl', 'wb'))

# categórico ordinal 
dict_encoders = {}
X_train_ord = X_train[dados_cat_ord].copy()
X_test_ord = X_test[dados_cat_ord].copy()

for col in dados_cat_ord:
    encoder = LabelEncoder()
    X_train_ord[col] = encoder.fit_transform(X_train[col])
    X_test_ord[col] = encoder.transform(X_test[col])
    dict_encoders[col] = encoder
pickle.dump(dict_encoders, open(MODEL_DIR / 'normalizador_cat_ord.pkl', 'wb'))

# categóricos nominais
X_train_nom = pd.get_dummies(X_train[dados_cat_nom], prefix=dados_cat_nom, dtype=int)
X_test_nom = pd.get_dummies(X_test[dados_cat_nom], prefix=dados_cat_nom, dtype=int)

X_train_nom, X_test_nom = X_train_nom.align(X_test_nom, join='left', axis=1, fill_value=0)
pickle.dump(X_train_nom.columns.to_list(), open(MODEL_DIR / 'normalizador_cat_nom.pkl', 'wb'))

# concatenação
X_train_final = pd.concat([X_train_num, X_train_ord, X_train_nom], axis=1)
X_test_final = pd.concat([X_test_num, X_test_ord, X_test_nom], axis=1)

# 6. Balanceamento 
balancer = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = balancer.fit_resample(X_train_final, y_train)
#print(Counter(y_train_resampled))

# 7. Hiperparametrização
rf_grid = {
    'n_estimators': [int(x) for x in np.linspace(start=10, stop=100, num=10)],
    'criterion': ['gini', 'entropy'],
    'min_samples_split': [int(x) for x in np.linspace(start=2, stop=20, num=10)],
    'max_depth': [int(x) for x in np.linspace(start=10, stop=100, num=20)],
    'max_features': ['sqrt', 'log2']
}
rf = RandomForestClassifier(random_state=42)
rf_hyperparameters = RandomizedSearchCV(
    estimator=rf,
    param_distributions=rf_grid,
    n_iter=10,
    cv=3,
    verbose=2,
    n_jobs=-1,
    random_state=42
)
rf_hyperparameters.fit(X_train_resampled, y_train_resampled)
print("\nMelhores Parâmetros:")
pprint(rf_hyperparameters.best_params_)

# 8. Treinamento
best_rf = RandomForestClassifier(**rf_hyperparameters.best_params_, random_state=42)
best_rf.fit(X_train_resampled, y_train_resampled)
pickle.dump(best_rf, open(MODEL_DIR / 'modelo_rf.pkl', 'wb'))

# 9. Cross-Validation
scoring = ['accuracy', 'f1_macro', 'precision_macro', 'recall_macro']
scores_cross = cross_validate(
                            best_rf,
                            X_train_resampled, 
                            y_train_resampled,
                            scoring=scoring,
                            n_jobs=-1,
                            cv=10,
                            verbose=1
)
print('\nResultado do cross vall:', scores_cross)
print('\nAcurácia:', scores_cross['test_accuracy'].mean())
print('\nPrecision:', scores_cross['test_precision_macro'].mean())
print('\nRecall:', scores_cross['test_recall_macro'].mean())
print('\nF1 Score:', scores_cross['test_f1_macro'].mean())

# 10. Avaliação
y_predito = best_rf.predict(X_test_final)
acuracia = accuracy_score(y_test, y_predito)
f1_macro = f1_score(y_test, y_predito, average='macro')
print(f"\nAcurácia Global no conjunto de Teste: {acuracia:.4f}")
print(f"F1-Score (macro) no conjunto de Teste: {f1_macro:.4f}")

# 11. Matriz de Confusão
cm = confusion_matrix(y_test, y_predito)
classes = best_rf.classes_
print("\n Matriz de Confusão:")
print(cm)

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=classes)
disp.plot(cmap='Blues', values_format='d', xticks_rotation=45) 
plt.title("Matriz de Confusão - Random Forest")
plt.tight_layout()
plt.savefig(MODEL_DIR / 'matriz_confusao.png', dpi=300, bbox_inches='tight')
plt.close()
# 12. Cálculo Sensibilidade, Especificidade e F1-Score
n_classes = len(classes)
sensibilidade_classes = []
especificidade_classes = []
acuracia_classes = []
f1_classes = []

for i in range(n_classes):
    tp = cm[i, i]
    fn = cm[i, :].sum() - tp
    fp = cm[:, i].sum() - tp
    tn = cm.sum() - (tp + fn + fp)
    sens = tp / (tp + fn) if (tp + fn) > 0 else 0
    spec = tn / (tn + fp) if (tn + fp) > 0 else 0
    acc_classe = (tp + tn) / cm.sum()
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0
    f1_c = 2 * (prec * sens) / (prec + sens) if (prec + sens) > 0 else 0

    sensibilidade_classes.append(sens)
    especificidade_classes.append(spec)
    acuracia_classes.append(acc_classe)
    f1_classes.append(f1_c)

    print(f"\nClasse: {classes[i]}")
    print(f"  Acurácia: {acc_classe:.4f}")
    print(f"  Sensibilidade (Recall): {sens:.4f}")
    print(f"  Especificidade: {spec:.4f}")
    print(f"  Precisão: {prec:.4f}")
    print(f"  F1-Score: {f1_c:.4f}")

print("\nMétricas Médias Globais:")
print(f"Sensibilidade Média: {np.mean(sensibilidade_classes):.4f}")
print(f"Especificidade Média: {np.mean(especificidade_classes):.4f}")
print(f"Acurácia Média por Classe: {np.mean(acuracia_classes):.4f}")
print(f"F1-Score Médio: {np.mean(f1_classes):.4f}")
