import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="01551703990",
    database="sign_language"
)

cursor = db.cursor()