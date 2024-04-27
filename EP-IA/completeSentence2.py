import math
from UpperClasses import Problem, LanguageModel
from nltk.util import ngrams

class CompleteSentence2(Problem, LanguageModel):
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
        # só checa o final da frase
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
        # aquelas que levam a um estado possível (i.e. cujo n-grama final da frase parcial aparece no texto)
        # ligeiramente modificado, computamos a nova frase parcial explicitamente
        # ao invés de chamar a função result, para evitar calcular a probabilidade
        final_n2gram = estado[-self.N2:]
        return [action for action in total_actions if final_n2gram + (action, ) in self.n_grams]
    def result(self, estado, acao):
        """
        Retorna o estado resultante de aplicar acao em estado
        """
        # só concatena a ação
        return estado + (acao, )

    def cost(self, estado1, acao, estado2):
        """
        retorna a diferença de perplexidade entre o estado1 e o estado2.
        """
        # computamos as perplexidades explicitamente

        # calculamos as log-probabilidades de todos os n-gramas presentes nos estados,
        # menos o primeiro n-grama (que é só marcadores de começo de sentença e portanto tem prob 0),
        # e acumulamos a sua soma
        log_prob_sum_initial = 0
        for n_gram in ngrams(estado1[1:], self.N):
            # (n-1)-grama inicial do n-grama
            n2gram = n_gram[:-1]
            # fórmula fornecida no enunciado
            log_prob_sum_initial += -math.log(self.n_grams[n_gram]/self.n_grams_smaller[n2gram])

        log_prob_sum_final = 0
        for n_gram in ngrams(estado2[1:], self.N):
            # (n-1)-grama inicial do n-grama
            n2gram = n_gram[:-1]
            # fórmula fornecida no enunciado
            log_prob_sum_final += -math.log(self.n_grams[n_gram]/self.n_grams_smaller[n2gram])
        
        # perplexidade é só a soma acumulada dividida pelo tamanho da frase
        perp_initial = log_prob_sum_initial / (len(estado1))
        perp_final = log_prob_sum_final / (len(estado2))
        return perp_final - perp_initial

