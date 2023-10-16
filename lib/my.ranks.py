import itertools
import math
from typing import Dict,List

import numpy as np

from ui.tabular.models import numbkey,kinds,kind2char,kind2index,primes,chars,kindex
from ui.tabular.models.Cards import Cards

class Ranks:
    """
    Iterate through 5-card poker hands in rank order
    Save their unique numbkey --> rank
    If suited, save in the suited[numbkey] --> rank table
    """
    
    def __init__(self):
        self.numbSrank = {}
        self.numbOrank = {}
    
    def nextrank(self):
        return len(self.numbSrank)+len(self.numbOrank)
    
    def build(self):
        # straight flushes
        self.__straights(numb2rank=self.numbSrank)
        # multiples larger than a flush
        self.__multiples([4,1],numb2rank=self.numbOrank)
        self.__multiples([3,2],numb2rank=self.numbOrank)
        # flushes
        self.__multiples([3,1,1],numb2rank=self.numbSrank)
        self.__multiples([2,2,1],numb2rank=self.numbSrank)
        self.__multiples([2,1,1,1],numb2rank=self.numbSrank)
        self.__multiples([1,1,1,1,1],numb2rank=self.numbSrank)
        # straights
        self.__straights(numb2rank=self.numbOrank)
        # multiples smaller than a flush
        self.__multiples([3,1,1],numb2rank=self.numbSrank)
        self.__multiples([2,2,1],numb2rank=self.numbSrank)
        self.__multiples([2,1,1,1],numb2rank=self.numbSrank)
        self.__multiples([1,1,1,1,1],numb2rank=self.numbSrank)
    
    def rank(self,cards: Cards):
        assert np.sum(cards.kinds) == 5
        return self.numbSrank[cards.numbkey()] if any(cards.suits) == 5 else self.numbOrank[cards.numbkey()]
    
    def __multiples(self,multiples: List[int],numb2rank):
        for ks in itertools.product(kindex,repeat=len(multiples)):
            if len(set(ks)) != len(ks):
                continue
            kindcounts = np.zeros(13)
            ms = multiples[:]
            for k in reversed(ks):
                kindcounts[k] = ms.pop()
            numb2rank[numbkey(kindcounts)] = self.nextrank()
    
    def __straights(self,numb2rank):
        num = len("akqjt9876")
        straights = [np.append(np.zeros(i),np.append(np.ones(5),np.zeros(num-i-1))) for i in range(num)]
        for straight in straights:
            numb2rank[numbkey(straight)] = self.nextrank()
        acelow = np.zeros(13)
        acelow[0] = 1
        acelow[len(acelow)-5] = 0
        numb2rank[numbkey(acelow)] = self.nextrank()
    
    @staticmethod
    def __prime_factorize(n: int) -> str:
        """
        Each number has a unique prime factorization. For us that's the card ranks.
        :param n: a prime product
        :return: AAKQJ, the kinds as a string sorted decreasing
        """
        prime2kind = lambda p:chars[[i for i in range(len(primes)) if primes[i] == p][0]]
        kinds = []
        # Print the number of two's that divide n
        while n%2 == 0:
            kinds.append(prime2kind(2))
            n /= 2
        # For each odd number divisor increasing
        for i in range(3,int(math.sqrt(n))+1,2):
            while n%i == 0:
                kinds.append(prime2kind(i))
                n //= i
        # if n is still here, n is prime
        if n > 2:
            kinds.append(prime2kind(n))
        return "".join(reversed(kinds))
    