import itertools

import numpy as np

from simulator import Simulator,get_all_cards

if __name__ == "__main__":
    simulator = Simulator()
    print(simulator.est_win_probability_v2(herocards="AsAc",commcards="",villpctile=0.10,num_trials=2**14))