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
        frase_inicial = self.BOS_mark+frase_inicial+self.EOS_mark
        n_gramas = generate_n_grams(frase_inicial, self.N)
        return n_gramas[-1]
    def isGoal(self, estado):
        """
        Testa se estado é um final de frase.
        """
        return estado[-1].strip() == "</s>"
    def actions(self, estado):
        """
        Retorna a lista de ações aplicáveis a estado.
        """
        actions = self.vocabulary.copy()
        actions.remove("<QUEBRA>")
        actions.add("</s>")
        return actions
    def result(self, estado, acao):
        """
        Retorna o estado resultante de aplicar acao em estado
        """
        return estado[1:] + (acao, )
    def cost(self, estado1, acao, estado2):
        """
        retorna o -log da probabilidade de ir de estado1 para estado2 aplicando acao.
        """
        return -math.log(self.n_grams[estado2]/self.n_grams_smaller[estado2[:-1]])

