import pandas as pd
from pickle import load
import numpy as np

# 1. DECLARANDO DADOS NOVOS
# -- Nome das colunas
columns_name = [
    'fixed acidity',       
    'volatile acidity',     
    'citric acid',         
    'residual sugar',       
    'chlorides',            
    'free sulfur dioxide',  
    'total sulfur dioxide', 
    'density',              
    'pH',
    'sulphates',            
    'alcohol'        
]
# -- Novo vinho
novo_vinho = [[
    7.8,
    0.76,
    0.04,
    2.3,
    0.092,
    15,
    54,
    0.997,
    3.26,
    0.65,
    9.8
]]

# -- Cria um dataframe com os novos dados e estrutura de colunas
dados_dataframe = pd.DataFrame(novo_vinho, columns=columns_name)
#print(dados_dataframe)

# 2. PRÉ-PROCESSAMENTO
# -- Carregamento dos arquivos
normalizador = load(open('normalizador.pkl', 'rb'))
modelo = load(open('modelo.pkl', 'rb'))

# -- Normalizar dados do novo vinho
dados_norm = normalizador.transform(dados_dataframe)
dados_norm = pd.DataFrame(dados_norm, columns=columns_name)
#print(dados_norm)

# 3. PREDIÇÃO
qualidade = modelo.predict(dados_norm)
print(qualidade)
print(modelo.classes_)
print(modelo.predict_proba(dados_norm))
