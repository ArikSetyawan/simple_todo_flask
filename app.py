from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from peewee import *

db = "Todos.db"
database = SqliteDatabase(db)

class BaseModel(Model):
	class Meta:
		database=database

class Todo(BaseModel):
	id = AutoField(primary_key=True)
	todo = TextField()
	description = TextField()

class create_tables():
	with database:
		database.create_tables([Todo])

app = Flask(__name__)
api = Api(app)

class Resource_Todo(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('todo_id', location="args", type=int)
		args = parser.parse_args()
		if args['todo_id']:
			get_todo = Todo.select().where(Todo.id == args['todo_id'])
			if get_todo.exists():
				get_todo = get_todo.dicts().get()
				data_return = {
	                "data":get_todo,
	                "message":"Get todo by id success",
	                "code":"200",
	                "error":None
	            }
				return jsonify(data_return)
			else:
				data_return = {
	                "data":None,
	                "message":"Get todo by id Failed. Todo Not Found",
	                "code":"404",
	                "error":None
	            }
				return jsonify(data_return)
		else:
			get_todo = list(Todo.select().dicts())
			data_return = {
                "data":get_todo,
                "message":"Get todo success",
                "code":"200",
                "error":None
            }
			return jsonify(data_return)


	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('todo', location='json', type=str, required=True)
		parser.add_argument('description', location='json', type=str, required=True)
		args = parser.parse_args()

		Todo.create(todo=args['todo'],description=args['description'])

		data_return = {
            "data":None,
            "message":"create todo success",
            "code":"200",
            "error":None
        }
		return jsonify(data_return)

	def put(self):
		parser = reqparse.RequestParser()
		parser.add_argument('todo_id', location='json', type=int, required=True)
		parser.add_argument('todo', location='json', type=str, required=True)
		parser.add_argument('description', location='json', type=str, required=True)
		args = parser.parse_args()

		update_todo = Todo.update(todo=args['todo'], description=args['description']).where(Todo.id == args['todo_id'])
		update_todo.execute()

		data_return = {
            "data":None,
            "message":"update todo success",
            "code":"200",
            "error":None
        }
		return jsonify(data_return)

	def delete(self):
		parser = reqparse.RequestParser()
		parser.add_argument('todo_id', location="args", type=int, required=True)
		args=parser.parse_args()

		delete_todo = Todo.delete().where(Todo.id == args['todo_id'])
		delete_todo.execute()

		data_return = {
            "data":None,
            "message":"delete todo success",
            "code":"200",
            "error":None
        }
		return jsonify(data_return)


api.add_resource(Resource_Todo, '/api/todo')

if __name__ == "__main__":
	create_tables()
	app.run(debug=True, port=5012)