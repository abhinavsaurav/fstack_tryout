import psycopg2

conn = psycopg2.connect('dbname=example user=postgres password=password')

# cursor= connection.cursor()
cur = conn.cursor()

# drop any existing todos table
cur.execute("DROP TABLE IF EXISTS todos;")

# (re)create the todos table
# (note: triple quotes allow multiline text in python)

cur.execute("""
  CREATE TABLE todos (
    id serial PRIMARY KEY,
    description VARCHAR NOT NULL
  );
""")


cur.execute('insert into todos(id,description) values(%s,%s);',(1,"No Way"))

dict1 ={'id':2,'descr':"hello world"}

sql = 'insert into todos(id,description) values (%(id)s, %(descr)s);'
cur.execute(sql, dict1)

cur.execute('insert into todos(id,description) values(%s,%s);',(3,"No Way"))
cur.execute('insert into todos(id,description) values(%s,%s);',(4,"OH Way"))
cur.execute('insert into todos(id,description) values(%s,%s);',(5,"My Way"))

cur.execute('select * from todos');
result1=cur.fetchone()
result2=cur.fetchmany(2)
result=cur.fetchall()
print("result1:", result1,"---result2---",result2,"--result3---",result)






# commit, so it does the executions on the db and persists in the db
conn.commit()

cur.close()
conn.close()