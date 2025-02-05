import sqlite3

class Boat():

    def __init__(self, name: str, id: int , model: str):
        self.name = name
        self.id = id
        self.model = model


class SlapStore():
       
    def __init__(self):
        # Set up an in-memory database for testing
        self.connection = sqlite3.connect(":memory:")
        self.cursor = self.connection.cursor()
        # Create the table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS BOATS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                model TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS CONFIG (
                id INTEGER,
                boatName TEXT NOT NULL,
                boatModel TEXT NOT NULL
            )
        ''')


    def setConfig(self, name: str, model: str):
         self.cursor.execute(f"REPLACE INTO CONFIG(id, name, model) VALUES(0,'{name}', '{model}')")

    def getConfig(self):
        self.cursor.execute(f"SELECT * FROM CONFIG")
        row = self.cursor.fetchone()
        return row
    def addBoat(self, boat: Boat):  
        self.cursor.execute(f"INSERT INTO BOATS (name, model) VALUES ('{boat.name}','{boat.model}')")
        self.connection.commit()


    def getBoat(self,name: str):
            self.cursor.execute(f"SELECT * FROM BOATS WHERE name == '{name}'")
            row = self.cursor.fetchone()
            return row

