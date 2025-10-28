import math
import random

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
                neuronio_pesos.append( self.random_float() )
            # Append para representar o bias
            neuronio_pesos.append( self.random_float() )
            camada_neuronios.append(neuronio_pesos)
        self.neurons.append(camada_neuronios)

        # Camada de saída
        camada_neuronios = []
        for neuronio in range(saidas):
            neuronio_pesos = []
            for n_meio in range(meio):
                neuronio_pesos.append( self.random_float() )
            # Append para representar o bias
            neuronio_pesos.append( self.random_float() )
            camada_neuronios.append(neuronio_pesos)
        self.neurons.append(camada_neuronios)

# ----- ----- ----- ----- ----- ----- -----
    def random_float(self):
        dezena = random.choice((range(1, 9)))
        #unidade = random.choice((range(0, 9)))

        peso = (dezena*1.0)/10.0

        #print(f"Peso: {peso}")

        return(peso)

# ----- ----- ----- ----- ----- ----- -----

# Para reduzir casas decimais
    def shorten_nums(self, neuronio):
        text = "[|"
        n_pesos = len(neuronio)
        for n in range(n_pesos):
            text = text + f"{round(neuronio[n], 5)}" + "|"
        text = text + "]"
        return(text)

# ----- ----- ----- ----- ----- ----- -----
        
    # Resultados intermediarios
    def instance_intermediario(self, entradas):
        resultados_intermediario = []
        for neuronio in self.neurons[0]:
            soma_atual = 0
            n_entradas = len(entradas)

            # Para cada entrada
            for n in range(n_entradas):
                soma_atual = soma_atual + entradas[n] * neuronio[n]
            #print(f"Soma atual (intermediario) (sem bias): {soma_atual}")
            # Somar bias
            soma_atual = soma_atual + 1 * neuronio[n_entradas]
            #print(f"Soma atual (intermediario): {soma_atual}")

            # Aplicar função de normalização
            soma_atual = 1 / (1 + math.exp(0-soma_atual))
            #print(f"Soma atual (pos normalizacao): {soma_atual}")
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
                #print(f"{resultados_intermediario[n]} * {neuronio[n]}")
                soma_atual = soma_atual + resultados_intermediario[n] * neuronio[n]
            #print(f"Soma atual (saída) (sem bias): {soma_atual}")
            # Somar bias
            soma_atual = soma_atual + 1 * neuronio[n_intermediario]
            #print(f"Soma atual (saída): {soma_atual}")

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
    
# ----- ----- ----- ----- ----- ----- -----

    # Derivadas dos neurônios das camadas em determinadas instâncias
    def instance_derivadas(self, entradas, resultados_intermediario, resultados_saida):
        resultados = []

        # Camada intermediária
        derivadas_intermediario = []
        for resultado in resultados_intermediario:
            derivada = resultado * (1-resultado)
            derivadas_intermediario.append(derivada)

        # Camada de saída
        derivadas_resultados = []
        for resultado in resultados_saida:
            derivada = resultado * (1-resultado)
            derivadas_resultados.append(derivada)

        resultados.append(derivadas_intermediario)
        resultados.append(derivadas_resultados)

        return resultados

# ----- ----- ----- ----- ----- ----- -----

    # Ajustes
    def weight_adjust(self, entradas, resultados_intermediario, erros_intermediario, erros_resultados, taxa):
        #print(f"Start adjusting weight")

        #print(entradas)
        #print(resultados_intermediario)
        #print(erros_intermediario)
        #print(erros_resultados)
        
        # Camada de saída
        for neuronio in range(len(self.neurons[1])):
            #print(f"Neurônio: {self.neurons[1][neuronio]}")

            n_neuronios = len(resultados_intermediario)
            #print(f"N resultados intermediario = {n_neuronios}")

            for n in range(n_neuronios):
                #print(n)
                #print(resultados_intermediario[n])
                #print(erros_resultados[n])

                # Taxa de aprendizado * Entrada neurônio intermediário * Erro do neurônio 
                ajuste = taxa * resultados_intermediario[n] * erros_resultados[neuronio]
                #print(f"{ajuste}")
                self.neurons[1][neuronio][n] = self.neurons[1][neuronio][n] + ajuste
            # Bias
            ajuste = taxa * 1 * erros_resultados[neuronio]
            #print(f"{ajuste}")
            self.neurons[1][neuronio][n_neuronios] = self.neurons[1][neuronio][n_neuronios] + ajuste

        # Camada intermediária
        for neuronio in range(len(self.neurons[0])):
            #print(f"Neurônio: {self.neurons[0][neuronio]}")

            n_neuronios = len(entradas)
            for n in range(n_neuronios):
                # Taxa de aprendizado * Entrada * Erro do neurônio
                ajuste = taxa * entradas[n] * erros_intermediario[neuronio]
                #print(f"{ajuste}")
                self.neurons[0][neuronio][n] = self.neurons[0][neuronio][n] + ajuste
            # Bias
            ajuste = taxa * 1 * erros_intermediario[neuronio]
            #print(f"{ajuste}")
            self.neurons[0][neuronio][n_neuronios] = self.neurons[0][neuronio][n_neuronios] + ajuste
                
        #print(f"Finish adjusting weight")

