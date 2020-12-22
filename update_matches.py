from database_management import db_interaction as dbi
from match_extraction.Match import Match
from match_extraction import popflash_scraper as ps


def update_matches():
    conn = dbi.get_database_connection()
    matches = dbi.get_table_data(conn,"matches")
    for row in matches:
        match_id = int(row[0])
        print("Getting data for match",match_id)
        m = ps.get_match_data(match_id)
        print("Updating data for match",match_id)
        dbi.update_match_data(m)

    print("Done!")
if __name__ == "__main__":
    update_matches()