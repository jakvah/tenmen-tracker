# python 3
# from urllib.request import Request, urlopen

# Python 2
import urllib2

from bs4 import BeautifulSoup as bs

if __name__ == "__main__":
    from Match import Match
    from Player import Player
    from Team import Team
else:
    from match_extraction.Match import Match
    from match_extraction.Outcome import Tie, Determined
    from match_extraction.Team import Team
    from match_extraction.Player import Player

# Take match id from popflash site and return a match instance
def get_match_data(match_id):
    match_url = create_url(match_id)
    page_html = get_html(match_url)
    soup = bs(page_html,"html.parser")
    
    team_1_score = soup.find("div", {"class": "score-1"}).text.strip()
    team_2_score = soup.find("div", {"class": "score-2"}).text.strip()

    tables = soup.findAll("table")

    team_2_table_rows = tables[4].findAll("tr")
    team_1_table_rows = tables[0].findAll("tr")
    team2 = rows_to_team(team_2_table_rows)
    team1 = rows_to_team(team_1_table_rows)
    
    team1.set_score(team_1_score)
    team2.set_score(team_2_score)

    match = Match(match_id,team1=team1,team2=team2)

    return match

def create_url(match_id):
    return "https://popflash.site/match/" + str(match_id)
    
def rows_to_team(team_rows):
    team = Team()
    for i in range(1,len(team_rows)):
        columns = team_rows[i].findAll("td")
        popflash_id = get_popflash_id(columns)
        
        player = Player(popflash_id)
        player.set_nick(columns[0].text.strip())
        player.set_kills(columns[1].text.strip())
        player.set_assists(columns[2].text.strip())
        player.set_deaths(columns[3].text.strip())
        player.set_flash_assists(columns[4].text.strip())
        player.set_adr(columns[5].text.strip())
        player.set_hltv_rating(columns[6].text.strip())
        player.set_hs_percentage(columns[7].text.strip())
        player.set_clutch_kills(columns[8].text.strip())
        player.set_bombs_planted(columns[9].text.strip())
        player.set_bombs_defused(columns[10].text.strip())
        
        team.add_player(player)

    return team

def get_popflash_id(columns):
    pop_id_link = str(columns[0].find("a"))
    temp = pop_id_link.split('"')
    pop_id_userlink = temp[1].split("/")
    pop_id = pop_id_userlink[2]
    return pop_id

def get_html(url):
    if not url_exists(url):
        print("u need to add error handling here")
    else:
        req =  Request(url,headers={'User-Agent': 'Mozilla/5.0'})
        page_html = urlopen(req).read()
    return page_html

def get_html_2_7(url):
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    con = urllib2.urlopen( req )
    return con.read()

def url_exists(url):
    return True

if __name__ == "__main__":
    match_id = str(input("matchid:"))
    url = create_url(match_id)
    h = get_html_2_7(url)
    print(h)
    

        