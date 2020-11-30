from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
from Match import Match
from Player import Player
from Team import Team

def create_url(math_id):
    return "http://popflash.site/match/" + str(math_id)

# Take match url from popflash site and return a match instance
def get_match_data(math_url):
    page_html = get_html(math_url)
    soup = bs(page_html,"html.parser")
    
    team_1_score = soup.find("div", {"class": "score-1"}).text.strip()
    team_2_score = soup.find("div", {"class": "score-2"}).text.strip()

    tables = soup.findAll("table")


    team_2_table_rows = tables[4].findAll("tr")
    team_1_table_rows = tables[0].findAll("tr")
    team2 = rows_to_team(team_2_table_rows)
    team1 = rows_to_team(team_1_table_rows)

    print("team2:",team2)
    print("team1:",team1)
    print("team2 points: ",team_2_score)
    print("team1 points: ",team_1_score)
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

def url_exists(url):
    return True

if __name__ == "__main__":
    math_id = str(input("mathid:"))
    url=create_url(math_id)
    get_match_data(url)

        