# ----- ----- ----- ----- ----- ----- -----

    # Uma geração do algoritmo
    def run_generation(self, entradas, resultados_esperados, learning_rate):

        #print(f"Start running generation")


        erro_medio = 0; erro_max = 0
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
        derivadas = self.instance_derivadas(entradas, resultados_intermediario, resultados_obtidos)

        print(f"Entrada Atual: {entradas}")
        print(f"Resultado Esperado: {resultados_esperados}")
        print(f"Resultado Obtido: {resultados_obtidos}")

        # Obter diferença dos resultados desejados pelos obtidos
        for n in range(len(resultados_esperados)):
            #print(n)

            diferenca = resultados_esperados[n] - resultados_obtidos[n]

            # Como queremos calcular MSE, obter o quadrado da diferença
            #diferenca = pow(diferenca, 2)

            # Pelos meus testes, usar a diferença quadrática leva a resultados
            #  desproporcionalmente piores do que não a usar.
            # É provável que isso seja pois estou calculando e ajustando o erro
            #  a cada execução (esqueci o nome desse método em específico)
            # Então manterei o uso da diferença absoluta ao invés da quadrática,
            #  mas fique registrado que é puramente devido a observações pessoais,
            #  a forma certa seria adaptar o código para calcular o erro médio
            #  quadrático após conferir todos os resultados para todas as entradas
            #  e apenas após isso calcular a mudança de peso

            #print(f"Diferença: {diferenca}")
            resultados_diferencas.append(diferenca)

        # Calcular erros na camada de resultados
        erros_resultados = []
        for neuronio in range(len(self.neurons[1])):
            erro_medio = erro_medio + resultados_diferencas[neuronio]
            erro_absoluto = abs(resultados_diferencas[neuronio])
            if (erro_absoluto > abs(erro_max)):
                erro_max = resultados_diferencas[neuronio]

            erro = resultados_diferencas[neuronio] * derivadas[1][neuronio]
            erros_resultados.append(erro)

        # Calcular erros na camada intermediária
        erros_intermediario = []
        # Para cada neurônio na camada intermediária
        for neuronio in range(len(self.neurons[0])):
            #print(self.neurons[0][neuronio])
            somatorio_camada_posterior = 0
            #print(f"len: {len(erros_resultados)}")
            # Somatório de (Peso até neurônio posterior * Erro neurônio posterior)
            for saida in range(len(self.neurons[1])):
                #print(saida)
                #teste = self.neurons[1][saida][neuronio]
                #teste = erros_resultados[saida]

                # Peso do neurônio da camada de saída e respectivo peso da camada intermediária
                #  vezes o erro desse neurônio de saída
                erro_ajustado = self.neurons[1][saida][neuronio] * erros_resultados[saida]
                somatorio_camada_posterior = somatorio_camada_posterior + erro_ajustado
            #erros_intermediario.append(erro)
            erro = somatorio_camada_posterior * derivadas[0][neuronio]
            erros_intermediario.append(erro)

        # Calcular erro médio
        #for erro in erros_intermediario:
        #    n_erros = n_erros + 1
        #    erro_medio = erro_medio + erro
        for erro in erros_resultados:
            #print(f"Erro medio (durante soma): {erro_medio}")
            n_erros = n_erros + 1
            #erro_medio = erro_medio + erro
        #print(f"Erro medio (pré divisão): {erro_medio}")
        erro_medio = erro_medio/n_erros
        #print(f"Erro medio: {erro_medio}")
        

        # Ajuster pesos
        self.weight_adjust(entradas, resultados_intermediario, erros_intermediario, erros_resultados, learning_rate)

        #print(f"Finish running generation")

        return erro_medio, erro_max
        
