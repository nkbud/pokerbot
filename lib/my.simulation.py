if __name__ == "__main__":
    ranks = Ranks()
    
    preflop = Preflop()
    print(preflop.string())
    flop = Flop(preflop=preflop)
    print(flop.string())
    turn = Turn(flop=flop)
    print(turn.string())
    river = River(turn=turn)
    print(river.string())