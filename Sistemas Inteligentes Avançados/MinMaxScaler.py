# este código serve para normalizar dados numéricos
# Ele recebe uma array com números, e transforma menor numero em 0 e maior numero em 1, e calcula os valores intermediários de forma proporcional
# Primeiramente ele treina com os dados originais e salva o modelo em um ".pkl"
# depois ele normaliza estes mesmos dados
# após, ele recebe um novo dado e normaliza com o modelo original
# e por fim ele reverte a normalização

from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pickle

#dados numéricos
dados =np.array([
    [1500], [3000], [5500], [10000]
])

#instanciar o normalizador
scaler = MinMaxScaler()

#Treinar o modelo normalizador para uso posterior
scaler_model = scaler.fit(dados) #Método fit() treina o modelo normalizador

#Salvar o modelo normalizador para uso posterior
pickle.dump(scaler_model,open('scaler1.pkl', 'wb'))

#Normalizar os dados
dados_norm = scaler_model.fit_transform(dados)

print(dados)
print(dados_norm)

# --------------------------------------------------------------------------------------------------------------------------------------

#Recebe um novo valor numerico e normaliza com o modelo original
#Abrir o modelo normalizador original
scaler_model = pickle.load(open('scaler1.pkl', 'rb'))

novo_dado =[[2000]]
novo_dado_norm = scaler_model.transform(novo_dado)

print(novo_dado)
print(novo_dado_norm)
dado_revertido = scaler_model.inverse_transform(novo_dado_norm)
print(dado_revertido)