# ----- ----- ----- ----- ----- ----- -----

    def run_network(self, num_generations, entradas, resultados_esperados, min_error):

        print(f"Start running network\n")

        print(f"Início")
        print(f"Intermediarios: {self.neurons[0]}")
        print(f"Saida: {self.neurons[1]}")
        print(f"\n")

        min_error_found = False
        generation = 1
        n_aleatorio = 0; n_below_min_erro = 0

        n_entradas = len(entradas)
        entrada_atual = entradas[0]
        resultados_esperados_atual = resultados_esperados[0] 

        
        while ( ((generation <= num_generations) or (num_generations == -1)) and (not min_error_found) ):
            # Definir entrada atual (e respectivas saídas)
            # Com base na geração atual
            #entrada_atual = entradas[(generation - 1) % n_entradas]
            #resultados_esperados_atual = resultados_esperados[(generation - 1) % n_entradas]

            # De forma aleatória

            # Intermediário para evitar testes iguais em seguida
            # Não precisa evitar garantidamente, só é bom reduzir a chance
            intermediario = random.choice( range(0, n_entradas) )
            if (intermediario == n_aleatorio):
                n_aleatorio = random.choice( range(0, n_entradas) )
            else:
                n_aleatorio = intermediario
            entrada_atual = entradas[n_aleatorio]
            resultados_esperados_atual = resultados_esperados[n_aleatorio]

            # Rodar geração
            print(f"Geração {generation}")
            erro, erro_max = self.run_generation(entrada_atual, resultados_esperados_atual, 0.5)
            print(f"Erro médio = {erro}")
            print(f"Erro máximo = {erro_max}")

            # Contador de quantas epochs seguidas foram abaixo do mínimo estabelecido
            # Como existe a possibilidade de, no caso de vários neurônios de saída, 
            #  muitos estarem certos mas um estar errado, o erro máximo é para evitar
            #  a grande disparidade que pode ser ofuscada pela média
            if ( ( abs(erro) < min_error ) and ( abs(erro_max) < (min_error*1.5) ) ):
                n_below_min_erro = n_below_min_erro + 1
            else:
                n_below_min_erro = 0

            # Usando como base o número de entradas possíveis
            if (n_below_min_erro >= 2*n_entradas):
                min_error_found = True

            # Próxima geração
            generation = generation + 1
            # Separação de texto entre gerações
            print(f"\n----------\n")

        print(f"Fim")
        print(f"Intermediarios: {self.neurons[0]}")
        print(f"Saida: {self.neurons[1]}")
        print(f"\n")

        print(f"Finish running network")

# ----- ----- ----- ----- ----- ----- -----
                
    # Teste
    def test_network(self, entradas, resultados_esperados):

        print(f"Network test")

        for n in range(len(entradas)):

            # Obter resultado
            resultados_intermediario = self.instance_intermediario(entradas[n])
            resultados_obtidos = self.instance_result(entradas[n], resultados_intermediario)

            print(f"Entrada: {entradas[n]}")
            print(f"Resultado Esperado: {resultados_esperados[n]}")
            print(f"Resultado Obtido: {self.shorten_nums(resultados_obtidos)}")
            print(f"--- --- --- --- --- --- ---")

# ----- ----- ----- ----- ----- ----- -----

    # Teste porém com erros(ruído)
    def test_network_noisy(self, entradas, resultados_esperados, n_erros):

        print(f"Network test")

        for n in range(len(entradas)):

            # Aplicar ruído à entrada
            n_aleatorio = 0
            for e in range(n_erros):
                intermediario = random.choice(range(0, len(entradas[n])))
                # Para evitar aplicar no mesmo
                if (n_aleatorio == intermediario):
                    n_aleatorio = random.choice(range(0, len(entradas[n])))
                else: 
                    n_aleatorio = intermediario

                # Alterar entrada
                if entradas[n][n_aleatorio] == 1:
                    entradas[n][n_aleatorio] = 0
                else:
                    entradas[n][n_aleatorio] = 1

            # Obter resultado
            resultados_intermediario = self.instance_intermediario(entradas[n])
            resultados_obtidos = self.instance_result(entradas[n], resultados_intermediario)

            print(f"Entrada: {entradas[n]}")
            print(f"Resultado Esperado: {resultados_esperados[n]}")
            print(f"Resultado Obtido: {self.shorten_nums(resultados_obtidos)}")
            print(f"--- --- --- --- --- --- ---")#
        
        


#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
#_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
