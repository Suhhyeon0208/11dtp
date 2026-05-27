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
        print(f"{aircraft[1]} {aircraft[2]} {aircraft[3]} {aircraft[4]}{aircraft[5]} {aircraft[6]}{aircraft[7]}")
    #loop finished here
    db.close()



#main code
print_all_aircraft()