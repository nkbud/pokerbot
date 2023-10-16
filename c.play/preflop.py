
class Preflop:
    """
    We pre-compute our preflops to help with strategy
    """
    
    sortedstr2preflop = {}
    sortedstr2key = {}
    
    def __init__(self, handstr: str, cardints: (int, int), winprob: float, tieprob: float):
        self.handstr = handstr
        self.cardints = cardints
        self.winprob = winprob
        self.tieprob = tieprob
        self.loseprob = 1 - self.winprob - self.tieprob
        Preflop.sortedstr2preflop[self.handstr] = self
        Preflop.sortedstr2key[self.handstr] = self.getkey()
    
    def getkey(self):
        k1,s1,k2,s2 = self.handstr[0:4]
        return f"{k1}{k2}s" if s1 == s2 else f"{k1}{k2}o"
