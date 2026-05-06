import pandas as pd
import numpy as np
from pickle import load, dump
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score
import matplotlib.pyplot as plt

#abrir arquivo de dados
dados = pd.read_csv(r'C:\Users\weverton\Desktop\Faculdade\faculdade\Sistemas Inteligentes Avançados\aula 9\fertility_Diagnosis.txt')

#separar atribuidos e classe
dados_atribuidos = dados.drop(columns=['Diagnostico'])
dados_classe = dados['Diagnostico']

#segmentar os dados em dados para treinamento e dados de teste
atributos_train, atributos_teste, classe_train, classe_teste = train_test_split(dados_atribuidos, dados_classe, test_size=0.2, random_state=42)

#treinar modelo
tree = DecisionTreeClassifier(random_state=42)
fertility_tree = tree.fit(atributos_train, classe_train)

#salvar modelo
dump(fertility_tree, open('fertility_tree.pkl', 'wb'))

#testando modelo
diagnostico_predito = fertility_tree.predict(atributos_teste)

acuraria = accuracy_score(classe_teste, diagnostico_predito)
print('Acurácia:', acuraria)

ConfusionMatrixDisplay.from_estimator(fertility_tree, atributos_teste, classe_teste)
# plt.show()
 
#calcular especificidade e sensibilidade
tn, fp, fn, tp = confusion_matrix(classe_teste, diagnostico_predito).ravel()

#especificidade
especificidade = tn / (tn + fp)
print('Especificidade:', especificidade)

#sensibilidade
sensibilidade = tp / (tp + fn)
print('Sensibilidade:', sensibilidade)