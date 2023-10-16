import itertools
import random
from typing import List

import numpy as np

from ui.tabular.models import randcard
from ui.tabular.models.Cards import Cards
from ui.tabular.models.Ranks import Ranks

class Preflop:
    def __init__(self,herocardstrs: List[str] = None):
        self.hero = Cards(herocardstrs if herocardstrs else self.random())
    
    def random(self):
        card1 = randcard()
        card2 = randcard()
        while card1 == card2:
            card2 = random.choice
        return [card1,card2]
    
    def string(self):
        return "%-5s|%-10s|%-5s"%(
            "",
            "",
            self.hero.handkey()
        )

class Flop:
    def __init__(self,preflop: Preflop,commcardstrs: List[str] = None):
        self.preflop = preflop
        self.comm = Cards(commcardstrs if commcardstrs else self.random())
    
    def random(self):
        card1 = randcard()
        while card1 in self.preflop.hero.cardstrs:
            card1 = randcard()
        card2 = randcard()
        while card2 in self.preflop.hero.cardstrs or card2 == card1:
            card2 = randcard()
        card3 = randcard()
        while card3 in self.preflop.hero.cardstrs or card3 == card2 or card3 == card1:
            card3 = randcard()
        return [card1,card2,card3]
    
    def string(self):
        return "%-5s|%-10s|%-10s"%(
            "",
            self.preflop.hero.handkey(),
            self.comm.handkey(),
        )

class Turn:
    def __init__(self,flop: Flop,turncardstr: str = None):
        self.flop = flop
        flop.comm.add(turncardstr if turncardstr else self.random())
    
    def random(self):
        card = randcard()
        while card in self.flop.comm.cardstrs or card in self.flop.preflop.hero.cardstrs:
            card = randcard()
        return card
    
    def string(self):
        return "%-5s|%-10s|%-10s"%(
            "",
            self.flop.preflop.hero.handkey(),
            self.flop.comm.handkey()
        )

class River:
    def __init__(self,turn: Turn,rivercard: str = None):
        self.turn = turn
        turn.flop.comm.add(rivercard if rivercard else self.random())
        self.rank = self.minrank()
    
    def random(self):
        card = randcard()
        while card in self.turn.flop.comm.cardstrs or card in self.turn.flop.preflop.hero.cardstrs:
            card = randcard()
        return card
    
    def minrank(self):
        hero = self.turn.flop.preflop.hero
        comm = self.turn.flop.comm
        fives = [combo for combo in itertools.combinations(hero.cardstrs+comm.cardstrs,5)]
        ranks = [Ranks.rank(five) for five in fives]
        return np.minimum(ranks)
    
    def string(self):
        return "%-5s|%-10s|%-10s"%(
            self.rank,
            self.turn.flop.preflop.hero.handkey(),
            self.turn.flop.comm.handkey()
        )
