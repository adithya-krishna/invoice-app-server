from flask import g
import sqlite3
from sqlite3 import Error

DB_NAME = 'invoices.db';

def db_select(query):
	db_connection = sqlite3.connect(DB_NAME)
	cursor = db_connection.cursor()
	result = cursor.execute(query)
	return result

def db_execute(query, data):
	db_connection = sqlite3.connect(DB_NAME)
	cursor = db_connection.cursor()
	cursor.execute(query, data);
	db_connection.commit();
	return "success";

def get_db_connection():
	db_connection = sqlite3.connect(DB_NAME)
	return db_connection;

def init_db(app):
	with app.app_context():
		with app.open_resource('schema.sql') as f:
			try:
				db_connection = sqlite3.connect(DB_NAME)
				cursor = db_connection.cursor()
				cursor.executescript(f.read().decode('utf8'))
			except Error as e:
				print(e)
			finally:
				cursor.close()
				db_connection.close()
