import math
from UpperClasses import Problem, LanguageModel

class CompleteSentence(Problem, LanguageModel):
    def __init__(self, texto, n, frase_inicial):
        """
        Função de inicialização do modelo, não a modifique.
        """
        LanguageModel.__init__(self, texto, n)
        self.frase_inicial = frase_inicial
    """
    Daqui para cima são funções relacionadas com preparar o modelo.
    Daqui para baixo são funções relacionadas com a busca.
    """ 
    def initialState(self):
        """
        Deve retornar uma tupla contendo N marcadores de sentença.
        """
        raise NotImplementedError
    def isGoal(self, estado):
        """
        Testa se estado é um final de frase.
        """
        raise NotImplementedError
    def actions(self, estado):
        """
        Retorna a lista de ações aplicáveis a estado.
        """
        raise NotImplementedError
    def result(self, estado, acao):
        """
        Retorna o estado resultante de aplicar acao em estado
        """
        raise NotImplementedError
    def cost(self, estado1, acao, estado2):
        """
        retorna o -log da probabilidade de ir de estado1 para estado2 aplicando acao.
        """
        return -math.log(1)

