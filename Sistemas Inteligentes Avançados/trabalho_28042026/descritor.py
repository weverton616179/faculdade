import pickle
import pandas as pd

cluster_model = pickle.load(open('cluster_obesity.pkl', 'rb'))
normalizador = pickle.load(open('normalizador_obesity.pkl', 'rb'))

dados = pd.read_csv(r'C:\Users\weverton\Desktop\Faculdade\faculdade\Sistemas Inteligentes Avançados\trabalho_28042026\ObesityDataSet_raw_and_data_sinthetic.csv', sep=',')
colunas_categoricas = ['Gender', 'family_history_with_overweight', 'FAVC', 'CAEC', 'SMOKE', 'SCC', 'CALC', 'MTRANS', 'NObeyesdad']

dados_num = dados.drop(columns=colunas_categoricas)
dados_cat = dados[colunas_categoricas]
dados_cat_norm = pd.get_dummies(dados_cat, prefix_sep='_', dtype=int)
columns_names = list(dados_num.columns) + list(dados_cat_norm.columns)

dataframe = pd.DataFrame(cluster_model.cluster_centers_, columns=columns_names)
atributos_num_desnorm = pd.DataFrame(
    normalizador.inverse_transform(dataframe[dados_num.columns]),
    columns=dados_num.columns
)

class_dataframe = dataframe[dados_cat_norm.columns].round(0).astype(int)
categorias_desnorm = pd.from_dummies(class_dataframe, sep='_', default_category='Desconhecido')
cluster = atributos_num_desnorm.join(categorias_desnorm)
print(cluster)