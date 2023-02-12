from flask import Flask
from flask_restx import Api, Resource, reqparse
from werkzeug.exceptions import abort
import sqlite3


ITEMS = []
ITEM = {}


def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection


def get_items():
    global ITEMS
    ITEMS = []
    connection = get_db_connection()
    items = connection.execute('select * from items').fetchall()
    connection.close()
    for item in items:
        current_item = dict(id=item['id'],
                            title=item['title'],
                            description=item['description'],
                            priority=item['priority'])
        ITEMS.append(current_item)


def get_item(item_id):
    global ITEM
    connection = get_db_connection()
    item = connection.execute('select * from items where id = ?', (item_id,)).fetchone()
    connection.close()
    ITEM = dict(id=item['id'],
                title=item['title'],
                description=item['description'],
                priority=item['priority'])

    if ITEM is None:
        abort(404)
    return ITEM


app = Flask(__name__)
api = Api(app)


namespace = api.namespace("TodoList API", description="TodoList API")

parser = reqparse.RequestParser()
parser.add_argument("title", type=str, help="Enter item title:")
parser.add_argument("description", type=str, help="Enter item description:")
parser.add_argument("priority", type=str, help="Enter item priority:")


@namespace.route('/items/')
class TodoList(Resource):
    @staticmethod
    def get():
        get_items()
        return ITEMS

    @api.doc(parser=parser)
    def post(self):
        args = parser.parse_args()
        item_title = args['title']
        item_description = args['description']
        item_priority = args['priority']
        connection = get_db_connection()
        connection.execute('insert into items(title, description, priority) values (?, ?, ?)',
                           (item_title, item_description, item_priority))
        connection.commit()
        connection.close()
        get_items()
        return ITEMS


@namespace.route('/items/<int:id>')
class Todo(Resource):
    @staticmethod
    def get(id):
        get_item(id)
        return ITEM

    @staticmethod
    def delete(id):
        connection = get_db_connection()
        connection.execute('delete from items where id = ?', (id,))
        connection.commit()
        connection.close()
        get_items()
        return ITEMS

    @api.doc(parser=parser)
    def put(self, id):
        args = parser.parse_args()
        item_title = args['title']
        item_description = args['description']
        item_priority = args['priority']
        connection = get_db_connection()
        connection.execute('update items set title = ?, description = ?, priority = ? where id = ?',
                           (item_title, item_description, item_priority, id))
        connection.commit()
        connection.close()
        get_items()
        return ITEMS


if __name__ == '__main__':
    app.run()
