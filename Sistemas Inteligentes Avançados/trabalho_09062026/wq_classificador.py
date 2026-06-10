import pandas as pd
import numpy as np
from pickle import dump
from sklearn.model_selection import cross_validate, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from pprint import pprint
from imblearn.over_sampling import SMOTE
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

from collections import Counter

# 1. Abrir ambos os CSV
red_df = pd.read_csv(r'/home/weverton/repositórios/faculdade/Sistemas Inteligentes Avançados/trabalho_09062026/winequality-red.csv', sep=';')
white_df = pd.read_csv(r'/home/weverton/repositórios/faculdade/Sistemas Inteligentes Avançados/trabalho_09062026/winequality-white.csv', sep=';')

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
        'classe': GradientBoostingClassifier,
        'param_dist': {
            'n_estimators': [int(x) for x in np.linspace(50, 200, 5)],
            'learning_rate': [0.01, 0.05, 0.1, 0.2],
            'max_depth': [3, 5, 7, 10],
            'min_samples_split': [2, 5, 10]
        }
    }
]

resultados = {}

for config in modelos_config:
    nome = config['nome']
    print(f'\n--- {nome} ---')

    # RandomizedSearchCV
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

    # Modelo final
    resultados[nome] = config['classe'](**search.best_params_, random_state=42)


# 5. AVALIAÇÃO DOS MODELOS COM VALIDAÇÃO CRUZADA
print('\ndesempenho dos modelos com validação cruzada:')
print(f"{'Classificador':<25} {'Acurácia':>10} {'F1-Score':>10}")
print('-' * 47)

metricas_modelos = {}

for nome, modelo in resultados.items():
    scores = cross_validate(modelo, atributos_b, classes_b, cv=5,
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

# retreinar com todos os dados balanceados e salvar
classificador_final.fit(atributos_b, classes_b)
dump(classificador_final, open('modelo.pkl', 'wb'))

# avaliação final com validação cruzada e matriz de confusão
scores_finais = cross_validate(classificador_final, atributos_b, classes_b, cv=5,
                                scoring=['accuracy', 'f1_macro'], n_jobs=-1)

acuracia_global = scores_finais['test_accuracy'].mean()
acuracia_std = scores_finais['test_accuracy'].std()
f1_medio = scores_finais['test_f1_macro'].mean()
f1_std = scores_finais['test_f1_macro'].std()

print(f'Acurácia Média (CV): {acuracia_global:.4f} ± {acuracia_std:.4f}')
print(f'F1-Score (macro, CV): {f1_medio:.4f} ± {f1_std:.4f}')

# predizer todos os dados para a matriz de confusão (análise exploratória)
y_previsto = classificador_final.predict(atributos_b)
mc = confusion_matrix(classes_b, y_previsto)
print('\nMatriz de Confusão (dados completos):')
print(mc)

ConfusionMatrixDisplay.from_predictions(classes_b, y_previsto)
plt.title(f'Matriz de Confusão - {modelo_vencedor}')
plt.tight_layout()
plt.savefig('matriz_confusao.png', dpi=100)
plt.close()

# acurácia individual por classe
print('\nAcurácia por classe:')
print(f"{'Classe':<10} {'Acerto (%)':>15}")
print('-' * 27)
for indice, rotulo in enumerate(sorted(set(classes_b))):
    verdadeiros_positivos = mc[indice, indice]
    total_ocorrencias = mc[indice, :].sum()
    porcentagem = (verdadeiros_positivos / total_ocorrencias) * 100 if total_ocorrencias > 0 else 0
    print(f"{rotulo:<10} {porcentagem:>14.2f}%")

# 8. sumario final dos resultados
print(f"\n{'Métrica':<25} {'Valor Obtido':>15}")
print('-' * 42)
print(f"{'Classificador Vencedor':<25} {modelo_vencedor:>15}")
print(f"{'Acurácia Média (CV)':<25} {acuracia_global:>14.4f}")
print(f"{'± Desvio Padrão':<25} {acuracia_std:>14.4f}")
print(f"{'F1-Score (macro, CV)':<25} {f1_medio:>14.4f}")
print(f"{'± Desvio Padrão':<25} {f1_std:>14.4f}")
