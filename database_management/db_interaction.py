"""
Module for interacting with the database
"""
import MySQLdb
import os.path
from database_exceptions import Error, TablesDoesNotExistError

DATABASE_LOGIN_DETAILS = {
	"host":"localhost",
	"user":"root",
	"password":"mysqlroot123",
	"database":"tenmandb"
}

def get_database_connection():
    try:
        db_conn = MySQLdb.connect(DATABASE_LOGIN_DETAILS["host"],DATABASE_LOGIN_DETAILS["user"],DATABASE_LOGIN_DETAILS["password"],DATABASE_LOGIN_DETAILS["database"])
        return db_conn
    except Exception as e:
        print("Could not establish connection to the database. Is the server running?")
        return None

def add_match_id(dbconn,match_id):
    if not table_exists(dbconn,"matches"):
        raise TablesDoesNotExistError
    else:
        dbcur = dbconn.cursor()
        query = "INSERT INTO " + "matches" + """(match_id) VALUES (%s)"""
        dbcur.execute(query,[match_id])
        db_conn.commit()
        dbcur.close()

def table_exists(dbconn,tablename):
    	dbcur = dbconn.cursor()
    	dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    	if dbcur.fetchone()[0] == 1:
        	dbcur.close()
        	return True

    	dbcur.close()
    	return False

def get_table_length(dbconn, tablename):
	cur = dbconn.cursor()
	sql = "SELECT * FROM " + tablename
	cur.execute(sql)
	dataset = cur.fetchall()
	l = int(len(dataset))
	return l

def get_table_data(dbconn, tablename):
    cur = dbconn.cursor()
    sql = "SELECT * FROM " + tablename
    cur.execute(sql)
    dataset = cur.fetchall()
    cur.close()

    return dataset

def create_table(db_conn,table_name):
    if not table_exists(db_conn,table_name):
        cur = db_conn.cursor()
        sql = "CREATE TABLE 2019_all (kode INT(6), navn VARCHAR(72), uni_kode VARCHAR(7), sted VARCHAR(18),opptakskrav VARCHAR(6),ord_poeng DOUBLE(3,1), ord_poeng_supp DOUBLE(3,1),for_poeng DOUBLE(3,1),for_poeng_supp DOUBLE(3,1))"

        #sql = "INSERT INTO " + "test" + """(id,dato,avg_ph,avg_temp,avg_turb,avg_kond,valid) VALUES (NULL,%s,%s,%s,%s,%s,%s)"""
        #sql = "INSERT INTO " + "test" + """(firstname, middleinitial) VALUES (%s,%s)"""
        cur.execute(sql)
        #cur.execute(sql,[name, initial])
        db_conn.commit()

        cur.close()
        print("Created table",table_name)
    else:
        print("Table",table_name,"already exist")

def exists_in_table(dbconn,tablename,search_item):
    data = get_table_data(dbconn,tablename)
    for i in range(len(data)):
        if search_item == d[i][0]:
            return True

if __name__ == "__main__":
    db_conn = get_database_connection()
    for i in range(3):
        add_match_id(db_conn,i)
    
    d = get_table_data(db_conn,"matches")
    if exists_in_table(db_conn,"matches",1):
        print("fant")
