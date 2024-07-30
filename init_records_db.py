import os
import psycopg2

con = psycopg2.connect(user=os.environ.get("PGUSER"), password=os.environ.get("PGPASSWORD"), host=os.environ.get("PGHOST"), port=5432, database=os.environ.get("PGDATABASE"))

# Open a cursor to perform database operations
cur = con.cursor()
#Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS records;')
cur.execute('CREATE TABLE records (id serial PRIMARY KEY,'
                                 'todo varchar (150) NOT NULL,'
                                 'description varchar (150));'
                                 )
# Insert data into the table
cur.execute("INSERT INTO records (todo, description) VALUES (%s, %s);", ('Hire','Hire a Product Manager'))
cur.execute("INSERT INTO records (todo, description) VALUES (%s, %s);", ('Fire','Fire the Product Owner'))
cur.execute("INSERT INTO records (todo, description) VALUES (%s, %s);", ('Holidays Next Week','Go to Berlin'))

con.commit()
cur.close()
con.close()
