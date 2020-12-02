from database_management import *
from match_extraction import popflash_scraper as ps


def main():
    pop_id = int(input("Match_ID"))
    pop_match = ps.get_match_data(pop_id)
    print(pop_match.team_1)
    print(pop_match.team_2)

main()