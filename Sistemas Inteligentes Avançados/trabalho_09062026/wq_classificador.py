import pandas as pd
import numpy as np
from pickle import dump
from sklearn.model_selection import cross_validate, cross_val_predict, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, HistGradientBoostingClassifier
from pprint import pprint
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

from collections import Counter

# 1. Abrir ambos os CSV
endereco_arquivo_red = r'C:\Users\08459973948\Desktop\faculdade\Sistemas Inteligentes Avançados\trabalho_09062026\winequality-red.csv'
endereco_arquivo_white = r'C:\Users\08459973948\Desktop\faculdade\Sistemas Inteligentes Avançados\trabalho_09062026\winequality-white.csv'

red_df = pd.read_csv(endereco_arquivo_red, sep=';')
white_df = pd.read_csv(endereco_arquivo_white, sep=';')

# 2. Juntar numa única tabela e separar atributos e classe
dados = pd.concat([red_df, white_df], ignore_index=True)
dados_atributos = dados.drop(columns=['quality'])
dados_classe = dados['quality']

# print(dados_atributos)
# print(dados_classe)

# 3. Padronizar os dados (StandardScaler)
scaler = StandardScaler()
# Ajustar o normalizador aos dados e salvar o modelo do normalizador
normalizador = scaler.fit(dados_atributos)
dump(normalizador, open('normalizador.pkl', 'wb'))
# Transformar os dados usando o normalizador e criar um DataFrame com os mesmos rótulos de coluna
dados_atributos_norm = normalizador.transform(dados_atributos)
dados_atributos_norm = pd.DataFrame(dados_atributos_norm, columns=dados_atributos.columns)

# print(dados_atributos_norm)
# print(dados_classe)

# 4. Balancear os dados
resampler = SMOTE(random_state=42, k_neighbors=4)
atributos_b, classes_b = resampler.fit_resample(dados_atributos_norm, dados_classe)

print("frequência das classes antes e após o balanceamento:")
print("Antes do balanceamento:")
for classe, count in sorted(Counter(dados_classe).items()):
    print(f'class: {classe} elementos: {count}')
print("\nApós o balanceamento:")
for classe, count in sorted(Counter(classes_b).items()):
    print(f'class: {classe} elementos: {count}')
    
# Hiperparametrização 3 modelos
modelos_config = [
    {
        'nome': 'Extra Trees',
        'classe': ExtraTreesClassifier,
        'param_dist': {
            'n_estimators': [int(x) for x in np.linspace(10, 100, 10)],
            'criterion': ['gini', 'entropy'],
            'min_samples_split': [int(x) for x in np.linspace(2, 10, 2)],
            'max_depth': [int(x) for x in np.linspace(10, 100, 20)],
            'max_features': ['sqrt', 'log2']
        }
    },
    {
        'nome': 'Random Forest',
        'classe': RandomForestClassifier,
        'param_dist': {
            'n_estimators': [int(x) for x in np.linspace(10, 100, 10)],
            'criterion': ['gini', 'entropy'],
            'min_samples_split': [int(x) for x in np.linspace(2, 10, 2)],
            'max_depth': [int(x) for x in np.linspace(10, 100, 20)],
            'max_features': ['sqrt', 'log2']
        }
    },
    {
        'nome': 'Gradient Boosting',
        'classe': HistGradientBoostingClassifier,
        'param_dist': {
            'max_iter': [int(x) for x in np.linspace(50, 200, 5)],
            'learning_rate': [0.01, 0.05, 0.1, 0.2],
            'max_depth': [3, 5, 7, 10],
            'min_samples_leaf': [10, 20, 50]
        }
    }
]

resultados = {}

