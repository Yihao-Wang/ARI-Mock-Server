# -*- coding: utf-8 -*-
# @Time    : 2019-01-17 17:44
# @Author  : Yihao Wang
# @Site    : 
# @File    : rateModel.py
# @Software: PyCharm

from db import db


class RateModel(db.Model):
    __tablename__ = 'rate'

    id = db.Column(db.Integer, primary_key=True)
    hotel_code = db.Column(db.String(40))
    room_type = db.Column(db.String(20))
    rate_plan = db.Column(db.String(20))
    price = db.Column(db.Float(precision=2))
    rate_date = db.Column(db.String(20))

    def __init__(self, hotel_code, room_type, rate_plan, price, rate_date, detail):
        self.rate_date = rate_date
        self.hotel_code = hotel_code
        self.price = price
        self.rate_plan = rate_plan
        self.room_type = room_type
        self.detail = detail

    def json(self):
        return {
				'hotel_code': self.hotel_code,
				'detail':
					{
					'room_type': self.room_type,
					'rate_plan': self.rate_plan
					},
                'price': self.price,
				'rate_date': self.rate_date
	    }

    @classmethod
    def find_by_hotel_code(cls, hotel_code):
        return cls.query.filter_by(hotel_code=hotel_code).all()

    @classmethod
    def find_by_conditions(cls, hotel_code, room_type, rate_plan, price, rate_date):
        return cls.query.filter_by(hotel_code=hotel_code,
	                           room_type=room_type,
	                           rate_plan=rate_plan,
	                           price=price,
	                           rate_date=rate_date).first()

    @classmethod
    def find_for_put(cls, hotel_code, room_type, rate_plan, rate_date):
        return cls.query.filter_by(hotel_code=hotel_code,
	                            room_type=room_type,
	                            rate_plan=rate_plan,
	                            rate_date=rate_date).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
