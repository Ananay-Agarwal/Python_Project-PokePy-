import sqlite3
con = sqlite3.connect('PokePy.db')
cur = con.cursor()
cur.execute('''Insert into Moves values(
            "Hurricane" , 'FLYING' , 110)''')
con.commit()
cur.close()
con.close()
