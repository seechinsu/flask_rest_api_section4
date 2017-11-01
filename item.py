import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

db_home = 'C:\\Users\\seech\\PycharmProjects\\flask_api_section4\\data.db'


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!")

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
            return {"item": {"name": row[0], "price": row[1]}}

    @jwt_required()
    def get(self, name):
        item = Item.find_by_name(name)
        if item:
            return item
        return {"message": "Item not found."}, 404

    def post(self, name):
        if Item.find_by_name(name):
            return {"message": "This item already exists"}, 400

        data = Item.parser.parse_args()

        item = {"name": name, "price": data['price']}

        global db_home
        connection = sqlite3.connect(db_home)
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
            return {'message': 'item has been added'}
        else:
            item.update(data)
            return {'message': 'item has been updated'}


class ItemList(Resource):
    def get(self):
        return {'items': items}