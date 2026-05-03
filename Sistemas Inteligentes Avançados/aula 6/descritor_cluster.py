# W -- este arquivo tem como objetivo demonstrar os centroides dos clusters criados pelo modelo de clusterização
# W -- centroide é o ponto central de cada cluster (grupo), informalmente chamado de média. ou seja, este código mostra a média de cada grupo

#Imports
import pickle
import pandas as pd

#Abrir o modelo de clusters
# W -- é a IA que vai analisar os dados e definir a qual grupo/cluster pertence cada objeto, neste exemplo estamos usando 9 clusters
cluster_model = pickle.load(open('cluster_iris.pkl','rb'))

#Abrir o normalizador numérico salvo anteriormente
# W -- serve para transformar os dados normalizados em dados reais e vice-versa
normalizador = pickle.load(open('normalizador_iris.pkl', 'rb'))

#Desnormalizar os centroides
# W -- centroides são os pontos centrais de cada cluster
# W -- para cada cluster existe um centroide, por exemplo 6.535714     3.071429      4.635714     1.492857  Iris-versicolor é um centroide
# W -- columns_names é uma lista que contém os nomes das colunas do dataframe
columns_names = ['sepal_length', 
                 'sepal_width', 
                 'petal_length', 
                 'petal_width',
                 'Iris-setosa', 
                 'Iris-versicolor', 
                 'Iris-virginica']

#Converter os centroides em dataframe

# W -- pega os centroides e dá o nome das colunas do dataframe
dataframe = pd.DataFrame(cluster_model.cluster_centers_, columns = columns_names)

# W -- desnormaliza os centroides sem as colunas de classe
atributos_num_desnorm = pd.DataFrame(
    normalizador
      .inverse_transform(
          dataframe[
              ['sepal_length', 
                 'sepal_width', 
                 'petal_length', 
                 'petal_width']]),
                 columns  = ['sepal_length', 
                 'sepal_width', 
                 'petal_length', 
                 'petal_width']
                 )

#Desnormalizar as colunas codificadas com one_hot_encoder
# W -- Desnomaliza as colunas de classe
# W -- class_dataframe transforma as colunas da classe em booleano/binario novamente
class_dataframe = dataframe[['Iris-setosa', 
                 'Iris-versicolor', 
                 'Iris-virginica']].round(0).astype(int)

# W -- Transforma os valores binários em categorias (desnormaliza), ficando com o nome da classe
class_dataframe = pd.from_dummies(class_dataframe)
class_dataframe.columns=['class']

#Juntar os dataframes: colunas numéricas desnormalizadas e a categoria desnormalizada
cluster = atributos_num_desnorm.join(class_dataframe)
print(cluster)


