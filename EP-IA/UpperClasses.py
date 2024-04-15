import math
import utils
from collections import Counter

class LanguageModel:
    def print_values(self):
        """
        Essa função será usada apenas como auxiliar para testar se o texto está sendo lido corretamente. Não a modifique.
        """
        print(f"Our vocabulary is made of approximately {len(self.vocabulary)} different words")
        print(f"Our model was made based on {len(self.sentences)} sentences")
        print(f"We have {len(self.n_grams)} instances of {self.N}-grams and {len(self.n_grams_smaller)} instances of {self.N2}-grams")
    def generate_EOS(self):
        """
        Função que retorna uma string contendo a quantidade correta de <s> para serem postos no final da frase.
        """
        return " </s> "
    def generate_BOS(self):
        """
        Retorna uma string contendo a quantidade correta de <s> para o N do modelo
        por exemplo, para N=4, deve retornar "<s> <s> <s>".
        """
        inicio = ""
        for i in range(self.N-1):
            inicio += " <s> "
        return inicio
    def adapt_sentences(self):
        """
        Função responsável por juntar as duas anteriores com as frases presentes no modelo. Não a modifique.
        """
        for index, frase in enumerate(self.sentences):
            self.sentences[index] = self.BOS_mark+frase+self.EOS_mark
    def __init__(self, texto, n):
        self.processado = texto #textos utilizados já estão processados
        self.vocabulary = set(self.processado.split())
        self.sentences = self.processado.split("<QUEBRA>")[:-1]
        self.n_grams = {} #nossos n-gramas serão um dicionário contendo um n-grama e a sua contagem 
        self.n_grams_smaller = {} #n_gramas_menor terá a contagem dos (n-1)-gramas.
        self.N = n
        self.N2 = n-1
        self.BOS_mark = self.generate_BOS() #responsável por gerar o prefixo de começo de frase para o n-grama especificado
        self.EOS_mark = self.generate_EOS() #responsável por gerar o sufixo de final de semana
        self.adapt_sentences() #responsável por juntar as duas linhas anteriores com as frases do texto.
        self.count_n_grams() #responsável por contar os N-gramas e os (N-1)-gramas
        self.print_values()
    def count_n_grams(self):
        """
        Ao final desta função, essas duas variáveis devem conter todos os seus respectivos n-gramas e suas contagens.
        """
        contador = utils.get_empty_counter()
        outro_contador = utils.get_empty_counter()
        for f in self.sentences:
            n_grams = utils.generate_n_grams(f, self.N)
            n_grams_menor = utils.generate_n_grams(f, self.N2)
            contador.update(n_grams)
            outro_contador.update(n_grams_menor)
        self.n_grams = contador
        self.n_grams_smaller = outro_contador

class Problem(object):
    """The abstract class for a formal deterministic and fully observable 
    planning problem. Specialize this class to specify a concrete problem."""

    def __init__(self, initial=None, goal=None, **kwds): 
        self.__dict__.update(initial=initial, **kwds) 
        
    def actions(self, state):        raise NotImplementedError # Available actions at state (return Iterator)
    def result(self, state, action): raise NotImplementedError # Result of applying action in given state (hence a state)
    def isGoal(self, state):         raise NotImplementedError # Tests if given state is a goal
    def cost(self, s, a, s1):        return 1                  # costs of transiting from state s to s' via action a