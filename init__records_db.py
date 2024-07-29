import os
import psycopg2

#conn = psycopg2.connect(host='localhost',dbname='records', port=5432)
con = psycopg2.connect(user="yqercigvpu", password="0ANXei8$DZrty$j2", host="demoapi.postgres.database.azure.com", port=5432, database="postgres")
# Open a cursor to perform database operations
cur = conn.cursor()


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


conn.commit()

cur.close()
conn.close()
