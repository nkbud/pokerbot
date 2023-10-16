class State:
    """
    Encodes an object describing the current game state
    An "equals" operation allows detection of state changes / sequences
    """
    
    def __init__(self):
        self.herocards = ""
        self.commcards = ""
        self.potsize = 0
        pass

