"Outcome class"

from Team import Team
class Outcome:
    def __init__(self):
        pass

class Tie(Outcome):
    def __init__(self):
        pass

class Determined(Outcome):
    def __init__(self,victor,loser):
        self.victor = victor