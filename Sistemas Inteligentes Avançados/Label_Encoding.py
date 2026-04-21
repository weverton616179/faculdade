from sklearn.preprocessing import LabelEncoder

cores = ['preto', 'azul', 'branco', 'azul']

encoder = LabelEncoder()

cores_codificadas = encoder.fit_transform(cores)

print(cores_codificadas)

# o label encoder atribui um valor inteiro para cada categoria, de acordo com a ordem alfabética
# no exemplo acima, azul é 0, branco é 1 e preto é 2