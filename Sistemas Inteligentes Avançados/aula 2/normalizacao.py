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