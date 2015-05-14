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
        for i in range(len(self.current_proba)):
            if proba > self.current_proba[i][0]:
                proba -= self.current_proba[i][0]
            else:
                return self.elems[self.current_proba[i][1]]

    def refreshProba(self):
        probas = [[self.proba[i], i] for i in range(len(self.proba))
                  if self.presence[i]]
        total = sum([el[0] for el in probas])
        self.current_proba = [(el[0]/total, el[1]) for el in probas]
