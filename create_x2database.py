import sqlite3

location = 'data/'
database = 'x2cfmap.db'
con = sqlite3.connect(f"./{location}{database}")
cursor = con.cursor()


cursor.execute("""create table if not exists temperature (ROWID integer primary key autoincrement, celsius float, fahrenheit float, datetime text)""")

