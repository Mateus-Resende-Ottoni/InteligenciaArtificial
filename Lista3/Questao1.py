import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

from sklearn.tree import DecisionTreeClassifier

from sklearn.preprocessing import LabelEncoder

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

from sklearn.model_selection import train_test_split

import pickle

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from yellowbrick.classifier import ConfusionMatrix

from sklearn import tree
#__________________________________________________

# Carregar dados e os formatar para uso
def loadData():
    # Obter dados do arquivo
    dados = pd.read_csv('/Dados/restaurante.csv', sep=';')

    # Codifica os atributos de valor binário e multivalorados ordinais em numérico
    cols_label_encode = ['Alternativo', 'Bar', 'SexSab','fome', 'Cliente','Preco', 'Chuva', 'Res','Tempo']
    dados[cols_label_encode] = dados[cols_label_encode].apply(LabelEncoder().fit_transform)

    # Codificação da coluna multivalorada não-ordinal em numérica
    cols_onehot_encode = ['Tipo']
    # Inicializar o OneHotEncoder (sparse_output=False retorna um array denso)
    onehot = OneHotEncoder(sparse_output=False)
    # Aplicar o OneHotEncoder apenas nas colunas categóricas
    df_onehot = onehot.fit_transform(dados[cols_onehot_encode])
    # Obter os novos nomes das colunas após a codificação
    nomes_das_colunas = onehot.get_feature_names_out(cols_onehot_encode)
    # Criar um DataFrame com os dados codificados e as novas colunas
    df_onehot = pd.DataFrame(df_onehot, columns=nomes_das_colunas)
    # Combinar as colunas codificadas com as colunas que não foram transformadas
    dados_encoded= pd.concat([df_onehot, dados.drop(columns=cols_onehot_encode)], axis=1)

    # Separação dos dados de atributo da conclusão
    X_prev= dados_encoded.iloc[:, :-1]
    y_classe = dados_encoded.iloc[:, -1]

    # Separar dados em treino e teste
    # (parte é usada para treinar a árvore, os demais servem para testes futuros do modelo)
    X_treino, X_teste, y_treino, y_teste = train_test_split(X_prev, y_classe, test_size = 0.20, random_state = 42)

    # Salvar dados formatados em novo arquivo
    with open('/Dados/Restaurante.pkl', mode = 'wb') as f:
        pickle.dump([X_treino, X_teste, y_treino, y_teste], f)
#__________________________________________________

# Testar modelo
def testTree(modelo, x_treino, x_teste, y_treino, y_teste):
    # Testar árvore
    previsoes = modelo.predict(x_teste)

    # Obter acurácia do teste
    accuracy_score(y_teste, previsoes)

    # Matriz de confusão
    confusion_matrix(y_teste, previsoes)
    cm = ConfusionMatrix(modelo)
    cm.fit(x_treino, y_treino)
    cm.score(x_teste, y_teste)
    print(classification_report(y_teste, previsoes))
#__________________________________________________

# Criar árvore com a base de dados
def createTree():
    # Abrir dados formatados de arquivo e transferir para variáveis
    with open('/Dados/restaurante.pkl', 'rb') as f:
        X_treino, X_teste, y_treino, y_teste = pickle.load(f)

    # Definir critério da árvore como sendo entropia
    modelo = DecisionTreeClassifier(criterion='entropy')

    Y = modelo.fit(X_treino, y_treino)

    # Testar modelo
    testTree(modelo, X_treino, X_teste, y_treino, y_teste)

    # Print do resultado
    previsores = X_treino.columns
    figura, eixos = plt.subplots(nrows=1, ncols=1, figsize=(13,13))
    tree.plot_tree(modelo, feature_names=previsores, class_names = modelo.classes_, filled=True);
#__________________________________________________

# Função principal
def main():
    #print("Program start")
    # Carregar base de dados
    loadData()

    # Montar árvore
    createTree()
#__________________________________________________

# Chamar função principal
if __name__ == "__main__":
    main();
#__________________________________________________