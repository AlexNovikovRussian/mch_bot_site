import os 

print(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")), 
"db.sqlite3"))
