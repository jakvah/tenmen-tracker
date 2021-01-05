"Match class"

from Outcome import Tie, Determined

class Match:
    def __init__(self,match_id,team1=None,team2=None,map_img_url="",date="",map_name=""):
        self.match_id = match_id
        self.team_1 = team1
        self.team_2 = team2

        self.outcome = self.determine_outcome(self.team_1,self.team_2)
        self.map_img_url = map_img_url
        self.date = date
        self.map = map_name

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
    def get_map(self):
        return self.map
    def get_team_1(self):
        return self.team_1
    def get_team_2(self):
        return self.team_2

    # Setters
    def set_map_img_url(self,map_img_url):
        self.map_img_url = map_img_url
    def set_date(self,date):
        self.date = date
    def set_map(self,map_name):
        self.map = map_name

    # Kings of match functions
    def get_highest_rated(self):
        hrp_1 = self.team_1.get_highest_rated()
        hrp_2 = self.team_2.get_highest_rated()
        if hrp_1.get_hltv_rating() >= hrp_2.get_hltv_rating():
           return hrp_1
        else:
            return hrp_2
    def get_highest_flash(self):
        hrf_1 = self.team_1.get_highest_flash_assist()
        hrf_2 = self.team_2.get_highest_flash_assist()
        if hrf_1.get_flash_assists() >= hrf_2.get_flash_assists():
            return hrf_1
        else:
            return hrf_2
    def get_highest_adr(self):
        hradr_1 = self.team_1.get_highest_adr()
        hradr_2 = self.team_2.get_highest_adr()
        if int(hradr_1.get_adr()) >= int(hradr_2.get_adr()):
            return hradr_1
        else:
            return hradr_2
    def get_highest_ck(self):
        hrck_1 = self.team_1.get_highest_ck()
        hrck_2 = self.team_2.get_highest_ck()
        if hrck_1.get_clutch_kills() >= hrck_2.get_clutch_kills():
            return hrck_1
        else:
            return hrck_2
    
    def get_highest_hs(self):
        hrhs_1 = self.team_1.get_highest_hs()
        hrhs_2 = self.team_2.get_highest_hs()
        if hrhs_1.get_hs_percentage() >= hrhs_2.get_hs_percentage():
            return hrhs_1
        else:
            return hrhs_2
    
    def get_highest_assists(self):
        ha1 = self.team_1.get_highest_assists()
        ha2 = self.team_2.get_highest_assists()
        if ha1.get_assists() >= ha2.get_assists():
            return ha1
        else:
            return ha2

    def get_highest_bp(self):
        hbp1 = self.team_1.get_highest_bp()
        hbp2 = self.team_2.get_highest_bp()
        if hbp1.get_bombs_planted() >= hbp2.get_bombs_planted():
            return hbp1
        else:   
            return hbp2

    def get_highest_bd(self):
        hbd1 = self.team_1.get_highest_bd()
        hbd2 = self.team_2.get_highest_bd()
        if hbd1.get_bombs_defused() >= hbd2.get_bombs_defused():
            return hbd1
        else:
            return hbd2
    
        
        