import pandas as pd
import numpy as np
from pickle import dump
from sklearn.model_selection import cross_validate, cross_val_predict, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, HistGradientBoostingClassifier
from pprint import pprint
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

from collections import Counter

# 1. Abrir o CSV
endereco_arquivo = r'C:\Users\08459973948\Desktop\faculdade\Sistemas Inteligentes Avançados\trabalho_09062026\retail_black_friday_sales_100k.csv'
dados = pd.read_csv(endereco_arquivo)

# 2. Remover colunas identificadoras (não relevantes para a classificação)
dados = dados.drop(columns=['transaction_id', 'customer_id', 'product_id', 'purchase_date'])

# Definir colunas categóricas e numéricas para o pré-processamento
colunas_categoricas = ['gender', 'city', 'customer_segment', 'age_group', 'product_category', 'payment_method']
colunas_numericas = ['original_price', 'discount_pct', 'final_price', 'quantity', 'purchase_amount', 'purchase_hour', 'is_weekend', 'is_black_friday']

# Configuração dos 3 modelos (Extra Trees, Random Forest, Gradient Boosting)
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


# -----------------------------------------------------------
# Função auxiliar para treinar e avaliar um classificador
# -----------------------------------------------------------
def treinar_classificador(nome_alvo, dados, colunas_categoricas, colunas_numericas, modelos_config):
    print(f'\n{"="*60}')
    print(f'    CLASSIFICADOR — {nome_alvo.upper()}')
    print(f'{"="*60}')

    # 3. Separar atributos (X) e classe (y)
    y = dados[nome_alvo]
    X = dados.drop(columns=[nome_alvo])

    # Ajustar a lista de colunas categóricas (remover o alvo se ele estiver lá)
    cat_cols = [c for c in colunas_categoricas if c != nome_alvo and c in X.columns]
    num_cols = [c for c in colunas_numericas if c in X.columns]

    # 4. Pré-processamento: OneHotEncoder para categóricas + StandardScaler para numéricas
    preprocessor = ColumnTransformer([
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols),
        ('num', StandardScaler(), num_cols)
    ])

    # Ajustar o preprocessador aos dados e salvar
    preprocessador = preprocessor.fit(X)
    dump(preprocessador, open(f'preprocessor_{nome_alvo}.pkl', 'wb'))

    # Transformar os dados
    X_transformado = preprocessador.transform(X)

    # Obter os nomes das colunas após a transformação (one-hot encoding expande as colunas)
    colunas_transformadas = (
        preprocessador.named_transformers_['cat'].get_feature_names_out(cat_cols).tolist()
        if cat_cols else []
    )
    X_transformado = pd.DataFrame(X_transformado, columns=colunas_transformadas + num_cols)

    # 5. Balancear os dados
    resampler = SMOTE(random_state=42, k_neighbors=4)
    X_b, y_b = resampler.fit_resample(X_transformado, y)

    print(f'\nFrequência das classes antes e após o balanceamento ({nome_alvo}):')
    print("Antes do balanceamento:")
    for classe, count in sorted(Counter(y).items()):
        print(f'  {classe}: {count}')
    print("\nApós o balanceamento:")
    for classe, count in sorted(Counter(y_b).items()):
        print(f'  {classe}: {count}')

    # 6. Hiperparametrização dos 3 modelos
    resultados = {}

    for config in modelos_config:
        nome = config['nome']
        print(f'\n--- {nome} ({nome_alvo}) ---')

        # Classificador diretamente (dados já balanceados do passo 5)
        search = RandomizedSearchCV(
            estimator=config['classe'](random_state=42),
            param_distributions=config['param_dist'],
            n_iter=10, cv=3, verbose=2, n_jobs=-1, random_state=42
        )
        search.fit(X_b, y_b)

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

    # 7. AVALIAÇÃO DOS MODELOS COM VALIDAÇÃO CRUZADA
    print(f'\nDesempenho dos modelos com validação cruzada ({nome_alvo}):')
    print(f"{'Classificador':<25} {'Acurácia':>10} {'F1-Score':>10}")
    print('-' * 47)

    metricas_modelos = {}

    for nome, modelo in resultados.items():
        scores = cross_validate(modelo, X_transformado, y, cv=5,
                                scoring=['accuracy', 'f1_macro'], n_jobs=-1)
        acc = scores['test_accuracy'].mean()
        f1 = scores['test_f1_macro'].mean()
        metricas_modelos[nome] = {'acuracia': acc, 'f1_macro': f1}
        print(f"{nome:<25} {acc:>10.4f} {f1:>10.4f}")

    # 8. Seleção do modelo vencedor
    modelo_vencedor = max(metricas_modelos, key=lambda x: metricas_modelos[x]['acuracia'])
    classificador_final = resultados[modelo_vencedor]
    print(f'\n>>> Modelo campeão ({nome_alvo}): {modelo_vencedor}')

    # Retreinar com todos os dados e salvar
    classificador_final.fit(X_transformado, y)
    dump(classificador_final, open(f'modelo_{nome_alvo}.pkl', 'wb'))

    # 9. Matriz de confusão com cross_val_predict (out-of-fold)
    y_previsto = cross_val_predict(classificador_final, X_transformado, y, cv=5)

    acuracia_global = accuracy_score(y, y_previsto)
    f1_medio = f1_score(y, y_previsto, average='macro')

    print(f'\nAcurácia: {acuracia_global:.4f}')
    print(f'F1-Score (macro): {f1_medio:.4f}')

    mc = confusion_matrix(y, y_previsto)
    print('\nMatriz de Confusão (out-of-fold):')
    print(mc)

    ConfusionMatrixDisplay.from_predictions(y, y_previsto)
    plt.title(f'Matriz de Confusão - {nome_alvo} ({modelo_vencedor})')
    plt.tight_layout()
    plt.savefig(f'matriz_confusao_{nome_alvo}.png', dpi=100)
    plt.close()

    # Acurácia individual por classe + sensibilidade + especificidade
    classes_rotulos = sorted(set(y))
    print(f'\nMétricas por classe ({nome_alvo}):')
    print(f"{'Classe':<20} {'Sensibilidade':>14} {'Especificidade':>16} {'F1-Score':>10}")
    print('-' * 62)
    for indice, rotulo in enumerate(classes_rotulos):
        VP = mc[indice, indice]
        FN = mc[indice, :].sum() - VP
        FP = mc[:, indice].sum() - VP
        VN = mc.sum() - (VP + FN + FP)

        sensibilidade = VP / (VP + FN) if (VP + FN) > 0 else 0.0
        especificidade = VN / (VN + FP) if (VN + FP) > 0 else 0.0
        f1_classe = 2 * VP / (2 * VP + FP + FN) if (2 * VP + FP + FN) > 0 else 0.0

        print(f"{rotulo:<20} {sensibilidade:>13.4f} {especificidade:>15.4f} {f1_classe:>9.4f}")

    # 10. Sumário final dos resultados
    print(f'\n{"Métrica":<35} {"Valor Obtido":>15}')
    print('-' * 52)
    print(f"{'Classificador Vencedor':<35} {modelo_vencedor:>15}")
    print(f"{'Acurácia':<35} {acuracia_global:>14.4f}")
    print(f"{'F1-Score (macro)':<35} {f1_medio:>14.4f}")


# -----------------------------------------------------------
# Executar o treinamento para cada um dos 3 alvos
# -----------------------------------------------------------
for alvo in ['product_category', 'payment_method', 'age_group']:
    treinar_classificador(alvo, dados, colunas_categoricas, colunas_numericas, modelos_config)
