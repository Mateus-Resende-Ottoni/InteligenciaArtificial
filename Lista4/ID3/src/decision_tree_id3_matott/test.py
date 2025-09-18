import id3

import pandas as pd

def __init__():

    print("\n\nInicio\n\n")

    # Abrir dados
    dados = pd.read_csv('restaurante.csv', sep=';')
    # Separar em dados e resultados
    classe = 'Conclusao'
    #
    data = dados.drop(columns=classe)
    #results = dados
    results = dados['Conclusao']

    # Criar árvore e definir critérios
    arvore = id3.ID3(-1, 0, data, results, 'Conclusao')
    # Gerar árvore
    arvore.create_tree(data, results)

    str(arvore)

    print("\n\nFim\n\n")
