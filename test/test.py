#docstring- Suhhyeon- airb=plane database application
#imports
import sqlite3

#contants and variables
DATABASE = 'task7.db'

#functions
def print_all_aircraft():
    """Print all the aircraft nicely"""
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    sql = "SELECT * FROM aircraft;"
    cursor.execute(sql)
    results = cursor.fetchall()
    #loop through all the results
    for aircraft in results:
        print(aircraft)
    #loop finished here
    db.close()



#main code
print_all_aircraft()