# -*- coding: utf-8 -*-
# @Time    : 2019-01-15 14:18
# @Author  : Yihao Wang
# @Site    : 
# @File    : availModel.py
# @Software: PyCharm

from db import db


class AvailabilityModel(db.Model):
    __tablename__ = 'availability'

    id = db.Column(db.Integer, primary_key=True)
    hotel_code = db.Column(db.String(40))
    room_type = db.Column(db.String(20))
    rate_plan = db.Column(db.String(20))
    los = db.Column(db.Integer)
    date = db.Column(db.String(20))

    def __init__(self, hotel_code, room_type, rate_plan, los, date, detail):
        self.date = date
        self.hotel_code = hotel_code
        self.los = los
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
                'los': self.los,
				'date': self.date
	    }

    @classmethod
    def find_by_hotel_code(cls, hotel_code):
        return cls.query.filter_by(hotel_code=hotel_code).all()

    @classmethod
    def find_by_conditions(cls, hotel_code, room_type, rate_plan, los, date):
        return cls.query.filter_by(hotel_code=hotel_code,
	                           room_type=room_type,
	                           rate_plan=rate_plan,
	                           los=los,
	                           date=date).first()

    @classmethod
    def find_for_put(cls, hotel_code, room_type, rate_plan, date):
	    return cls.query.filter_by(hotel_code=hotel_code,
	                            room_type=room_type,
	                            rate_plan=rate_plan,
	                            date=date).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()