"Outcome class"
"""
from Team import Team
"""    

class Outcome:
    def __init__(self):
        pass

class Tie(Outcome):
    def __init__(self):
        pass

class Determined(Outcome):
    def __init__(self,victor,looser):
        self.winner = victor
        self.looser = looser

    def get_winner(self):
        return self.winner
    def get_looser(self):
        return self.looser