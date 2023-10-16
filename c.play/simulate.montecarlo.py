import itertools
import random

import numpy as np

from evaluator.evaluator import Evaluator
from evaluator.eval_card import EvaluationCard
import re

def get_all_cards():
    kinds = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
    suits = ['s','d','h','c']
    return ["".join(sorted(x)) for x in itertools.product(kinds,suits)]

class Simulator:
    """
    Hero + community + random(missing community):
    v1: random(villains) + random(community)
    v2: all(villains in a range) + random(community)

    # arbitrary range weights via random.choices(weights=[])
    v1 helps us rank preflop hands
    v2 helps us fight all villains in a range across a limited set of community cards
    """
    
    def __init__(self):
        self.evaluable = [EvaluationCard.new(card) for card in get_all_cards()]
        self.evaluator = Evaluator()
        self.wins,self.ties,self.trials = 0,0,0
        self.__read_villrange_csv()
    
    def __read_villrange_csv(self):
        self.deal2rank = {}
        with open("config/ranges.csv") as f:
            self.sorted_hands = [line[0:4] for line in f.readlines()]
            for i in range(len(self.sorted_hands)):
                self.deal2rank[self.sorted_hands[i]] = i
    
    def write_villrange_csv(self):
        cards = get_all_cards()
        heros,wins,ties,scores,ints = [],[],[],[],[]
        count = 0
        for combo in itertools.combinations(cards,2):
            combos = sorted(combo)
            hero = "".join(combos)
            hero1,hero2 = EvaluationCard.new(combos[0]),EvaluationCard.new(combos[1])
            win,tie = self.est_win_probability(hero,"",num_trials=(2**15))[0:2]
            heros.append(hero)
            wins.append(round(win,ndigits=8))
            ties.append(round(tie,ndigits=8))
            scores.append(3*win+tie)
            ints.append(f"{hero1},{hero2}")
            print(f"{hero}: {count} / 1326. {round(win,ndigits=3)}")
            count += 1
        
        with open("w.t.l.score.csv","w") as f:
            f.writelines(reversed([f"{heros[i]},{ints[i]},{wins[i]},{ties[i]}\n" for i in np.argsort(scores)]))
    
    def est_win_probability_v2(self,herocards: str,commcards: str,villpctile: float,num_trials=10000):
        self.wins,self.ties,self.trials = 0,0,0
        
        # what cards remain?
        takencards = herocards+commcards
        
        # what villain cards are we up against?
        villrange = self.sorted_hands[0:int(villpctile*len(self.sorted_hands))]
        villcards = [x for x in villrange if x[0:2] not in takencards and x[2:4] not in takencards]
        
        # translate cards into integers
        hero = [EvaluationCard.new(x) for x in re.findall("..",herocards)]
        comm = [EvaluationCard.new(x) for x in re.findall("..",commcards)]
        vills = [[EvaluationCard.new(x) for x in re.findall("..",y)] for y in villcards]
        
        missing = 5-len(comm)
        if missing == 0:
            # fight them all
            for vill in vills:
                self.eval_vill_v2(hero=hero,comm=comm,vill=vill)
            return self.wins/self.trials,self.ties/self.trials
        else:
            # we've got some work to do...
            allcards = get_all_cards()
            
            # for each villain card set, do a certain amount of random-community trials
            numtrials_eachvill = num_trials//len(vills)
            for i in range(len(vills)):
                numtrials_thisvill = 0
                while numtrials_thisvill < numtrials_eachvill:
                    # fill out the community with randomly selected cards from the remaining
                    comm2 = comm[:]
                    takencards2 = takencards[:]
                    while len(comm2) != 5:
                        card = random.choice(allcards)
                        if card not in takencards2 and card not in villcards[i]:
                            takencards2 += card
                            comm2.append(EvaluationCard.new(card))
                    
                    self.eval_vill_v2(hero,comm2,vills[i])
                    numtrials_thisvill += 1
            
            return self.wins/self.trials,self.ties/self.trials
    
    def est_win_probability(self,herocards: str,commcards: str,num_trials=10000):
        self.wins,self.ties,self.trials = 0,0,0
        
        # translate cards into integers
        hero = [EvaluationCard.new(x) for x in re.findall("..",herocards)]
        comm = [EvaluationCard.new(x) for x in re.findall("..",commcards)]
        
        # remove all known cards from deck
        rem = [x for x in self.evaluable if x not in hero and x not in comm]
        
        # how many missing from the community?
        missing = 5-len(comm)
        
        # perform at least some # of trials
        while self.trials < num_trials:
            
            # shuffle the deck and get as much as we can out of it
            random.shuffle(rem)
            if missing == 0:
                self.eval_vills(hero,comm,rem)
            else:
                for i in range(0,len(rem)-missing,missing):
                    comm2 = comm+rem[i:(i+missing)]
                    rem2 = [x for x in rem if x not in comm2]
                    self.eval_vills(hero,comm2,rem2)
        
        return self.wins/self.trials,self.ties/self.trials
    
    def eval_vill_v2(self,hero: list[int],comm: list[int],vill: list[int]):
        herorank = self.evaluator.evaluate(hero,comm)
        villrank = self.evaluator.evaluate(vill,comm)
        self.trials += 1
        if herorank < villrank:
            self.wins += 1
        elif herorank == villrank:
            self.ties += 1
    
    def eval_vills(self,hero: list[int],comm: list[int],rem: list[int]):
        herorank = self.evaluator.evaluate(hero,comm)
        for i in range(0,len(rem)-2,2):
            vill = rem[i:(i+2)]
            villrank = self.evaluator.evaluate(vill,comm)
            self.trials += 1
            if herorank < villrank:
                self.wins += 1
            elif herorank == villrank:
                self.ties += 1
