from pickle import load

#coletar dados da nova intância
#atenção: lembre-se que os dados da nova instanca devem ser normalizados
paciente = [-0.33,0.92,1,0,0,1,0.6,-1,0.19]

#Carregar o modelo
fertility_model = load(open('fertilty_rf.pkl', 'rb'))

diagnostico = fertility_model.predict([paciente])
print(diagnostico)
print(fertility_model.classes_)
print(fertility_model.predict_proba([paciente]))
