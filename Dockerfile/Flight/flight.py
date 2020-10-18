import json
import sys
import os
import requests
from flask import Flask, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

from os import environ
#from amadeus import Client, ResponseError

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



amadeus_flight_url = "https://test.api.amadeus.com/v2/shopping/flight-offers?"
amadeus_auth_url = "https://test.api.amadeus.com/v1/security/oauth2/token"

grant_type = "client_credentials"

class Airport(db.Model):
	__tablename__ = 'airports'

	airport_code = db.Column(db.String(3), primary_key=True)
	airport_type = db.Column(db.String(14))
	airport_name = db.Column(db.String(100))
	country = db.Column(db.String(2))

	def json(self):
		return {'airport_code':self.airport_code, 'airport_type':self.airport_type, 'airport_name':self.airport_name, 'country':self.country}

class FlightList(db.Model):
	__tablename__ = 'flight_list'

	fid = db.Column(db.String(8), primary_key=True)
	departure_date = db.Column(db.DATE, primary_key=True)
	departure_airport = db.Column(db.String(200), nullable=False)
	departure_time = db.Column(db.String(50), nullable=False)
	arrival_airport = db.Column(db.String(200), nullable=False)
	arrival_date = db.Column(db.DATE, nullable=False)
	arrival_time = db.Column(db.String(50), nullable=False)
	airline = db.Column(db.String(200), nullable=False)
	travel_time = db.Column(db.String(200), nullable=False)

	def __init__(self, fid,departure_airport,departure_date,departure_time,arrival_airport,arrival_date,arrival_time,airline,travel_time):
		self.fid = fid
		self.departure_airport = departure_airport
		self.departure_date = departure_date
		self.departure_time = departure_time
		self.arrival_airport = arrival_airport
		self.arrival_date = arrival_date
		self.arrival_time = arrival_time
		self.airline = airline
		self.travel_time = travel_time

	def json(self):
		return {'fid':self.fid, 'departure_airport':self.departure_airport, 'departure_date':self.departure_date, 'departure_time': self.departure_time, 'arrival_airport':self.arrival_airport, 'arrival_date':self.arrival_date, 'arrival_time':self.arrival_time, 'airline':self.airline, 'travel_time': self.travel_time}

class BookedFlight(db.Model):
	__tablename__ = 'booked_flight'

	pid = db.Column(db.String(8), primary_key=True)
	fid = db.Column(db.String(8), primary_key=True)
	departure_date = db.Column(db.DATE, primary_key=True)
	departure_airport = db.Column(db.String(200), nullable=False)
	departure_time = db.Column(db.String(50), primary_key=True)
	arrival_airport = db.Column(db.String(200), nullable=False)
	arrival_date = db.Column(db.DATE, nullable=False)
	arrival_time = db.Column(db.String(50), nullable=False)
	airline = db.Column(db.String(200), nullable=False)
	travel_time = db.Column(db.String(200), nullable=False)
	fare_class = db.Column(db.String(100), nullable=False)
	ticket_status = db.Column(db.String(100), nullable=False)
	remarks = db.Column(db.String(2000), nullable=False)

	def __init__(self, pid,fid,departure_airport,departure_date,departure_time,arrival_airport,arrival_date,arrival_time,airline,travel_time,fare_class,ticket_status,remarks):
		self.pid = pid
		self.fid = fid
		self.departure_airport = departure_airport
		self.departure_date = departure_date
		self.departure_time = departure_time
		self.arrival_airport = arrival_airport
		self.arrival_date = arrival_date
		self.arrival_time = arrival_time
		self.airline = airline
		self.travel_time = travel_time
		self.fare_class = fare_class
		self.ticket_status = ticket_status
		self.remarks = remarks

	def json(self):
		return {'pid':self.pid, 'fid':self.fid, 'departure_airport':self.departure_airport, 'departure_date':self.departure_date, 'departure_time': self.departure_time, 'arrival_airport':self.arrival_airport, 'arrival_date':self.arrival_date, 'arrival_time':self.arrival_time, 'airline':self.airline, 'travel_time': self.travel_time, 'fare_class':self.fare_class, 'ticket_status':self.ticket_status, 'remarks':self.remarks}

def check_airport_code(airport_code):
	return bool(Airport.query.filter_by(airport_code=airport_code).first()),200

@app.route("/airport-info/<string:airport_code>")
def check_airport_exists(airport_code):
	if bool(Airport.query.filter_by(airport_code=airport_code).first()):
		return jsonify({'airport':Airport.query.filter_by(airport_code=airport_code).first().json()}),200
	else:
		return jsonify({'airport':'Airport IATA code provided is invalid'}),400

@app.route("/flight-records/<int:pid>")
def getflightrecords_bypid(pid):
	print("Request received for "+ str(pid))
	return jsonify({'message':[record.json() for record in BookedFlight.query.filter_by(pid=pid)]}),200

@app.route("/flight-records/search_booked_flights")
def getallbookedflights():
	return jsonify({'message':[record.json() for record in BookedFlight.query.all()]}),200

@app.route("/flight-records/searchflights_internal",methods=['POST'])
def getflights_internalsearch():
	search = request.get_json()
	print(request.get_json())
	if request.is_json:
		search = request.get_json()
		origin = search['origin_airport']
		destination = search['destination_airport']
		status =200
	else:
		return jsonify({'message':'Error in search, please try again'}),500

	return jsonify({'message':[record.json() for record in FlightList.query.filter_by(departure_airport=origin).filter_by(arrival_airport=destination)]}),200

