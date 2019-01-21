# -*- coding: utf-8 -*-
# @Time    : 2019-01-17 17:27
# @Author  : Yihao Wang
# @Site    : 
# @File    : rate.py
# @Software: PyCharm

from flask_restful import Resource, reqparse
from Models.rateModel import RateModel

req_body_help_message = 'This field cannot be left unfilled.'


class Rate(Resource):
	root_parser = reqparse.RequestParser()
	'''
	we use RequestParser to define what data, types of data the API accept
	'''
	root_parser.add_argument('hotel_code', type=str, required=True, help=req_body_help_message)
	root_parser.add_argument('detail', type=dict, required=True, help=req_body_help_message)
	root_parser.add_argument('price', type=float, required=True, help=req_body_help_message)
	root_parser.add_argument('rate_date', type=str, required=True, help=req_body_help_message)

	def get(self, hotel_code):
		'''

		:param hotel_code:
		:return:
		'''
		'''
		### In-Memory Setup ###
		avail = next(filter(lambda x: x['hotel_code'] == hotel_code, avails), None)
		'''
		rate = RateModel.find_by_hotel_code(hotel_code)
		if rate:
			return {'rates': list(map(lambda x: x.json(), rate))}
		return {'message': 'Rate Not Found'}, 404

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
		rate_data = Rate.root_parser.parse_args()
		if RateModel.find_by_conditions(hotel_code,
		                                        rate_data['detail']['room_type'],
		                                        rate_data['detail']['rate_plan'],
		                                        rate_data['price'],
		                                        rate_data['rate_date']):
			return {'message': 'The Same Rate Is Already Exist.'}, 400
		rate = RateModel(**rate_data, **rate_data.detail)
		try:
			rate.save_to_db()
		except:
			return {'message': 'An Error Occurred During Data Insertion.'}, 500
		return rate.json(), 201

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
		delete_rate_data = Rate.root_parser.parse_args()
		rate = RateModel.find_by_conditions(hotel_code,
		                                             delete_rate_data['detail']['room_type'],
		                                             delete_rate_data['detail']['rate_plan'],
		                                             delete_rate_data['price'],
		                                             delete_rate_data['rate_date'])
		if rate:
			try:
				rate.delete_from_db()
				return {'message': 'The Rate Is Deleted.'}, 200
			except:
				return {'message': 'An Error Occurred During Data Deletion.'}, 500
		return {'message': 'Rate Not Found.'}, 404

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
		rate_data = Rate.root_parser.parse_args()
		rate = RateModel.find_for_put(hotel_code,
		                                       rate_data['detail']['room_type'],
		                                       rate_data['detail']['rate_plan'],
		                                       rate_data['rate_date'])
		if rate:
			rate.price = rate_data['price']
		else:
			rate = RateModel(**rate_data, **rate_data.detail)
		try:
			rate.save_to_db()
		except:
			return {'message': 'An Error Occurred During Data Insertion.'}, 500
		return rate.json()


class RateList(Resource):
	def get(self):
		'''

		:return:
		'''
		return {'rates': list(map(lambda x: x.json(), RateModel.query.all()))}
