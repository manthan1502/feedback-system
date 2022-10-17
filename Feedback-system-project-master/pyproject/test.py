import mysql.connector

myconn = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="12345",
  database="studentfeedback"
)

cur=myconn.cursor()
cur.execute("Select * from students;")
data=cur.fetchall()
print(data)