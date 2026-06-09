import pandas as pd

# 1. Abrir ambos os CSV (separador é ';')
red_df = pd.read_csv(r'C:\Users\08459973948\Desktop\faculdade\Sistemas Inteligentes Avançados\trabalho_09062026\winequality-red.csv', sep=';')
white_df = pd.read_csv(r'C:\Users\08459973948\Desktop\faculdade\Sistemas Inteligentes Avançados\trabalho_09062026\winequality-white.csv', sep=';')

# Adicionar uma coluna para identificar o tipo de vinho
red_df['wine type'] = 'red'
white_df['wine type'] = 'white'

# 2. Juntar numa única tabela
dados = pd.concat([red_df, white_df], ignore_index=True)

dados_atributos = dados.drop(columns=['wine type', 'quality'])
dados_classe = dados[['wine type', 'quality']]

