from random import random


class RandomBonus:
    def __init__(self, ratios, presence, elems):
        self.proba = ratios
        self.presence = presence
        self.elems = elems
        self.refreshProba()

    def getRandom(self):
        proba = random()
        
        i = 0
        while i < len(self.current_proba)-1 and proba > self.current_proba[i][0]:
            i += 1
            proba -= self.current_proba[i][0]
        return self.elems[self.current_proba[i][1]]

    def refreshProba(self):
        probas = [[self.proba[i], i] for i in range(len(self.proba)) if self.presence[i]]
        total = sum([el[0] for el in probas])
        self.current_proba = [(el[0]/total, el[1]) for el in probas]