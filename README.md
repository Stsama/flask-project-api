# create a database in this application:

-flask shell

-from src.database import db
-db.create_all()
-db

# to destroy all your tables 
-db.drop_all()