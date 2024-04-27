    # estado é uma tupla com a frase parcial inteira, ação é uma palavra à ser concatenada à frase parcial
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
