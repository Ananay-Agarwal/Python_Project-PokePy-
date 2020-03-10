import sqlite3
con = sqlite3.connect('PokePy.db')
cur = con.cursor()
cur.execute('''INSERT INTO Moves VALUES
             ('Inferno', 'FIRE', 100)''')
con.commit()
cur.close()
con.close()
