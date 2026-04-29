import pandas as pd
import pickle

columns_names = [
    'Age', 'Height', 'Weight', 'FCVC', 'NCP', 'CH2O', 'FAF', 'TUE',
    'Gender_Female', 'Gender_Male', 'family_history_with_overweight_no',
    'family_history_with_overweight_yes', 'FAVC_no', 'FAVC_yes',
    'CAEC_Always', 'CAEC_Frequently', 'CAEC_Sometimes', 'CAEC_no',
    'SMOKE_no', 'SMOKE_yes', 'SCC_no', 'SCC_yes', 'CALC_Always',
    'CALC_Frequently', 'CALC_Sometimes', 'CALC_no', 'MTRANS_Automobile',
    'MTRANS_Bike', 'MTRANS_Motorbike', 'MTRANS_Public_Transportation',
    'MTRANS_Walking', 'NObeyesdad_Insufficient_Weight',
    'NObeyesdad_Normal_Weight', 'NObeyesdad_Obesity_Type_I',
    'NObeyesdad_Obesity_Type_II', 'NObeyesdad_Overweight_Level_I',
    'NObeyesdad_Overweight_Level_II'
]

paciente_dataframe = pd.DataFrame(columns=columns_names)

novo_paciente = [[21.5, 1.57, 51.5, 2.37, 3.12, 2.0, 0.0, 0.0]]

normalizador = pickle.load(open('normalizador_obesity.pkl', 'rb'))
cluster_obesity = pickle.load(open('cluster_obesity.pkl', 'rb'))

novo_paciente_norm = normalizador.transform(novo_paciente)

novo_paciente_norm = pd.DataFrame(novo_paciente_norm, 
                                  columns=['Age', 'Height', 'Weight', 'FCVC', 
                                           'NCP', 'CH2O', 'FAF', 'TUE'])

paciente_nova_instancia = pd.concat([novo_paciente_norm, paciente_dataframe]).fillna(0)

cluster_paciente = cluster_obesity.predict(paciente_nova_instancia)
print('Cluster do novo paciente:', cluster_paciente)
