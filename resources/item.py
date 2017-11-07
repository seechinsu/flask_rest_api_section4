import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

db_home = 'C:\\Users\\seech\\PycharmProjects\\flask_api_section4\\data.db'


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found."}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "This item already exists"}, 400

        data = self.parser.parse_args()

        item = ItemModel(name, data['price'])

        try:
            item.insert()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item, 201

    def delete(self, name):
        global db_home
        if ItemModel.find_by_name(name):
            connection = sqlite3.connect(db_home)
            cursor = connection.cursor()

            query = "DELETE FROM items WHERE name = ?"
            cursor.execute(query, (name,))

            connection.commit()
            connection.close()

            return {"message": name + " has been deleted"}
        return {"message": name + " is not found"}

    def put(self, name):
        global db_home

        data = self.parser.parse_args()

        item = ItemModel.find_by_name(name)

        updated_item = ItemModel(name, data['price'])

        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "An error occurred inserting the item."}, 500
        else:
            try:
                updated_item.update()
            except:
                return {"message": "An error occurred updating the item."}, 500
        return updated_item.json()


class ItemList(Resource):
    def get(self):
        global db_home
        connection = sqlite3.connect(db_home)
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items = []

        for row in result:
            items.append({"name": row[0], "price": row[1]})

        connection.close()

        return {'items': items}