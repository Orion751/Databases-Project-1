# You will require Connector/Python to use this program.
# See this link for more details: https://dev.mysql.com/doc/connector-python/en/connector-python-installation.html
# Alternatively, you can utilize the Conda package manager. It's best to get acquainted with it now.

#MAKE SURE YOU CONNECT TO NJIT'S NETWORK VIA VPN! It won't work otherwise!

import mysql.connector
from mysql.connector import errorcode
import re

# User supplies username and password via Standard Input

uname=raw_input("Please enter your username for NJIT's MySQL database: ")
pword=raw_input("Please enter your password for NJIT's MySQL Database: ")

# Orion751's contribution: Converts output of a curse object to a human-readable string
def parseTable(curse):
    delim = ","
    temp = ""
    p = re.compile('\)$')

    for i in curse:
        temp += p.sub("", (str(i) + "\n").replace("(u'", "'").replace("', u'", "'" + delim + " '"))

    return temp

# As this is a simple proof-of-concept, everything is defined in this one function. We'll break it up as time goes on.

def initialize():

    try:
        # Connect to the database, create a Cursor, and try to create a table. Catch the exception if it already exists.
        cnx = mysql.connector.connect(user=uname, password=pword, host='sql2.njit.edu', database=uname)
        curse = cnx.cursor()
        mediaDBname = uname + "MediaDB"
        print("The program will now automatically create the DB.\n")

        # The statement below creates the database.
        try:
            curse.execute("CREATE TABLE `" + mediaDBname + "` (`Title` VARCHAR(225), `Medium` VARCHAR(225), `Rating` VARCHAR(2)) ENGINE=InnoDB")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("The database already exists. Continuing to next step.\n")


        cmdVar=""
        print("\nThe database has been created and is now ready for operation.")
        while True:

            print("Please input a command. ( ADD, REMOVE, VIEW, DELETE_TABLE, QUIT )")
            cmdVar = raw_input("Come on, don't be shy!\n\n").upper()

            if (cmdVar==("ADD")):
                print("Please answer the following prompts.\n\nEnter \"QUIT-NOW\" to cancel the ADD operation.")
                titleTemp=raw_input("What is the title of the work? ")
                mediaTemp=raw_input("What medium is it?")
                ratingTemp=raw_input("How would you rate the work? (1-10)")
                curse.execute("INSERT INTO `" + mediaDBname + "` (Title, Medium, Rating) VALUES (%s, %s, %s)", (titleTemp, mediaTemp,ratingTemp))
                cnx.commit()
                continue

            if (cmdVar=="VIEW"):
                curse.execute("SELECT * FROM " + mediaDBname)
                print(parseTable(curse))

            if (cmdVar=="REMOVE"):
                print("Please answer the following prompts.\n\nEnter \"QUIT-NOW\" to cancel the REMOVE operation.")
                titleTemp = raw_input("What is the title of the work you wish to remove? ")
                mediaTemp = raw_input("What medium is it?")
                curse.execute("DELETE FROM " + mediaDBname + " WHERE Title=%s AND Medium=%s", (titleTemp,mediaTemp))
                cnx.commit()

            if (cmdVar=="DELETE_TABLE"):
                confirm = raw_input("Are you sure? Deleting the table will erase your entire database! (yes/n) \n")
                if (confirm=="yes"):
                    curse.execute("DROP TABLE " + mediaDBname)
                    print("Table cleared.")

            if (cmdVar=="QUIT"):
                break

        result=curse.fetchall()
        for row in result:
            print(row[0])

        cnx.close()
        curse.close()


    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Please check your username and password. Alternatively, connect to NJIT's network via VPN.")

    else:
        cnx.close()

initialize()
