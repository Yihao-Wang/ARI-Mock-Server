# -*- coding: utf-8 -*-
# @Time    : 2019-01-17 17:58
# @Author  : Yihao Wang
# @Site    : 
# @File    : inventory.py
# @Software: PyCharm

from flask_restful import Resource, reqparse
from Models.inventoryModel import InventoryModel

req_body_help_message = 'This field cannot be left unfilled.'


class Inventory(Resource):
	root_parser = reqparse.RequestParser()
	'''
	we use RequestParser to define what data, types of data the API accept
	'''
	root_parser.add_argument('hotel_code', type=str, required=True, help=req_body_help_message)
	root_parser.add_argument('room_type', type=str, required=True, help=req_body_help_message)
	root_parser.add_argument('count', type=int, required=True, help=req_body_help_message)
	root_parser.add_argument('inv_date', type=str, required=True, help=req_body_help_message)

	def get(self, hotel_code):
		'''
		Retrieve the inventory records which belong to a single hotel. (search by hotel_code)
		:param hotel_code: the single param.
		:return: teh list of inventories.
		'''
		inv = InventoryModel.find_by_hotel_code(hotel_code)
		if inv:
			return {'inventories': list(map(lambda x: x.json(), inv))}
		return {'message': 'Inventory Not Found'}, 404

	def post(self, hotel_code):
		'''
		Create a new inventory records.
		:param hotel_code: stands for the Inventory's host.
		:return: the POST result.
		'''
		inv_data = Inventory.root_parser.parse_args()
		if InventoryModel.find_by_conditions(hotel_code,
		                                        inv_data['room_type'],
		                                        inv_data['count'],
		                                        inv_data['inv_date']):
			return {'message': 'The Same Inventory Is Already Exist.'}, 400
		inv = InventoryModel(**inv_data)
		try:
			inv.save_to_db()
		except:
			return {'message': 'An Error Occurred During Data Insertion.'}, 500
		return inv.json(), 201

	def delete(self, hotel_code):
		'''
		Remove an Inventory entry.
		:param hotel_code: The only param.
		:return: DELETE result.
		'''
		delete_inv_data = Inventory.root_parser.parse_args()
		inv = InventoryModel.find_by_conditions(hotel_code,
		                                             delete_inv_data['room_type'],
		                                             delete_inv_data['count'],
		                                             delete_inv_data['inv_date'])
		if inv:
			try:
				inv.delete_from_db()
				return {'message': 'The Inventory Is Deleted.'}, 200
			except:
				return {'message': 'An Error Occurred During Data Deletion.'}, 500
		return {'message': 'Inventory Not Found.'}, 404

	def put(self, hotel_code):
		'''
		Changing a 'count' value from an Inventory, or create a new one.
		:param hotel_code: The only Param.
		:return: the PUT result.
		'''
		inv_data = Inventory.root_parser.parse_args()
		inv = InventoryModel.find_for_put(hotel_code,
		                                       inv_data['room_type'],
		                                       inv_data['inv_date'])
		if inv:
			inv.count = inv_data['count']
		else:
			inv = InventoryModel(**inv_data)
		try:
			inv.save_to_db()
		except:
			return {'message': 'An Error Occurred During Data Insertion.'}, 500
		return inv.json()


class InventoryList(Resource):
	def get(self):
		'''
		Retrieve all teh Inventory records.
		:return: All Inventory entries.
		'''
		return {'invs': list(map(lambda x: x.json(), InventoryModel.query.all()))}
