import pandas as pd

df = pd.DataFrame({
    'sexo': ['M', 'F', 'N/A', 'M', 'F', 'M', 'F', 'N/A', 'M', 'F'],
    'cor': ['preto', 'azul', 'verde', 'rosa', 'rosa', 'verde', 'amarelo', 'preto', 'branco', 'azul']
})

dummies_sexo = pd.get_dummies(df, prefix='sexo', columns=['sexo'])
dummies_cor = pd.get_dummies(dummies_sexo, prefix='cor', columns=['cor'])

# print(dummies_sexo)
# print(dummies_cor)

# código acima recebe uma coluna com diversos valores, e os "binariza", chamado de one-hot encoding
# No exemplo acima, sexo gerará 3 colunas (sexo_F, sexo_M, sexo_N/A), com valores booleanos (True/False), e apenas uma das colunas será True

linha_exemplo = dummies_cor.iloc[1] # pega a linha de indice 1, que é sexo_F e cor_azul, porém está binarizado
print(linha_exemplo)

df_linha = linha_exemplo.to_frame().T # converte a linha (tipo Series) em um dataframe de uma linha
print(df_linha)

df_original = pd.from_dummies(df_linha, sep='_') # converte o dataframe binarizado de volta para o formato original
print(df_original)