"""
Module for interacting with the database
"""
import MySQLdb
import os.path

DATABASE_LOGIN_DETAILS = {
	"host":"localhost",
	"user":"root",
	"password":"jakob",
	"database":"points"
}

def get_database_connection():
    try:
        db_conn = MySQLdb.connect(DATABASE_LOGIN_DETAILS["host"],DATABASE_LOGIN_DETAILS["user"],DATABASE_LOGIN_DETAILS["password"],DATABASE_LOGIN_DETAILS["database"])
        return db_conn
    except Exception as e:
        print("Could not establish connection to the database. Is the server running?")
        return None

def table_exists(dbcon,tablename):
    	dbcur = dbcon.cursor()
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

if __name__ == "__main__":
    db_conn = get_database_connection()
    print(db_conn)