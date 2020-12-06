"Player class"

class Player:
    def __init__(self,pop_id,nick="",kills=0,deaths=0,assists=0,f_assists=0,adr=0,hltv_rating=0,hs_percentage=0,ck=0,bombs_planted=0,bombs_defused=0,wins=0,losses=0,img_url=""):
        self.popflash_id = pop_id
        self.nick_name = nick

        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.flash_assists =f_assists
        self.adr = adr
        self.hltv_rating = hltv_rating
        self.hs_percentage = hs_percentage
        self.clutch_kills = ck
        self.bombs_planted = bombs_planted
        self.bombs_defused = bombs_planted
        
        self.wins = wins
        self.losses = losses
        self.img_url = img_url
        
        try:
            self.kd_ratio = self.kills / self.deaths
        except ZeroDivisionError:
            self.kd_ratio = 0
    
    def __eq__(self,other):
        return self.popflash_id == other.popflash_id        

    # Setters
    def set_nick(self,nick):
        self.nick_name = nick
    def set_kills(self,kills):
        self.kills = kills
    def set_deaths(self,deaths):
        self.deaths = deaths
    def set_assists(self,assists):
        self.assists = assists
    def set_flash_assists(self,f_assists):
        self.flash_assists = f_assists
    def set_adr(self,adr):
        self.adr = adr
    def set_hltv_rating(self,rating):
        self.hltv_rating = rating
    def set_hs_percentage(self,hs_per):
        self.hs_percentage = hs_per
    def set_clutch_kills(self,ck):
        self.clutch_kills = ck
    def set_bombs_planted(self,bp):
        self.bombs_planted = bp
    def set_bombs_defused(self,bd):
        self.bombs_defused = bd
    def set_wins(self,wins):
        self.wins = wins
    def set_losses(self,losses):
        self.losses = losses
    def set_kd_ratio(self,kd_ratio):
        self.kd_ratio = kd_ratio
    def set_img_url(self,img_url):
        self.img_url = img_url

    # Getters
    def get_pop_id(self):
        return self.popflash_id
    def get_nick(self):
        return self.nick_name
    def get_kills(self):
        return self.kills
    def get_deaths(self):
        return self.deaths
    def get_assists(self):
        return self.assists
    def get_flash_assists(self):
        return self.flash_assists
    def get_adr(self):
        return self.adr
    def get_hltv_rating(self):
        return self.hltv_rating
    def get_hs_percentage(self):
        return self.hs_percentage
    def get_clutch_kills(self):
        return self.clutch_kills
    def get_bombs_planted(self):
        return self.bombs_planted
    def get_bombs_defused(self):
        return self.bombs_defused
    def get_kd_ratio(self):
        return self.kd_ratio
    def get_wins(self):
        return self.wins    
    def get_losses(self):
        return self.losses
    def get_img_url(self):
        return self.img_url

    def __str__(self):
        try:
            return "ID: " + str(self.popflash_id) + ", Nick: " + str(self.nick_name)
        except UnicodeEncodeError: 
            return "ID: " + str(self.popflash_id) + ", Nick: " + str(self.nick_name[1:])


    

    
        
