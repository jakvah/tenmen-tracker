from database_management import db_interaction, database_exceptions
from match_extraction import popflash_scraper as ps


def main():
    
    pop_id = int(input("Match_ID"))
    pop_match = ps.get_match_data(pop_id)
    print(pop_match.team_1)
    print(pop_match.team_2)
    """
    print("Adding match to database")
    conn = db_interaction.get_database_connection()
    db_interaction.add_match_data(conn,pop_match)
    print("Done")
    """
    
   
main()