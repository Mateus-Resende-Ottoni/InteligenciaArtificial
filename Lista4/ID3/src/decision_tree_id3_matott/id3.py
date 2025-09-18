import pandas as pd
import math
import rule

# Receber matriz completa de dados
def data_classification(data):
    # Separar matriz de dados em treino e teste
    train_data = data
    test_data = data
    # Separar coluna de resultados
    train_data = train_data
    train_result = train_data
    test_data = test_data
    test_result = test_data

class ID3:
    # Criar árvore
    def __init__ (self, max_height, min_information, data, results, classification_attribute):
        # Altura máxima
        # -1 significa que não tem máximo
        self.max_height = max_height
        self.current_height = 0
        # Regras para o ganho de informação
        self.min_information = min_information
        # Base de dados inicial
        self.data = data
        # Atributo buscado na classificação
        self.classification_attribute = classification_attribute
        # Contar na coluna de resultados quantos há
        self.results_list = list(set(results))
        self.results_n = len(list(set(results)))
        # Definir raiz
        self.root = None
        # Teste
        #print(f"Criado árvore altura máxima {self.max_height}, informação mínima {self.min_information} com {self.results_n} tipos de resultados")

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

    # Montar árvore
    def create_tree(self, data, result):
        # Chamar método de montagem da árvore para a raiz
        self.root = self.define_rule(self.root, data, result, 0)

    # Método para montagem de árvore
    def define_rule(self, current_rule, data, result, level):
        # Chamar método de determinação de atributo e salvar regra de montagem
        regra_resultante = self.define_attribute(data, result, level)
        #print(regra_resultante)
        #print("-     -------------------     -")
        #current_rule = regra_resultante
        # Se retorno tiver sido nulo, parar
        # Retorno nulo significa que o ganho na regra não foi suficiente
        if ( (regra_resultante != None) ):
            # Se ainda não tiver chegado no limite de altura 
            if ( (self.current_height < self.max_height) or (self.max_height == -1) ):
                # Para cada ramo, chamar método de montagem da árvore
                for ramo in regra_resultante.connections:
                        # Uma forma mais eficiente é adicionar quando corresponder ao critério
                        # ao invés de remover quando não corresponder, mas não sei implementar isso
                    # Tabela completa para remover atributos que não encaixarem
                    data_branch = data
                    result_branch = result
                    # Remover dados não pertencentes ao ramo
                    for row in data.index:
                        if data[regra_resultante.attribute][row] != ramo.result_name:
                            data_branch = data_branch.drop(index=row)
                            result_branch = result_branch.drop(index=row)
                    # Chamar método de montagem da regra
                    #print("\n\n"); print(data_branch)
                    #print("\n");   print(result_branch); print("\n\n")
                    ramo.rule = self.define_rule(ramo.rule, data_branch, result_branch, level+1)
        return regra_resultante

    # Método de determinação de atributo (recebendo dados e resultados de treino)
    def define_attribute(self, data_unformatted, results, level):
        #print (f"define attribute level {level}\n")
        # Formatar dados para melhor uso
        data = pd.DataFrame(data_unformatted)
        #results = pd.DataFrame(results_unformatted)
        #print(results)
        #print(type(results))
        # Número de linhas
        n_instancias = len(data)
        #print(f"n_instancias: {n_instancias}")
        resultados_distintos = list(set(results))
        #print(resultados_distintos)
        n_resultados = len(list(set(results)))
        #print(f"n_instancias: {n_instancias} e n_resultados: {n_resultados}")

        # Caso só haja um resultado distinto, não é necessário determinar uma regra
        if n_resultados == 1:
            regra = rule.DecisionRule('(Final)', 1.0, data, results, level)
            return regra

        # Cálculo da entropia da classe
        entropia_classe = 0
        for resultado in resultados_distintos:
            frequencia = 0
            for instancia in results:
                if instancia == resultado:
                    frequencia = frequencia + 1
            #print(f"frequencia: {frequencia} | n_instancias: {n_instancias} | n_resultados: {n_resultados}")
            freq_div_instancias = (frequencia * 1.0)/(n_instancias * 1.0)
            #print(f"Cálculo de entropia de classe: {freq_div_instancias}, {n_resultados}")
            entropia_atual = freq_div_instancias * (math.log(freq_div_instancias, n_resultados))
            entropia_classe = entropia_classe + entropia_atual
        entropia_classe = entropia_classe * (-1)
        # Criar lista separada para contabilizar ganho de informação em cada coluna
        attributes_gain = []
        # Loop de for para cada coluna
        #data_formatted = pd.DataFrame(data)
        #num_columns = data_formatted.shape[1]
        for column in data.columns:
            #print(f"coluna atual: {column}")
            ganho = entropia_classe
            # Contar quantas entradas diferentes há na coluna
            #print(data[column])
            #print(type(data[column]))
            entradas = len(list(set(data[column])))
            # Variável do somatório
            somatorio = 0
            # Cálculo de entropia
            # Para cada entrada possível
            for entrada in list(set(data[column])):
                soma = 0
                frequencia_entrada = 0
                # Contabilizar instancias da entrada
                for instancia in data[column]:
                    if ( (instancia == entrada) ):
                        frequencia_entrada = frequencia_entrada + 1
                # Contabilizar quantos número em cada resultado
                for resultado in resultados_distintos:
                    frequencia = 0
                    #print(f"entrada: {entrada} e resultado: {resultado}")
                    for instancia in data.index:
                        #print(data[column][instancia])
                        #print(results[instancia])
                        if ( (data[column][instancia] == entrada) & (results[instancia] == resultado) ):
                            frequencia = frequencia + 1
                    # Probabilidade do resultado * Log 2 da probabilidade
                    # Somar ao dos demais resultados
                    #print(f"frequencia: {frequencia} | frequencia_entrada: {frequencia_entrada} | n_resultados: {n_resultados}")
                    # Se a frequência for zero, efetivamente somamos 0, o que significa nada
                    if frequencia != 0:
                        freq_div_freqentrada = (frequencia * 1.0)/(frequencia_entrada * 1.0)
                        entropia_atual = freq_div_freqentrada * (math.log(freq_div_freqentrada, n_resultados))
                        soma = soma + entropia_atual
                # Multiplicar por -1 (correção devido a como log funciona)
                soma = soma * (-1)
                # Multiplicar pelo n de ocorrencia da entrada e dividir pelo n total
                soma = soma * ( (frequencia_entrada * 1.0) / (n_instancias * 1.0) )
                # Somar resultado ao somatório
                #print(f"somatorio: {somatorio} e soma: {soma}")
                somatorio = somatorio + soma
                #print(f"somatorio novo: {somatorio}")
            # Ganho = 1 - Somatório
            ganho = ganho - somatorio
            #print(f"somatorio final: {somatorio} e ganho: {ganho}")
            #print("- - - - -")
            # Adicionar resultado à lista
            #print(f"ganho da coluna {column} de {ganho}")
            attributes_gain.append(Association(ganho, column))
        # Varrer lista e definir coluna que provém maior ganho de informação
        maior_ganho_coluna = ''
        maior_ganho = -1
        for atributo in attributes_gain:
            if atributo.ganho > maior_ganho:
                maior_ganho_coluna = atributo.coluna
                maior_ganho = atributo.ganho
        # Se o ganho de informação for abaixo do mínimo estabelecido, retornar nulo
        if (maior_ganho < self.min_information):
            return None
        # Criar regra resultado
        #print(f"maior_ganho: {maior_ganho}")
        regra = rule.DecisionRule(maior_ganho_coluna, maior_ganho, data, results, level)
        #print(regra)
        #print("-     -------------------     -")
        # Criar conexões com nós seguintes da árvore para cada resultado possível do nó
        valores_coluna = list(set(data[maior_ganho_coluna]))
        for valor in valores_coluna:
            regra.connections.append(rule.Connection(valor))
        # Retornar resultado
        return regra
    
#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

    def test_tree(self, test_data, test_results):
        confusionMatrix = pd.DataFrame(index=self.results_list, columns=self.results_list)


#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
    
    def __str__(self):
        return self.rule_to_str(self.root, "")

    def rule_to_str(self, current_rule, attribute_name):
        # Retornar vazio se regra for vazia
        if current_rule == None:
            return f"{attribute_name}"
        current_str = ""
        # Indentação em acordo com profundidade da árvore
        for i in range(current_rule.level):
            current_str = current_str + "\t"
        # Adicionar valor de atributo que deriva de
        current_str = current_str + "{" + attribute_name + "}" + "  "
        current_str = current_str + str(current_rule)
        #print(current_str)
        # Adicionar as ramificações
        # Falta inserir as conexões em si para exibir
        for branch in current_rule.connections:
            current_str = current_str + "\n" + self.rule_to_str(branch.rule, branch.result_name)
        return current_str

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

class Association:
    def __init__(self, ganho, coluna):
        self.ganho = ganho
        self.coluna = coluna

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_



