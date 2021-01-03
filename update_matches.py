"""
Function used to update database of existing matches
"""

from database_management import db_interaction as dbi
from match_extraction.Match import Match
from match_extraction import popflash_scraper as ps

def update_matches(startmatch=0):
    conn = dbi.get_database_connection()
    matches = dbi.get_table_data(conn,"matches")
    count = 0
    for row in matches:
        if count < startmatch:
            count += 1
            continue
        match_id = int(row[0])
        print("Getting data for match",match_id)
        m = ps.get_match_data(match_id)
        print("Updating data for match",match_id)
        dbi.update_match_data(m)

    print("Done!")

# Remove weekday from match date column
def update_match_dates():
    pass
if __name__ == "__main__":
    #update_matches()
    m = ps.get_match_data(1125941)
    dbi.update_match_data(m)