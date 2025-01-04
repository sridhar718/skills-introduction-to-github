import sqlite3

con = sqlite3.connect('database.db')
cr = con.cursor()

cr.execute("create table if not exists data (member TEXT, project TEXT)")

rows = [['paramesh', 'project1'], 
        ['paramanand', 'project2'], 
        ['person3', 'project3'], 
        ['person4', 'project4'], 
        ['person5', 'project5']]

for row in rows:
    cr.execute("insert into data values (?,?)", row)
    con.commit()