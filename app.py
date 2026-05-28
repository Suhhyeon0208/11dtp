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
    print(f"name                          speed   max_g climb range payload")
    for aircraft in results:
        print(f"{aircraft[1]:<30} {aircraft[2]:<8} {aircraft[3]:<6} {aircraft[4]:<6}{aircraft[5]:<6} {aircraft[6]:<6}")
    #loop finished here
    db.close()


def print_all_aircraft_by_speed():
    """Print all the aircraft nicely"""
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    sql = "SELECT * FROM aircraft;"
    cursor.execute(sql)
    results = cursor.fetchall()
    #loop through all the results
    print(f"name                          speed   max_g climb range payload")
    for aircraft in results:
        print(f"{aircraft[1]:<30} {aircraft[2]:<8} {aircraft[3]:<6} {aircraft[4]:<6}{aircraft[5]:<6} {aircraft[6]:<6}")
    #loop finished here
    db.close()


def print_all_aircraft_by_g():
    """Print all the aircraft nicely"""
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    sql = "SELECT * FROM aircraft;"
    cursor.execute(sql)
    results = cursor.fetchall()
    #loop through all the results
    print(f"name                          speed   max_g climb range payload")
    for aircraft in results:
        print(f"{aircraft[1]:<30} {aircraft[2]:<8} {aircraft[3]:<6} {aircraft[4]:<6}{aircraft[5]:<6} {aircraft[6]:<6}")
    #loop finished here
    db.close()


def print_all_aircraft_by_climb():
    """Print all the aircraft nicely"""
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    sql = "SELECT * FROM aircraft;"
    cursor.execute(sql)
    results = cursor.fetchall()
    #loop through all the results
    print(f"name                          speed   max_g climb range payload")
    for aircraft in results:
        print(f"{aircraft[1]:<30} {aircraft[2]:<8} {aircraft[3]:<6} {aircraft[4]:<6}{aircraft[5]:<6} {aircraft[6]:<6}")
    #loop finished here
    db.close()

def print_all_aircraft_by_range():
    """Print all the aircraft nicely"""
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    sql = "SELECT * FROM aircraft;"
    cursor.execute(sql)
    results = cursor.fetchall()
    #loop through all the results
    print(f"name                          speed   max_g climb range payload")
    for aircraft in results:
        print(f"{aircraft[1]:<30} {aircraft[2]:<8} {aircraft[3]:<6} {aircraft[4]:<6}{aircraft[5]:<6} {aircraft[6]:<6}")
    #loop finished here
    db.close()

def print_all_aircraft_by_payload():
    """Print all the aircraft nicely"""
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    sql = "SELECT * FROM aircraft;"
    cursor.execute(sql)
    results = cursor.fetchall()
    #loop through all the results
    print(f"name                          speed   max_g climb range payload")
    for aircraft in results:
        print(f"{aircraft[1]:<30} {aircraft[2]:<8} {aircraft[3]:<6} {aircraft[4]:<6}{aircraft[5]:<6} {aircraft[6]:<6}")
    #loop finished here
    db.close()

#main code
while True:
    user_input = input(
        """
        What would you like to do. 
        1. Print all aircraft
        2. Print all aircraft sorted by speed
        3. Print all aircraft sorted by max g force
        4. Print all aircraft sorted by climb
        5. Print all aircraft sorted by range
        6. Print all aircraft sorted by payload
        7. Exit
        """)
    if user_input == "1":
        print_all_aircraft()
    elif user_input == "2":
        print_all_aircraft_by_speed()
    elif user_input == "3":
        print_all_aircraft_by_climb()
    elif user_input == "4":
        print_all_aircraft_by_range()
    elif user_input == "5":
        print_all_aircraft_by_climb()
    elif user_input == "6":
        print_all_aircraft_by_payload()
    elif user_input == "7":
        break
    else:
        print("That was not an option\n")
        