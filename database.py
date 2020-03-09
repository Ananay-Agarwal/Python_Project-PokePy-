import sqlite3
con = sqlite3.connect('PokePy.db')
cur = con.cursor()
cur.execute("INSERT INTO Pokemon VALUES('Pikachu', 'ELECTRIC', 'Thunderbolt', 'Iron Tail', 'Thunder', 'ElectroBall', "
            "274, 1)")
con.commit()
cur.close()
con.close()