for config in modelos_config:
    nome = config['nome']
    print(f'\n--- {nome} ---')

    # Classificador diretamente (dados já balanceados do passo 4)
    search = RandomizedSearchCV(
        estimator=config['classe'](random_state=42),
        param_distributions=config['param_dist'],
        n_iter=10, cv=3, verbose=2, n_jobs=-1, random_state=42
    )
    search.fit(atributos_b, classes_b)

    # Resultados
    print(f'\n=== Melhores hiperparâmetros ({nome}) ===')
    pprint(search.best_params_)
    print(f'>> Score médio (validação cruzada): {search.best_score_:.4f}')

    # Pipeline final (com SMOTE para usar nos dados originais desbalanceados)
    resultados[nome] = ImbPipeline([
        ('smote', SMOTE(random_state=42, k_neighbors=2)),
        ('classifier', config['classe'](**search.best_params_,
                                        random_state=42))
    ])


# 5. AVALIAÇÃO DOS MODELOS COM VALIDAÇÃO CRUZADA
print('\ndesempenho dos modelos com validação cruzada:')
print(f"{'Classificador':<25} {'Acurácia':>10} {'F1-Score':>10}")
print('-' * 47)

metricas_modelos = {}

for nome, modelo in resultados.items():
    scores = cross_validate(modelo, dados_atributos_norm, dados_classe, cv=5,
                            scoring=['accuracy', 'f1_macro'], n_jobs=-1)
    acc = scores['test_accuracy'].mean()
    f1 = scores['test_f1_macro'].mean()
    metricas_modelos[nome] = {'acuracia': acc, 'f1_macro': f1}
    print(f"{nome:<25} {acc:>10.4f} {f1:>10.4f}")

# 6. seleção do modelo vencedor
# escolher o modelo com maior acurácia
modelo_vencedor = max(metricas_modelos, key=lambda x: metricas_modelos[x]['acuracia'])
classificador_final = resultados[modelo_vencedor]
print(f'\n>>> Modelo campeão: {modelo_vencedor}')

# retreinar com todos os dados e salvar
classificador_final.fit(dados_atributos_norm, dados_classe)
dump(classificador_final, open('modelo.pkl', 'wb'))

# 7. Matriz de confusão com cross_val_predict (out-of-fold)
y_previsto = cross_val_predict(classificador_final, dados_atributos_norm, dados_classe, cv=5)

acuracia_global = accuracy_score(dados_classe, y_previsto)
f1_medio = f1_score(dados_classe, y_previsto, average='macro')

print(f'Acurácia: {acuracia_global:.4f}')
print(f'F1-Score (macro): {f1_medio:.4f}')

mc = confusion_matrix(dados_classe, y_previsto)
print('\nMatriz de Confusão (out-of-fold):')
print(mc)

ConfusionMatrixDisplay.from_predictions(dados_classe, y_previsto)
plt.title(f'Matriz de Confusão - {modelo_vencedor}')
plt.tight_layout()
plt.savefig('matriz_confusao.png', dpi=100)
plt.close()

# acurácia individual por classe + sensibilidade + especificidade
classes_rotulos = sorted(set(dados_classe))
print('\nMétricas por classe:')
print(f"{'Classe':<8} {'Sensibilidade':>14} {'Especificidade':>16} {'F1-Score':>10}")
print('-' * 50)
for indice, rotulo in enumerate(classes_rotulos):
    VP = mc[indice, indice]
    FN = mc[indice, :].sum() - VP
    FP = mc[:, indice].sum() - VP
    VN = mc.sum() - (VP + FN + FP)

    sensibilidade = VP / (VP + FN) if (VP + FN) > 0 else 0.0
    especificidade = VN / (VN + FP) if (VN + FP) > 0 else 0.0
    f1_classe = 2 * VP / (2 * VP + FP + FN) if (2 * VP + FP + FN) > 0 else 0.0

    print(f"{rotulo:<8} {sensibilidade:>13.4f} {especificidade:>15.4f} {f1_classe:>9.4f}")

# 8. sumario final dos resultados
print(f"\n{'Métrica':<25} {'Valor Obtido':>15}")
print('-' * 42)
print(f"{'Classificador Vencedor':<25} {modelo_vencedor:>15}")
print(f"{'Acurácia':<25} {acuracia_global:>14.4f}")
print(f"{'F1-Score (macro)':<25} {f1_medio:>14.4f}")
