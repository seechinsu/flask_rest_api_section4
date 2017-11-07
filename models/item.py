import sqlite3

db_home = 'C:\\Users\\seech\\PycharmProjects\\flask_api_section4\\data.db'


class ItemModel:

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {"name": self.name, "price": self.price}

    @classmethod
    def find_by_name(cls, name):
        global db_home
        connection = sqlite3.connect(db_home)
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return cls(*row)

    def insert(self):
        global db_home
        connection = sqlite3.connect(db_home)
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (self.name, self.price))

        connection.commit()
        connection.close()

    def update(self):
        global db_home
        connection = sqlite3.connect(db_home)
        cursor = connection.cursor()

        query = "UPDATE items SET price = ? WHERE name = ?"
        cursor.execute(query, (self.name, self.price))

        connection.commit()
        connection.close()