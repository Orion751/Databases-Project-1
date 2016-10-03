import mysql.connector

connect = mysql.connector.connect(user='mra25', password='tiger', host='sql2.njit.edu', database='mra25')

connect.close()