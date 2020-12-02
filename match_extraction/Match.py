"Match class"
from Team import Team
from Outcome import Tie, Determined

class Match:
    def __init__(self,match_id,*,team1=None,team2=None):
        self.match_id = match_id
        self.team_1 = team1
        self.team_2 = team2

        self.match_outcome = determine_outcome
        
    def determine_outcome(self,team1,team2):
        if team1.get_score() > team2.get_score():
            return Determined(victor=team1,loser=team2)
        elif team1.get_score() < team2.get_score():
            return Determined(victor=team2,loser=team1)
        else:
            return Tie()
        