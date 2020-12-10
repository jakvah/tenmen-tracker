"Match class"

from Outcome import Tie, Determined

class Match:
    def __init__(self,match_id,team1=None,team2=None,map_img_url="",date=""):
        self.match_id = match_id
        self.team_1 = team1
        self.team_2 = team2

        self.outcome = self.determine_outcome(self.team_1,self.team_2)
        self.map_img_url = map_img_url
        self.date = date

    def determine_outcome(self,team1,team2):
        if team1.get_score() > team2.get_score():
            return Determined(victor=team1,looser=team2)
        elif team1.get_score() < team2.get_score():
            return Determined(victor=team2,looser=team1)
        else:
            return Tie()
    def is_tie(self):
        return self.team_1.get_score() == self.team_2.get_score()
         
    # Getters
    def get_winner(self):
        return self.outcome.get_winner()
    def get_looser(self):
        return self.outcome.get_looser()
    def get_match_id(self):
        return self.match_id
    def get_outcome(self):
        return self.outcome
    def get_map_img_url(self):
        return self.map_img_url
    def get_date(self):
        return self.date

    # Setters
    def set_map_img_url(self,map_img_url):
        self.map_img_url = map_img_url
    def set_date(self,date):
        self.date = date

        