@app.route("/flight-records/cancel-flight",methods=['POST'])
def cancelflight():
	#get all request params & validate submission
	if request.is_json:
		booking = request.get_json()
		pid = booking['pid']
		fid = booking['fid']
		departure_date = booking['departure_date']
		status =201
	else:
		return jsonify({'message':'Error in cancellation, please try again'}),500

	#begin process to cancel booking
	try:
		record = BookedFlight.query.filter_by(pid=pid).filter_by(fid=fid).filter_by(departure_date=departure_date)
		record.ticket_status = 'CANCELLED'
		db.session.commit()
	except Exception as e:
		status = 500
		return jsonify({'message' : 'Error modifying the booking status'}),500
	if status == 201:
		return jsonify({'message':'Booking status successfully changed'}),201

@app.route("/flight-records/book", methods=['POST'])
def bookflight():
	#get all request params & validate submission
	if request.is_json:
		booking = request.get_json()
	else:
		return jsonify({'message':'Error in booking process, please try again'}),500

	current_pid = booking['pid']
	print(booking)
	flights_to_book = booking['flights']
	for req in flights_to_book:
		fid = req['fid']
		departure_airport = req['departure_airport']
		departure_date = req['departure_date']
		departure_time = req['departure_time']
		arrival_airport = req['arrival_airport']
		arrival_date = req['arrival_date']
		arrival_time = req['arrival_time']
		airline = req['airline']
		travel_time = req['travel_time']
		fare_class= req['fare_class']
		remarks = req['remarks']
		ticket_status = 'CONFIRMED'

		# if (BookedFlight.query.filter_by(pid=current_pid,fid=fid,departure_date=departure_date).first()):
		# 	return jsonify({'message': 'Flight booking already exists'}),400

		new_booking = BookedFlight(current_pid,fid,departure_airport,departure_date,departure_time,arrival_airport,arrival_date,arrival_time,airline,travel_time,fare_class,ticket_status,remarks)
		# add_to_flights = FlightList(fid,departure_airport,departure_date,departure_time,arrival_airport,arrival_date,arrival_time,airline,travel_time)
		status = 201
		try:
			db.session.add(new_booking)
			db.session.commit()

			# db.session.add(add_to_flights)
			# db.session.commit()

		except Exception as e:
			status = 500
			return jsonify({'message':'Error in creating new booking, booking may already exist'}),500

	if status == 201:
		return jsonify({'message':'Booking successfully created'}),201

@app.route("/flight-records/search-external",methods=['POST'])
def search_external():
	#creating function to call the amadeus api
	def call_amadeus_api(bearer, url, **params):
		full_url = f'https://test.api.amadeus.com/v2{url}'
		response = requests.get(full_url, params=params, headers={'Authorization': f'Bearer {bearer}','Content-Type': 'application/vnd.amadeus+json'})
		return response.json()
	#possible search params
	# children(INT), infants(INT), travelClass(ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST), nonStop(boolean), max(INT)
	#get all request params & validate submission
	if request.is_json:
		booking = request.get_json()
		origin_airport = booking['origin_airport']
		destination_airport = booking['destination_airport']
		departure_date = booking['departure_date']
		travel_class = booking['travel_class']
	else:
		return jsonify({'message':'Error in flight search, please try again'}),500

	if not(check_airport_code(origin_airport)) or not(check_airport_code(destination_airport)):
		return jsonify({'message':'Invaid Airport IATA code, please check to ensure input is correct'}),500
	#authenticate with the amadeus servers
	auth_request = {"grant_type":grant_type,"client_id":client_id,"client_secret":client_secret}
	auth_confirm = requests.post(amadeus_auth_url, data = auth_request)
	status = 201
	bearer = ""
	bearer = auth_confirm.json()['access_token']
	if bearer == "":
		return jsonify({"message":"Error in Amadeus authentication"}),500
	if status == 201:
		flight_response = call_amadeus_api(bearer, '/shopping/flight-offers',originLocationCode=origin_airport,destinationLocationCode=destination_airport,nonStop='false', departureDate=departure_date,adults=1,travelClass=travel_class,max=10)
		if 'errors' in flight_response:
			return jsonify({"flights":None}),500
		if flight_response['meta']['count'] == 0:
			return jsonify({"flights":None}),201
		else:
			response_dictionary = flight_response['dictionaries']
			aircraft_list = flight_response['dictionaries']['aircraft']
			carrier_list = flight_response['dictionaries']['carriers']
			all_flights_data = flight_response['data']
			result = []
			for option in all_flights_data:
				maintemp = []
				temp_fs = []
				for segments in option['itineraries'][0]['segments']:
					fs = {}
					aircraft_code = segments['aircraft']['code']
					fs['arrival_airport'] = segments['arrival']['iataCode']
					fs['arrival_time'] = segments['arrival']['at']
					fs['departure_time'] = segments['departure']['at']
					fs['departure_airport'] = segments['departure']['iataCode']
					fs['duration'] = segments['duration']
					carriercode = segments['carrierCode']
					fs['aircraft_type'] = response_dictionary['aircraft'][aircraft_code]
					fs['airline'] = response_dictionary['carriers'][carriercode]
					fs['flight_id'] = carriercode + segments['number']
					temp_fs.append(fs)
				price = option['price']['total']
				total_time = option['itineraries'][0]['duration']
				maintemp = {'segments':temp_fs,'price':price,'total_time':total_time}
				result.append(maintemp)
			flight_list = sorted(result, key=lambda k:k['price'])

	return jsonify({'flights':flight_list}),201

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("This is flask for Flight microservice")
    app.run(host='0.0.0.0', port=5001, debug=True)
