    # estado é uma tupla com a frase parcial inteira, ação é uma palavra à ser concatenada à frase parcial
    def cost(self, estado1, acao, estado2):
        """
        retorna a perplexidade do estado2.
        """
        # computamos a perplexidade do estado final explicitamente

        # calculamos as log-probabilidades de todos os n-gramas presentes no estado final,
        # menos o primeiro (que é só marcadores de começo de sentença e portanto tem prob 0),
        # e acumulamos a sua soma
        log_prob_sum = 0
        for n_gram in ngrams(estado2[1:], self.N):
            # (n-1)-grama inicial do n-grama
            initial_n2gram = n_gram[:-1]
            # fórmula fornecida no enunciado
            log_prob_sum += -math.log(self.n_grams[n_gram]/self.n_grams_smaller[initial_n2gram])
        
        # perplexidade é só a soma acumulada dividida pelo tamanho da frase
        # ignoramos padding inicial
        return log_prob_sum / (len(estado2) - self.N2)
