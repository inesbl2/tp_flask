from sqlalchemy import create_engine, text
from faker import Faker
import random
from datetime import datetime

fake = Faker()
db_string = "postgresql://root:root@localhost:5432/test_db"
engine = create_engine(db_string)
connection = engine.connect()

create_table_user= text("""
CREATE TABLE IF NOT EXISTS "User" (
  id SERIAL PRIMARY KEY,
  firstname VARCHAR(255),
  lastname VARCHAR(255),
  age INT,
  email VARCHAR(255),
  job VARCHAR(255)
)
""")
create_table_application= text("""
CREATE TABLE IF NOT EXISTS Application (
  id SERIAL PRIMARY KEY,
  appname VARCHAR(255),
  username VARCHAR(255),
  lastconnection TIMESTAMP,
  user_id INT,
  FOREIGN KEY (user_id) REFERENCES "User"(id)
);""")

def run_query (query):
    with engine.connect() as connection:
      trans = connection.begin()  
      connection.execute(query)
      trans.commit() 

def populate_user ():
  for _ in range(100):
    firstname = fake.first_name()
    lastname = fake.last_name()
    age = random.randrange(15,80)
    email = fake.email()
    job = fake.job().replace("'","")
    insert_user = text(f"""
      INSERT INTO "User" (firstname, lastname, age, email, job)
      VALUES ('{firstname}', '{lastname}', '{age}', '{email}', '{job}')""" )
    run_query(insert_user)
        
def populate_application ():
  apps= ['Facebook','Instagram','TikTok','Twitter']
  for _ in range(100):
    appname = random.choice(apps)
    username = fake.user_name()
    lastconnection = datetime.now()
    user_id = random.randrange(1,100)
    insert_app = text(f"""
      INSERT INTO Application (appname, username, lastconnection, user_id)
      VALUES ('{appname}', '{username}', '{lastconnection}', '{user_id}')""")
    run_query(insert_app)


if __name__ == '__main__' : 
   run_query(create_table_user)
   run_query(create_table_application)
   populate_user()
   populate_application()

