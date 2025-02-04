#poaaible code for the budget table
#Buget table imported from SQL lite database and displayed in a table format on the window
#table with all the transactions
import sqlite3
import pandas as pd
conn = sqlite3.connect('budget.db')
c = conn.cursor()
c.execute('SELECT * FROM budget')
rows = c.fetchall()
df = pd.DataFrame(rows)
conn.commit()
conn.close()
print(df)
tk.table = tk.Label(upe_budget, text=df) #maybe this will work
