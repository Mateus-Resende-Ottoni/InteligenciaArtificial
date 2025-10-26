import math

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
#_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
class NeuronNetwork:
    def __init__(self, entradas, meio, saidas):
        self.neurons = []

        # Os neurônios serão representados por uma lista de pesos
        # Camada oculta
        camada_neuronios = []
        for neuronio in range(meio):
            neuronio_pesos = []
            for n_entrada in range(entradas):
                neuronio_pesos.append(0.1)
            # Append para representar o bias
            neuronio_pesos.append(0.1)
            camada_neuronios.append(neuronio_pesos)
        self.neurons.append(camada_neuronios)

        # Camada de saída
        camada_neuronios = []
        for neuronio in range(saidas):
            neuronio_pesos = []
            for n_meio in range(meio):
                neuronio_pesos.append(0.1)
            # Append para representar o bias
            neuronio_pesos.append(0.1)
            camada_neuronios.append(neuronio_pesos)
        self.neurons.append(camada_neuronios)
            
        
    # Resultados intermediarios
    def instance_intermediario(self, entradas):
        resultados_intermediario = []
        for neuronio in self.neurons[0]:
            soma_atual = 0
            n_entradas = len(entradas)

            # Para cada entrada
            for n in range(n_entradas):
                soma_atual = soma_atual + entradas[n] * neuronio[n]
            # Somar bias
            soma_atual = soma_atual + 1 * neuronio[n_entradas]

            # Aplicar função de normalização
            soma_atual = 1 / (1 + math.exp(0-soma_atual))
            # Salvar resultado em camada intermediária
            resultados_intermediario.append(soma_atual)

        return resultados_intermediario
    
    # Resultados da camada de saída
    def instance_exit(self, resultados_intermediario):
        resultado = []
        for neuronio in self.neurons[1]:
            soma_atual = 0
            n_intermediario = len(resultados_intermediario)

            # Para cada neuronio da camada intermediária
            for n in range(n_intermediario):
                soma_atual = soma_atual + resultados_intermediario[n] * neuronio[n]
            # Somar bias
            soma_atual = soma_atual + 1 * neuronio[n_intermediario]

            # Aplicar função de normalização
            soma_atual = 1 / (1 + math.exp(0-soma_atual))
            # Salvar resultado
            resultado.append(soma_atual)
        return resultado

    # Resultados de uma instância
    def instance_result(self, entradas, resultados_intermediario):
        resultados = []

        # Camada de saída
        resultados = self.instance_exit(resultados_intermediario)

        return resultados
    

    # Derivadas dos neurônios das camadas em determinadas instâncias
    def instance_derivadas(self, entradas, resultados_intermediario):
        resultados = []

        # Camada intermediária
        derivadas_intermediario = []
        for resultado in resultados_intermediario:
            derivada = resultado * (1-resultado)
            derivadas_intermediario.append(derivada)

        # Camada de saída
        derivadas_resultados = []
        resultados_saida = self.instance_exit(resultados_intermediario)
        for resultado in resultados_saida:
            derivada = resultado * (1-resultado)
            derivadas_resultados.append(derivada)

        resultados.append(derivadas_intermediario)
        resultados.append(derivadas_resultados)

        return resultados


    # Ajustes
    def weight_adjust(self, entradas, resultados_intermediario, erros_intermediario, erros_resultados, taxa):
        print(f"Start adjusting weight")

        #print(entradas)
        #print(resultados_intermediario)
        #print(erros_intermediario)
        #print(erros_resultados)
        
        # Camada de saída
        for neuronio in range(len(self.neurons[1])):
            print(self.neurons[1][neuronio])

            n_neuronios = len(resultados_intermediario)
            print(f"N resultados intermediario = {n_neuronios}")

            for n in range(n_neuronios):
                #print(n)
                #print(resultados_intermediario[n])
                #print(erros_resultados[n])

                self.neurons[1][neuronio][n] = self.neurons[1][neuronio][n] + taxa * resultados_intermediario[n] * erros_resultados[neuronio]
            # Bias
            self.neurons[1][neuronio][n_neuronios] = self.neurons[1][neuronio][n_neuronios] + taxa * 1 * erros_resultados[neuronio]

        # Camada intermediária
        for neuronio in range(len(self.neurons[0])):
            n_neuronios = len(entradas)
            for n in range(n_neuronios):
                self.neurons[0][neuronio][n] = self.neurons[0][neuronio][n] + taxa * entradas[n] * erros_intermediario[neuronio]
            # Bias
            self.neurons[0][neuronio][n_neuronios] = self.neurons[0][neuronio][n_neuronios] + taxa * 1 * erros_intermediario[neuronio]
                
        print(f"Finish adjusting weight")


    # Uma geração do algoritmo
    def run_generation(self, entradas, resultados_esperados, learning_rate):

        print(f"Start running generation")


        erro_medio = 0
        n_erros = 0
        resultados_diferencas = []

        # Para caso o ajuste de erro seja a cada vários
        #for n in range(len(entradas)):
        #    resultados_intermediario = self.instance_intermediario(entradas[n])
        #    resultados_obtidos = self.instance_result(entradas[n], resultados_intermediario)
        #    derivadas = self.instance_derivadas(entradas[n], resultados_intermediario)

            # Obter diferença dos resultados desejados pelos obtidos
        #    for m in range(len(resultados_esperados[n])):
        #        diferenca = resultados_esperados[m] - resultados_obtidos[m]
        #        diferenca = pow(diferenca, 2)
        #        resultados_diferencas.append(diferenca)

        resultados_intermediario = self.instance_intermediario(entradas)
        resultados_obtidos = self.instance_result(entradas, resultados_intermediario)
        derivadas = self.instance_derivadas(entradas, resultados_intermediario)

        print(f"Esperado: {resultados_esperados}")
        print(f"Obtido: {resultados_obtidos}")

        # Obter diferença dos resultados desejados pelos obtidos
        for n in range(len(resultados_esperados)):
            print(n)

            diferenca = resultados_esperados[n] - resultados_obtidos[n]
            diferenca = pow(diferenca, 2)
            resultados_diferencas.append(diferenca)

        # Somatório das diferenças
        somatorio_diferencas = 0
        for n in range(len(resultados_diferencas)):
            somatorio_diferencas = somatorio_diferencas + resultados_diferencas[n]
        # Obter média
        media_diferencas = somatorio_diferencas/len(resultados_diferencas)


        # Calcular erros na camada de resultados
        erros_resultados = []
        for neuronio in range(len(self.neurons[1])):
            erro = media_diferencas * derivadas[1][neuronio]
            erros_resultados.append(erro)

        # Calcular erros na camada intermediária
        erros_intermediario = []
        for neuronio in range(len(self.neurons[0])):
            somatorio_camada_posterior = 0
            for saida in range(len(erros_resultados)):
                erro_ajustado = self.neurons[0][neuronio][saida] * erros_resultados[saida]
                somatorio_camada_posterior = somatorio_camada_posterior + erro_ajustado
            erro = somatorio_camada_posterior * derivadas[0][neuronio]
            erros_intermediario.append(erro)

        # Calcular erro médio
        for erro in erros_intermediario:
            n_erros = n_erros + 1
            erro_medio = erro_medio + erro
        for erro in erros_resultados:
            n_erros = n_erros + 1
            erro_medio = erro_medio + erro
        erro_medio = erro_medio/n_erros
        

        # Ajuster pesos
        self.weight_adjust(entradas, resultados_intermediario, erros_intermediario, erros_resultados, learning_rate)

        print(f"Finish running generation")

        return erro_medio
        

    def run_network(self, num_generations, entradas, resultados_esperados, min_error_difference):

        print(f"Start running network")

        min_error_found = False
        generation = 1

        n_entradas = len(entradas)
        entrada_atual = entradas[0]
        resultados_esperados_atual = resultados_esperados[0] 


        # Retornar saídas da camada de saída para comparar com resultados esperados


        while ( ((generation <= num_generations) or (num_generations == -1)) and (not min_error_found) ):
            # Definir entrada atual (e respectivas saídas)
            entrada_atual = entradas[(generation - 1) % n_entradas]
            resultados_esperados_atual = resultados_esperados[(generation - 1) % n_entradas]

            print(f"Entrada atual: {entrada_atual}")

            # Variáveis de erro salvas para comparar progresso
            erro1 = 0; erro2 = 0; erro3 = 0; erro4 = 0; erro5 = 0
            # Rodar geração
            if (generation % 5 == 0):
                erro1 = self.run_generation(entrada_atual, resultados_esperados_atual, 0.5)
                print(f"Geração {generation}. Erro médio = {erro1}")
            elif (generation % 5 == 1):
                erro2 = self.run_generation(entrada_atual, resultados_esperados_atual, 0.5)
                print(f"Geração {generation}. Erro médio = {erro2}")
            elif (generation % 5 == 2):
                erro3 = self.run_generation(entrada_atual, resultados_esperados_atual, 0.5)
                print(f"Geração {generation}. Erro médio = {erro3}")
            elif (generation % 5 == 3):
                erro4 = self.run_generation(entrada_atual, resultados_esperados_atual, 0.5)
                print(f"Geração {generation}. Erro médio = {erro4}")
            elif (generation % 5 == 4):
                erro5 = self.run_generation(entrada_atual, resultados_esperados_atual, 0.5)
                print(f"Geração {generation}. Erro médio = {erro5}")

            # Para evitar comparações com 0
            if (generation > 5):
                erro_comparativo1 = erro1 - erro2
                erro_comparativo2 = erro2 - erro3
                erro_comparativo3 = erro3 - erro4
                erro_comparativo4 = erro4 - erro5
                erro_comparativo5 = erro5 - erro1

                if erro_comparativo1 < min_error_difference:
                    if erro_comparativo2 < min_error_difference:
                        if erro_comparativo3 < min_error_difference:
                            if erro_comparativo4 < min_error_difference:
                                if erro_comparativo5 < min_error_difference:
                                    min_error_found = True

            # Próxima geração
            generation = generation + 1

        print(f"Finish running network")


                


        
        


#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
#_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
