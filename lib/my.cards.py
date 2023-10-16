import itertools
from typing import List

import numpy as np

from ui.tabular.models import kind2index,suit2index,kind2char,kinds,primes,suitkey,kindkey,numbkey

class Cards:
    """
    Given: ["As","Ks","4h","3h","2h"]
    Kinds: [1,1,0,0,0,0,0,0,0,0,1,1,1]
    Suits: [0,0,3,2]
    Returnable:
      Kindkey: "ABRST"
      Suitkey: "32"
      Handkey: "ABRST.32"
      Numbkey: 2**1 * 3**1 * 31**1 * 37**1 * 41**1 = 282,162
    """
    
    def __init__(self,cardstrs: List[str]):
        self.cardstrs = cardstrs
        self.kinds = np.zeros(13,dtype=np.uint8)
        self.suits: np.ndarray = np.zeros(4,dtype=np.uint8)
        for cardstr in cardstrs:
            self.kinds[kind2index[cardstr[0]]] += 1
            self.suits[suit2index[cardstr[1]]] += 1
    
    def add(self,card: str):
        self.kinds[kind2index[card[0]]] += 1
        self.suits[suit2index[card[1]]] += 1
    
    def suitkey(self) -> str:
        return suitkey(self.suits)
    
    def kindkey(self) -> str:
        return kindkey(self.kinds)
    
    def numbkey(self) -> int:
        return numbkey(self.kinds)
    
    def handkey(self) -> str:
        return "%s.%s"%(self.kindkey(),self.suitkey())
    
    def string(self) -> str:
        return "%-5s | %-5s | %-5s | %-5s"%(self.handkey(),self.numbkey(),self.kindkey(),self.suitkey())
    