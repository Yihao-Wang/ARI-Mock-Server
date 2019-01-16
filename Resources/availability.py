# -*- coding: utf-8 -*-
# @Time    : 2018-12-15 14:13
# @Author  : Yihao Wang
# @Site    : 
# @File    : availability.py
# @Software: PyCharm

from flask_restful import Resource, reqparse
from Models.availModel import AvailabilityModel

req_body_help_message = 'This field cannot be left unfilled.'


class Availability(Resource):
	root_parser = reqparse.RequestParser()
	root_parser.add_argument('hotel_code', type=str, required=True, help=req_body_help_message)
	root_parser.add_argument('detail', type=dict, required=True, help=req_body_help_message)
	root_parser.add_argument('los', type=int, required=True, help=req_body_help_message)
	root_parser.add_argument('date', type=str, required=True, help=req_body_help_message)

	def get(self, hotel_code):
		'''

		:param hotel_code:
		:return:
		'''
		'''
		### In-Memory Setup ###
		avail = next(filter(lambda x: x['hotel_code'] == hotel_code, avails), None)
		'''
		avail = AvailabilityModel.find_by_hotel_code(hotel_code)
		if avail:
			return {'avails': list(map(lambda x: x.json(), avail))}
		return {'message': 'Availability Not Found'}, 404

	def post(self, hotel_code):
		'''

		:param hotel_code:
		:return:
		'''

		'''
		### In-Memory Setup ###
		avail = {
				'hotel_code': hotel_code,
				'detail':
					{
						'room_type': avail_data['detail']['room_type'],
						'rate_plan': avail_data['detail']['rate_plan']
					},
				'los': avail_data['los'],
				'date': avail_data['date']
				}
		
		if next(filter(lambda x: x['hotel_code'] == hotel_code
		                and x['detail']['room_type'] == avail_data['detail']['room_type']
		                and x['detail']['rate_plan'] == avail_data['detail']['rate_plan']
						and x['los'] == avail_data['los']
		                and x['date'] == avail_data['date'], avails), None)
		 '''
		avail_data = Availability.root_parser.parse_args()
		if AvailabilityModel.find_by_conditions(hotel_code,
			                                    avail_data['detail']['room_type'],
			                                    avail_data['detail']['rate_plan'],
			                                    avail_data['los'],
			                                    avail_data['date']):
			return {'message': 'The Same Availability Is Already Exist.'}, 400
		avail = AvailabilityModel(**avail_data, **avail_data.detail)
		try:
			avail.save_to_db()
		except:
			return {'message': 'An Error Occurred During Data Insertion.'}, 500
		return avail.json(), 201

	def delete(self, hotel_code):
		'''

		:param hotel_code:
		:return:
		'''
		'''
		### In-Memory Setup ###
		global avails
		delete_avail_data = Availability.root_parser.parse_args()
		if next(filter(lambda x: x['hotel_code'] == hotel_code
		                and x['detail']['room_type'] == delete_avail_data['detail']['room_type']
		                and x['detail']['rate_plan'] == delete_avail_data['detail']['rate_plan']
		                and x['los'] == delete_avail_data['los']
		                and x['date'] == delete_avail_data['date'], avails), None) is None:
			return {'message': 'The availability does not exist.'}, 400
		else:
			avails = list(filter(lambda x: x['hotel_code'] != hotel_code
			              or x['detail']['room_type'] != delete_avail_data['detail']['room_type']
			              or x['detail']['rate_plan'] != delete_avail_data['detail']['rate_plan']
			              or x['date'] != delete_avail_data['date'], avails))
			return {'message': 'The availability is deleted'}, 200
		'''
		delete_avail_data = Availability.root_parser.parse_args()
		avail = AvailabilityModel.find_by_conditions(hotel_code,
		                                             delete_avail_data['detail']['room_type'],
		                                             delete_avail_data['detail']['rate_plan'],
		                                             delete_avail_data['los'],
		                                             delete_avail_data['date'])
		if avail:
			try:
				avail.delete_from_db()
				return {'message': 'The Availability Is Deleted.'}, 200
			except:
				return {'message': 'An Error Occurred During Data Deletion.'}, 500
		return {'message': 'Availability Not Found.'}, 404

	def put(self, hotel_code):
		'''

		:param hotel_code:
		:return:
		'''
		'''
		### In-Memory Setup ###
		avail = {
			'hotel_code': hotel_code,
			'detail':
				{
					'room_type': avail_data['detail']['room_type'],
				    'rate_plan': avail_data['detail']['rate_plan']
				},
			'los': avail_data['los'],
			'date': avail_data['date']
		}
		existence_check = next(filter(lambda x: x['hotel_code'] == hotel_code
		                         and x['detail']['room_type'] == avail_data['detail']['room_type']
		                         and x['detail']['rate_plan'] == avail_data['detail']['rate_plan']
		                         and x['date'] == avail_data['date'], avails), None)
		if existence_check is None:
			avails.append(avail)
		else:
			avail.update(avail_data)
		return avail, 201
		'''
		avail_data = Availability.root_parser.parse_args()
		avail = AvailabilityModel.find_for_put(hotel_code,
		                                    avail_data['detail']['room_type'],
		                                    avail_data['detail']['rate_plan'],
		                                    avail_data['date'])
		if avail:
			avail.los = avail_data['los']
		else:
			avail = AvailabilityModel(**avail_data, **avail_data.detail)
		try:
			avail.save_to_db()
		except:
			return {'message': 'An Error Occurred During Data Insertion.'}, 500
		return avail.json()


class AvailabilityList(Resource):
	def get(self):
		'''

		:return:
		'''
		return {'avails': list(map(lambda x: x.json(), AvailabilityModel.query.all()))}
