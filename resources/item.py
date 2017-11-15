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
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

        # global db_home
        # if ItemModel.find_by_name(name):
        #     connection = sqlite3.connect(db_home)
        #     cursor = connection.cursor()
        #
        #     query = "DELETE FROM items WHERE name = ?"
        #     cursor.execute(query, (name,))
        #
        #     connection.commit()
        #     connection.close()
        #
        #     return {"message": name + " has been deleted"}
        # return {"message": name + " is not found"}

    def put(self, name):

        data = self.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}