# -*- coding: utf-8 -*-
# @Time    : 2018-12-03 10:44
# @Author  : Yihao Wang
# @Site    : 
# @File    : appRate.py
# @Software: PyCharm

from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
rates = [

	]   # A list of rates


@app.route('/')
def home():
	return render_template('index.html')


# POST /rate - data: {rate_plan_code: }
@app.route('/rate', methods=['POST'])
def create_rate():
	request_data = request.get_json()
	new_rate = {
		'rate_plan_code': request_data['rate_plan_code'],
		'amount': ''
	}
	rates.append(new_rate)
	return jsonify(new_rate)


# Get  /rate/<string:rate_plan_code>
@app.route('/rate/<string:rate_plan_code>', methods=['GET'])
def retrieve_rate(rate_plan_code):
	'''
	Iterate rates, and try to find the right one;
	It none matches, return error messages.
	:param rate_plan_code:
	:return:
	'''
	for rate in rates:
		if rate['rate_plan_code'] == rate_plan_code:
			return jsonify(rate)
	return jsonify({'message': 'Rate Plan Not Found'})


# Get  /rates
@app.route('/rates', methods=['GET'])
def retrieve_rates():
	return jsonify(rates)


# Post /rate/<string:rate_plan_code>/amount - data: {rate_plan_code:, amount:}
@app.route('/rate/<string:rate_plan_code>/amount', methods=['POST'])
def create_rate_with_amount(rate_plan_code):
	request_data = request.get_json()
	for rate in rates:
		if rate['rate_plan_code'] == rate_plan_code:
			new_amount = {
				'rate_plan_code': request_data['rate_plan_code'],
				'amount': request_data['amount']
			}
			rate = new_amount
			return jsonify(rate)
	return jsonify({'message': 'Rate Plan Not Found'})


# Get  /rate/<String:ratePlanCode>/amount
@app.route('/rate/<string:rate_plan_code>/amount', methods=['GET'])
def retrieve_rate_with_amount(rate_plan_code):
	for rate in rates:
		if rate['rate_plan_code'] == rate_plan_code:
			return jsonify(rate['amount'])
	return jsonify({'message': 'Rate Plan Not Found'})


app.run(port=5000)
