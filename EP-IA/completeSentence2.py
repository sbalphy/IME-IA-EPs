import math
from UpperClasses import Problem, LanguageModel

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
    # modelo geral, ligeiramente modificado:
    # guardamos a probabilidade de uma frase parcial no seu estado como forma de memoização
    # idealmente para legibilidade só implementariamos uma classe Estado, mas para não mudar muito o programa evitei
    # estado é representado como um par consistindo em:
    # (tupla de palavras correspondendo à frase parcial (tupla de strings), negativo da log-probabilidade da frase parcial (float))
    # ações: palavras (strings)
    # transição: concatenar ação à frase parcial do estado atual e computar nova log-prob
    # estados-meta: estados cuja frase parcial termina no marcador de fim de frase
    # custo: como pedido no enunciado
    def initialState(self):
        """
        Deve retornar uma tupla contendo N marcadores de sentença.
        """
        # assumimos que a frase inicial ja vem tratada
        # self.frase_inicial = self.BOS_mark+self.frase_inicial+self.EOS_mark
        # convertemos em tupla de strings, inicializamos a frase com prob 0
        return (tuple(self.frase_inicial.split()), 0)
    def isGoal(self, estado):
        """
        Testa se estado é um final de frase.
        """
        # só checa o final da frase
        frase_parcial = estado[0]
        return frase_parcial[-1].strip() == "</s>"
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
        frase_parcial = estado[0]
        return [action for action in total_actions if self.n_grams[frase_parcial[-self.N2:] + (action, )] > 0]
    def result(self, estado, acao):
        """
        Retorna o estado resultante de aplicar acao em estado
        """
        # concatena a ação à frase parcial
        frase_parcial = estado[0]
        frase_parcial_nova = frase_parcial + (acao, )

        # assumindo que já conhecemos a probabilidade da frase parcial no estado inicial,
        # a probabilidade da frase parcial no estado após a ação é só a probabilidade da do estado inicial
        # multiplicada pela probabilidade de transição da ação, que já estavamos computando antes para o custo

        # computamos a mesma log-probabilidade condicional que na outra classe
        # (n-1)-grama no final da frase parcial atual
        final_n2gram = frase_parcial[-self.N2:]
        # n-grama no final da frase parcial após a ação
        final_ngram = frase_parcial_nova[-self.N:]
        # fórmula fornecida no enunciado
        transition_log_prob = -math.log(self.n_grams[final_ngram]/self.n_grams_smaller[final_n2gram])

        # já que tomamos o log, a log-probabilidade do novo estado é a soma da log-probabilidade do estado antigo
        # com a log-probabilidade de transição
        log_prob = estado[1] + transition_log_prob
        return (frase_parcial_nova, log_prob)
    
    def cost(self, estado1, acao, estado2):
        """
        retorna a perplexidade do estado2.
        """
        # estado2 contêm informação sobre a sua log-probabilidade (obtida a partir de self.result(estado1, acao))
        # basta processar essa informação em perplexidade
        frase_parcial_final = estado2[0]
        log_prob_final = estado2[1]

        return log_prob_final / len(frase_parcial_final)
    

