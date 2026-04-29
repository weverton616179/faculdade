import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pickle
from sklearn.cluster import KMeans
import math
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
import numpy as np

# separar e normalizar os dados

dados = pd.read_csv(r'C:\Users\weverton\Desktop\Faculdade\faculdade\Sistemas Inteligentes Avançados\trabalho_28042026\ObesityDataSet_raw_and_data_sinthetic.csv', sep= ',')

dados_num = dados.drop(columns=['Gender', 'family_history_with_overweight', 'FAVC', 'CAEC', 'SMOKE', 'SCC', 'CALC', 'MTRANS', 'NObeyesdad'])
dados_cat = dados[['Gender', 'family_history_with_overweight', 'FAVC', 'CAEC', 'SMOKE', 'SCC', 'CALC', 'MTRANS', 'NObeyesdad']]

scaler = MinMaxScaler()
normalizador = scaler.fit(dados_num)
pickle.dump(normalizador, open('normalizador_obesity.pkl', 'wb'))
dados_num_norm = normalizador.fit_transform(dados_num)
dados_num_norm = pd.DataFrame(dados_num_norm, columns = dados_num.columns)

dados_cat_norm = pd.get_dummies(dados_cat, prefix_sep='_', dtype=int)

dados_norm = dados_num_norm.join(dados_cat_norm)
print(dados_norm.columns)

# determinar o numero otimo de clusters

distortions=[]
K = range(1, dados.shape[0])

for i in K:
    cluster_model = KMeans(n_clusters=i, random_state=42).fit(dados_norm)

    distortions.append(
        sum(
            np.min(
                cdist(dados_norm,
                      cluster_model.cluster_centers_,
                      'euclidean'), axis=1)/dados_norm.shape[0] 
            )
        )
    
x0 = K[0]
y0 = distortions[0]
xn = K[-1]    
yn = distortions[-1]
distances = []
for i in range(len(distortions)):
    x = K[i]
    y = distortions[i]
    numerador = abs(
        (yn-y0)*x - (xn-x0)*y + xn*y0 - yn*x0
    )
    denominador = math.sqrt(
        (yn-y0)**2 + (xn-x0)**2
    )
    distances.append(numerador/denominador)

numero_clusters_otimo = K[distances.index(np.max(distances))]
cluster_model = KMeans(n_clusters= numero_clusters_otimo, random_state= 42).fit(dados_norm)

pickle.dump(cluster_model, open('cluster_obesity.pkl', 'wb'))
print(numero_clusters_otimo)