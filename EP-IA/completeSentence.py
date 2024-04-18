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
    # modelo geral:
    # estado: tupla de palavras correspondendo à frase parcial (tupla de strings)
    # ações: palavras (strings)
    # transição: concatenar ação ao estado atual
    # estados-meta: estados terminados no marcador de fim de frase
    # custo: como pedido no enunciado
    def initialState(self):
        """
        Deve retornar uma tupla contendo N marcadores de sentença.
        """
        # assumimos que a frase inicial ja vem tratada
        # self.frase_inicial = self.BOS_mark+self.frase_inicial+self.EOS_mark
        # convertemos em tupla de strings
        return tuple(self.frase_inicial.split())
    def isGoal(self, estado):
        """
        Testa se estado é um final de frase.
        """
        # só checa o final do estado
        return estado[-1].strip() == "</s>"
    def actions(self, estado):
        """
        Retorna a lista de ações aplicáveis a estado.
        """
        # pegamos o vocabulário, removemos o marcador
        # auxiliar <QUEBRA> e incluímos o marcador
        # auxiliar </s> para permitir que terminemos frases
        total_actions = self.vocabulary.copy()
        total_actions.remove("<QUEBRA>")
        total_actions.add("</s>")

        # dada todas as ações possíveis, retornamos apenas 
        # aquelas que levam a um estado possível (i.e. cujo n-grama final aparece no texto)
        return [action for action in total_actions if self.n_grams[self.result(estado, action)[-self.N:]] > 0]
    def result(self, estado, acao):
        """
        Retorna o estado resultante de aplicar acao em estado
        """
        # só concatena a ação
        return estado + (acao, )
    def cost(self, estado1, acao, estado2):
        """
        retorna o -log da probabilidade de ir de estado1 para estado2 aplicando acao.
        """
        # implementado como pedido.
        # (n-1)-grama no final da frase parcial atual
        final_n2gram = estado1[-self.N2:]
        # n-grama no final da frase parcial após a ação
        final_ngram = estado2[-self.N:]
        # fórmula fornecida no enunciado
        return -math.log(self.n_grams[final_ngram]/self.n_grams_smaller[final_n2gram])
    

