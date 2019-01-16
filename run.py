# -*- coding: utf-8 -*-
# @Time    : 2018-12-16 14:19
# @Author  : Yihao Wang
# @Site    : 
# @File    : run.py
# @Software: PyCharm

from app import app
from db import db

db.init_app(app)


@app.before_first_request
def create_tables():
	db.create_all()
