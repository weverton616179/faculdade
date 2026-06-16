import pandas as pd
from pickle import load
import numpy as np

# 1. declarar os dados do novo vinho
# nome das colunas
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
# novo vinho
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

# cria um dataframe com os novos dados e estrutura de colunas
dados_dataframe = pd.DataFrame(novo_vinho, columns=columns_name)
#print(dados_dataframe)

# 2. preprocessamento dos dados
# carregamento dos arquivos
normalizador = load(open('normalizador.pkl', 'rb'))
modelo = load(open('modelo.pkl', 'rb'))

# normalizar dados do novo vinho
dados_norm = normalizador.transform(dados_dataframe)
dados_norm = pd.DataFrame(dados_norm, columns=columns_name)

# 3. predição da qualidade do vinho usando o modelo treinado
qualidade = modelo.predict(dados_norm)[0]
probabilidades = modelo.predict_proba(dados_norm)[0]
classes = modelo.classes_

# grau de certeza da predição (probabilidade da classe prevista)
indice_classe = list(classes).index(qualidade)
certeza = probabilidades[indice_classe] * 100

# 4. apresentação dos resultados
print('=' * 55)
print('    MÓDULO DE INFERÊNCIA — QUALIDADE DO VINHO')
print('=' * 55)

print('\n📋 Dados do novo vinho:')
print(f'  Ácido fixo:            {novo_vinho[0][0]:.2f}')
print(f'  Ácido volátil:         {novo_vinho[0][1]:.2f}')
print(f'  Ácido cítrico:         {novo_vinho[0][2]:.2f}')
print(f'  Açúcar residual:       {novo_vinho[0][3]:.2f}')
print(f'  Cloretos:              {novo_vinho[0][4]:.3f}')
print(f'  SO2 livre:             {novo_vinho[0][5]:.0f}')
print(f'  SO2 total:             {novo_vinho[0][6]:.0f}')
print(f'  Densidade:             {novo_vinho[0][7]:.4f}')
print(f'  pH:                    {novo_vinho[0][8]:.2f}')
print(f'  Sulfatos:              {novo_vinho[0][9]:.2f}')
print(f'  Álcool:                {novo_vinho[0][10]:.1f}')

print(f'\n🔮 Qualidade prevista:   {qualidade}')
print(f'🎯 Grau de certeza:      {certeza:.2f}%')

print('\n📊 Distribuição de probabilidade por classe:')
print(f'  {"Classe":<8} {"Probabilidade":>15}')
print(f'  {"-"*8} {"-"*15}')
for i, classe in enumerate(classes):
    barra = '█' * int(probabilidades[i] * 30)
    print(f'  {classe:<8} {probabilidades[i]*100:>13.2f}%  {barra}')
print('=' * 55)
