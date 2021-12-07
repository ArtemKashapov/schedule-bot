from db_utils import Database

db = Database()

users = db.get_all()
print(users)

db.close_all()