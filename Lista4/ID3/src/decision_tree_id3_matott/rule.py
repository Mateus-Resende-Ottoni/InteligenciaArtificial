
# Determinação de classe para regras
class DecisionRule:
    def __init__(self, attribute, information_gain, data, data_results, level):
        # Nome da coluna determinante
        self.attribute = attribute
        # Ganho de informação
        self.information_gain = information_gain
        # Matriz de dados usada
        self.data = data
        # Coluna de resultados usada
        self.data_results = data_results
        # Altura na árvore
        self.level = level
        
        # N de instancias na matriz
        self.data_n = len(data)
        # N de cada resultado da matriz (lista)
        # Se der errado fazer um for
        resultados = list(set(data_results))
        # Para cada valor em resultados, contar quantos tem e salvar em result_ns
        maior_frequencia = -1
        maior_resultado = ""
        self.result_ns = []
        for resultado in resultados:
            frequencia = 0
            for instancia in data_results:
                if instancia == resultado:
                    frequencia = frequencia + 1
            if (frequencia > maior_frequencia):
                maior_frequencia = frequencia
                maior_resultado = resultado
            self.result_ns.append(Cell(resultado, frequencia))
        # Resultado predominante
        self.result = maior_resultado
        self.result_frequencia = maior_frequencia
        # Conexões com regras abaixo
        self.connections = []

    def __str__(self):
        resultados = ""
        for resultado in self.result_ns:
            resultados = resultados + "/" + resultado.name + " " + str(resultado.frequency) + "/"
        return (f"{self.level} - {self.result} ({resultados}) | Informacao: {self.information_gain} | Regra derivada: {self.attribute}")

# Conexão entre regras
class Connection:
    def __init__(self, result_name):
        self.result_name = result_name
        self.rule = None

# Célula
class Cell:
    def __init__(self, name, frequency):
        self.name = name
        self.frequency = frequency