import sqlite3

con = sqlite3.connect('database.db')
cr = con.cursor()

cr.execute("create table if not exists accounts (username TEXT, password TEXT, admin TEXT)")

rows = [['shreeja', 'shreeja@123', 'no'], 
        ['paramesh', 'paramesh@123', 'no'],
        ['chinna','chinna@123','yes']]

for row in rows:
    cr.execute("insert into accounts values (?,?,?)", row)
    con.commit()
