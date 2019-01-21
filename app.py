# -*- coding: utf-8 -*-
# @Time    : 2018-12-09 14:47
# @Author  : Yihao Wang
# @Site    :
# @File    : app.py
# @Software: PyCharm

from flask import Flask
from flask_restful import Api
from Resources.availability import Availability, AvailabilityList
from Resources.rate import Rate, RateList
from Resources.inventory import Inventory, InventoryList
import db
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)


api.add_resource(Availability, '/avail/<string:hotel_code>')
api.add_resource(AvailabilityList, '/avails')
api.add_resource(Rate, '/rate/<string:hotel_code>')
api.add_resource(RateList, '/rates')
api.add_resource(Inventory, '/inv/<string:hotel_code>')
api.add_resource(InventoryList, '/invs')


if __name__ == '__main__':
	from db import db

	db.init_app(app)

	if app.config['DEBUG']:
		@app.before_first_request
		def create_tables():
			db.create_all()

	app.run(port=5000, debug=True)
