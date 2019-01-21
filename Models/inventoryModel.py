# -*- coding: utf-8 -*-
# @Time    : 2019-01-17 18:08
# @Author  : Yihao Wang
# @Site    : 
# @File    : inventoryModel.py
# @Software: PyCharm

from db import db


class InventoryModel(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    hotel_code = db.Column(db.String(40))
    room_type = db.Column(db.String(20))
    count = db.Column(db.Integer)
    inv_date = db.Column(db.String(20))

    def __init__(self, hotel_code, room_type, count, inv_date):
        self.inv_date = inv_date
        self.hotel_code = hotel_code
        self.count = count
        self.room_type = room_type

    def json(self):
        return {
				'hotel_code': self.hotel_code,
				'room_type': self.room_type,
                'count': self.count,
				'inv_date': self.inv_date
	    }

    @classmethod
    def find_by_hotel_code(cls, hotel_code):
        return cls.query.filter_by(hotel_code=hotel_code).all()

    @classmethod
    def find_by_conditions(cls, hotel_code, room_type, count, inv_date):
        return cls.query.filter_by(hotel_code=hotel_code,
	                           room_type=room_type,
	                           count=count,
	                           inv_date=inv_date).first()

    @classmethod
    def find_for_put(cls, hotel_code, room_type, inv_date):
        return cls.query.filter_by(hotel_code=hotel_code,
	                            room_type=room_type,
	                            inv_date=inv_date).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
