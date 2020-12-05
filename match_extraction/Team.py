"Team class"
"""
from Player import Player
"""

class Team:
    def __init__(self,p1=None,p2=None,p3=None,p4=None,p5=None,size=5,score=0):
        self.iterator_value = 1
        self.size = size

        self.player_1 = p1
        self.player_2 = p2
        self.player_3 = p3
        self.player_4 = p4
        self.player_5 = p5

        self.score = score
    
    def __iter__(self):
        return self
    def __next__(self):
        if self.iterator_value > self.size:
            self.iterator_value = 1
            raise StopIteration
        
        if self.iterator_value == 1:
            player_to_return = self.player_1
        elif self.iterator_value == 2:
            player_to_return = self.player_2
        elif self.iterator_value == 3:
            player_to_return = self.player_3
        elif self.iterator_value == 4:
            player_to_return = self.player_4
        elif self.iterator_value == 5:
            player_to_return = self.player_5
        self.iterator_value += 1

        return player_to_return
    next = __next__  # python2.x compatibility.       

    def add_player(self,new_player):
        if self.player_1 is None and not self.is_in_team(new_player):
            self.player_1 = new_player
        elif self.player_2 is None and not self.is_in_team(new_player):
            self.player_2 = new_player
        elif self.player_3 is None and not self.is_in_team(new_player):
            self.player_3 = new_player
        elif self.player_4 is None and not self.is_in_team(new_player):
            self.player_4 = new_player
        elif self.player_5 is None and not self.is_in_team(new_player):
            self.player_5 = new_player
    
    def set_score(self,score):
        self.score = score
    def get_score(self):
        return self.score

    def __str__(self):
        return_string = "Team consists of players: \n"
        for p in self:
            return_string += (str(p) + "\n")
        return return_string

    def is_in_team(self,new_player):
        exists = False
        for player in self:
            if player is None:
                continue
            if player == new_player:
                exists = True
        return exists

if __name__ == "__main__":
    p = Player(123,nick="Jakob")
    p2 = Player(145,nick="notJakob")
    t = Team()
    t.add_player(p)
    print(t)   
    t.add_player(p2)
    print(t)
    t.add_player(p2)
    t.add_player(p2)
    t.add_player(p2)
    t.add_player(p2)
    t.add_player(p2)
    t.add_player(p2)

    print(t)        

                
        
        
        
        