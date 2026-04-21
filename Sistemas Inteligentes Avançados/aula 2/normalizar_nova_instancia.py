#Recebe um novo valor numerico e normaliza com o modelo original
import pickle

#Abrir o modelo normalizador original
scaler_model = pickle.load(open('scaler1.pkl', 'rb'))

novo_dado =[[2000]]
novo_dado_norm = scaler_model.transform(novo_dado)

print(novo_dado)
print(novo_dado_norm)
dado_revertido = scaler_model.inverse_transform(novo_dado_norm)
print(dado_revertido)