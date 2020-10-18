from __future__ import print_function
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests
import json
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from PIL import Image, ImageDraw, ImageFont
from datetime import date

import qrcode
import httplib2
import os
import auth
import send_email
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import pika
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# ========================== Codes for Gmail API =============================
def get_labels():
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'
authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = authInst.get_credentials()

http = credentials.authorize(httplib2.Http())
service = discovery.build('gmail', 'v1', http=http)

# =============================================================================
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/service_recovery'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Voucher(db.Model):
    __tablename__ = 'voucher'

    vid = db.Column(db.VARCHAR(100), primary_key=True)
    pid = db.Column(db.INTEGER, nullable=False)
    voucher_type = db.Column(db.VARCHAR(500), nullable=False)
    issue_date = db.Column(db.DATE, nullable=False)
    entitlement = db.Column(db.VARCHAR(1000), nullable=False)
    remarks = db.Column(db.VARCHAR(1000), nullable=False)
    is_redeemed = db.Column(db.BOOLEAN, nullable=False)
    hid = db.Column(db.INTEGER, nullable=True)

    def __init__(self, vid, pid, voucher_type, issue_date, entitlement, remarks, hid):
        self.vid = vid
        self.pid = pid
        self.voucher_type = voucher_type
        self.issue_date = issue_date
        self.entitlement = entitlement
        self.remarks = remarks
        self.is_redeemed = False
        self.hid = hid

    def json(self):
        return {"vid": self.vid, "pid": self.pid, "voucher_type": self.voucher_type, "issue_date": self.issue_date.__str__(), "entitlement": self.entitlement,
        "remarks": self.remarks, "is_redeemed": self.is_redeemed, "hid": self.hid}

class HotelList(db.Model):
    __tablename__ = 'hotel_list'

    hid = db.Column(db.INTEGER, primary_key=True)
    hotel_name = db.Column(db.VARCHAR(500), nullable=False)
    hotel_address = db.Column(db.VARCHAR(1000), nullable=False)
    economy_room_qty = db.Column(db.INTEGER, nullable=False)
    business_room_qty = db.Column(db.INTEGER, nullable=False)
    first_room_qty = db.Column(db.INTEGER, nullable=False)
    total_economy_room = db.Column(db.INTEGER, nullable=False)
    total_business_room = db.Column(db.INTEGER, nullable=False)
    total_first_room = db.Column(db.INTEGER, nullable=False)
    remarks = db.Column(db.INTEGER, nullable=False)

    def __init__(self, hid, hotel_name, hotel_address, economy_room_qty, business_room_qty,
    first_room_qty, total_economy_room, total_business_room, total_first_room, remarks):
        self.hid = hid
        self.hotel_name = hotel_name
        self.hotel_address = hotel_address
        self.economy_room_qty = economy_room_qty
        self.business_room_qty = business_room_qty
        self.first_room_qty = first_room_qty
        self.total_economy_room = total_economy_room
        self.total_business_room = total_business_room
        self.total_first_room = total_first_room
        self.remarks = remarks

    def json(self):
        return {"hid": self.hid, "hotel_name": self.hotel_name, "hotel_address": self.hotel_address, "economy_room_qty": self.economy_room_qty, "business_room_qty": self.business_room_qty,
        "first_room_qty": self.first_room_qty, "total_economy_room": self.total_economy_room, "total_business_room": self.total_business_room, "total_first_room": self.total_first_room,
        "remarks": self.remarks}

class Eligibility(db.Model):
    __tablename__ = 'eligibility'

    fare_class = db.Column(db.VARCHAR(30), primary_key=True)
    hotel_voucher = db.Column(db.BOOLEAN, nullable=False)
    meal_voucher = db.Column(db.INTEGER, nullable=False)
    lounge_voucher = db.Column(db.BOOLEAN, nullable=False)
    transport_voucher = db.Column(db.BOOLEAN, nullable=False)
    update_datetime = db.Column(db.DATETIME, nullable=False)

    def __init__(self, fare_class, hotel_voucher, meal_voucher, lounge_voucher, transport_voucher):
        self.fare_class = fare_class
        self.hotel_voucher = hotel_voucher
        self.meal_voucher = meal_voucher
        self.lounge_voucher = lounge_voucher
        self.transport_voucher = transport_voucher
        # self.update_datetime = update_datetime

    def json(self):
        return {"fare_class": self.fare_class, "hotel_voucher": self.hotel_voucher, "meal_voucher": self.meal_voucher,
        "lounge_voucher": self.lounge_voucher, "transport_voucher": self.transport_voucher, "update_datetime": self.update_datetime}

# ========== Vouchers ==========
@app.route("/service-vouchers")
def get_all_vouchers():
    return jsonify({"vouchers": [voucher.json() for voucher in Voucher.query.all()]})

@app.route("/pax-vouchers/<string:pid>")
def get_pax_vouchers(pid):
    return jsonify({"vouchers": [voucher.json() for voucher in Voucher.query.filter_by(pid=pid)]})

@app.route("/get-vouchers/<string:vid>")
def get_voucher(vid):
    voucher = Voucher.query.filter_by(vid=vid).first()
    if voucher:
        return jsonify(voucher.json())
    return jsonify({"message": "Voucher not found."}), 404

@app.route("/get-vouchers/<string:vid>")
def get_voucher_type(vid):
    get_voucher_type = Voucher.query.filter_by(vid=vid).first()
    if get_voucher_type:
        get_voucher_type.voucher_type

        return jsonify(get_voucher_type.json())
    return jsonify({"message": "Voucher Type not found."}), 404

# updates
@app.route("/service-vouchers/modify/<string:vid>", methods=['POST'])
def update_voucher(vid):
    voucher = Voucher.query.filter_by(vid=vid).first()
    if (not voucher):
        return jsonify({"message": "Voucher with vid '{}' does not exist".format(vid)}), 400

    data = request.get_json()
    for key, value in data.items():
        setattr(voucher, key, value)

    db.session.add(voucher)
    db.session.commit()

    if voucher.voucher_type  == "Hotel":

        hostname = "project_rabbit" #might not work with docker
        port = 5672
        price = [voucher.hid, voucher.vid, 100] # this should be the price of the hotel
        price  = json.dumps(price, default=str) # convert a JSON object to a string

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
        channel = connection.channel()
        exchangename="payment_direct"
        channel.exchange_declare(exchange=exchangename, exchange_type='direct')
        channel.queue_declare(queue='paymenthandler', durable=True) # make sure the queue used by the error handler exist and durable
        channel.queue_bind(exchange=exchangename, queue='paymenthandler', routing_key='payment.process') # make sure the queue is bound to the exchange

        channel.basic_publish(exchange=exchangename, routing_key="payment.process", body=price,
        properties=pika.BasicProperties(delivery_mode = 2) # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange)
        )
        connection.close()

    # except:
    #     return jsonify({"message": "An error occurred updating the voucher."}), 500

    return jsonify(voucher.json()), 201

@app.route("/service-vouchers/redeem/<string:vid>")
def redeem_voucher(vid):
    voucher = Voucher.query.filter_by(vid=vid).first()
    if (not voucher):
        return jsonify({"message": "Voucher with vid '{}' does not exist".format(vid)}), 400

    if(voucher.is_redeemed):
        return jsonify({"message": "Voucher with vid '{}' has already been redeemed".format(vid)}), 400

    setattr(voucher, "is_redeemed",True) # set to redeemed back after test

    voucher_type = voucher.voucher_type

    try:
        db.session.commit()

    except:
        return jsonify({"message": "An error occurred updating the voucher."}), 500

    return "Voucher " + vid + " has been successfully redeemed! This voucher is entitled to " + voucher.entitlement

@app.route("/service-vouchers/issue", methods=['POST'])
def issue_voucher():
    data = request.get_json()
    vid = data['vid']
    if (Voucher.query.filter_by(vid=vid).first()):
        return jsonify({"message": "A voucher with vid '{}' already exists.".format(vid)}), 400

    voucher = Voucher(**data)

    try:
        db.session.add(voucher)
        db.session.commit()

        # qr image creation
        voucher_accept_url = "http://127.0.0.1:5002/service-vouchers/redeem/" + vid # URL TO BE CHANGED
        qr = qrcode.make(voucher_accept_url)


        #voucher image creation
        voucher_type = data['voucher_type']
        #background = Image.open('vouchers/images/' + voucher_type + '.jpg')
        background = Image.open('vouchers/images/background.jpg')
        background.paste(qr, (300, 500))
        draw = ImageDraw.Draw(background)


        #pull passenger details from passenger db
        passengerid = str(data['pid'])
        retrieve_pax_url = "http://127.0.0.1:5003/passenger-search/" + passengerid
        pax_info = requests.get(retrieve_pax_url)
        pax_info = json.loads(pax_info.text)
        name = pax_info['title'] + " " + pax_info['given_name'] + " " + pax_info['family_name']
        date = data['issue_date']

        pax_email = pax_info['email']
        #draw voucher details
        font = ImageFont.truetype('vouchers/font/Helvetica 400.ttf', 25)
        title = vid
        w,h = font.getsize(title)
        draw.text((172,185), title ,(255,255,255),font=font)

        #draw user details
        font = ImageFont.truetype('vouchers/font/Helvetica 400.ttf', 25)
        title = name
        w,h = font.getsize(title)
        draw.text((51,240), title ,(255,255,255),font=font)

        #draw issue date
        font = ImageFont.truetype('vouchers/font/Helvetica 400.ttf', 18)
        title = date
        w,h = font.getsize(title)
        draw.text((160,293), title ,(255,255,255),font=font)

        #Draw title
        font = ImageFont.truetype('vouchers/font/Helvetica 400.ttf', 60)
        if voucher_type == 'Meal':
            title = "Meal Voucher"
            w,h = font.getsize(title)
            draw.text(((1000-w)/2, 943), title ,(255,255,255),font=font)

        elif voucher_type == 'Hotel':
            title = "Hotel Voucher"
            hid = data["hid"]
            hotel_url = "http://127.0.0.1:5002/service-hotels/" + str(hid)
            hotel_details_json = requests.get(hotel_url)
            hotel_details = json.loads(hotel_details_json.text)
            w,h = font.getsize(title)
            draw.text(((1000-w)/2, 943), title ,(255,255,255),font=font)
            font = ImageFont.truetype('vouchers/font/Helvetica 400.ttf', 18)
            hotel_name = hotel_details['hotel_name']
            hotel_address = hotel_details['hotel_address']
            title = "Hotel:                   " + hotel_name
            draw.text((500, 373), title ,(255,255,255),font=font)
            title = "Hotel Address:   " + hotel_address
            draw.text((500, 410), title ,(255,255,255),font=font)

        elif voucher_type == 'Lounge':
            title = "Lounge Voucher"
            w,h = font.getsize(title)
            draw.text(((1000-w)/2, 943), title ,(255,255,255),font=font)

        elif voucher_type == 'Transport':
            title = "Transport Voucher"
            w,h = font.getsize(title)
            draw.text(((1000-w)/2, 943), title ,(255,255,255),font=font)

        #draw title
        font = ImageFont.truetype('vouchers/font/Helvetica 400.ttf', 18)
        title = data['voucher_type']
        w,h = font.getsize(title)
        draw.text((150,373), title ,(255,255,255),font=font)


        #draw content
        font = ImageFont.truetype('vouchers/font/Helvetica 400.ttf', 18)
        title = data['entitlement']
        w,h = font.getsize(title)
        draw.text((150,410), title ,(255,255,255),font=font)


        background.save('vouchers/vouchers/' + vid + '.jpg')
        sendInst = send_email.send_email(service)
        #sender, receiver, Title, message, attachment
        message = sendInst.create_message_with_attachment('esd.singaporeairline@gmail.com', pax_email,
        'Here is your '+ data['voucher_type'] + ' voucher!', data['entitlement'], "vouchers/vouchers/" + vid + '.jpg' )
        sendInst.send_message('me', message)

    except:
        return jsonify({"message": "An error occurred creating the voucher."}), 500
    return jsonify(voucher.json()), 201

# ========== Hotel ==========
@app.route("/service-hotels")
def get_all_hotels():
    return jsonify({"hotels": [hotel.json() for hotel in HotelList.query.all()]}), 200

@app.route("/service-hotels/<int:hid>")
def get_hotel_details(hid):
    hotel = HotelList.query.filter_by(hid=hid).first()
    if hotel:
        return jsonify(hotel.json()), 200
    return jsonify({"message": "Hotel not found."}), 404

@app.route("/service-hotels/add", methods=['POST'])
def add_hotel():
    data = request.get_json()
    hid = data['hid']
    if (HotelList.query.filter_by(hid=hid).first()):
        return jsonify({"message": "A hotel with hid '{}' already exists.".format(hid)}), 400

    hotel = HotelList(**data)

    try:
        db.session.add(hotel)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the hotel."}), 500
    return jsonify(hotel.json()), 201

@app.route("/service-hotels/modify/<int:hid>", methods=['POST'])
def modify_hotel(hid):
    hotel = HotelList.query.filter_by(hid=hid).first()
    if (not hotel):
        return jsonify({"message": "A passenger with hid '{}' does not exist".format(hid)}), 400

    data = request.get_json()
    for key, value in data.items():
        setattr(hotel, key, value)

    try:
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred updating the passenger."}), 500

    return jsonify(hotel.json()), 201

# ========== Eligibility ==========

@app.route("/eligibility")
def get_current_eligibility():
    return jsonify({"Eligibility": [eligibility.json() for eligibility in Eligibility.query.all()]}), 200

# passenger_url = "http://passenger:5003/passenger-search"
passenger_url = "http://127.0.0.1:5003/passenger-search"

@app.route("/eligibility/<int:pid>")
def get_passenger_eligibility(pid):
    retrieve_pax_url = passenger_url + "/" + str(pid)
    pax_info = requests.get(retrieve_pax_url)
    print(pax_info)
    result = json.loads(pax_info.text)
    if "message" in result:
        return jsonify({"message": "Passenger not found."}), 404
    fare_class = result["fare_class"]
    eligibility = Eligibility.query.filter_by(fare_class=fare_class).first()

    return jsonify(eligibility.json()), 200

@app.route("/eligibility/edit/<string:fare_class>", methods=["POST"])
def modify_eligibility(fare_class):
    data = request.get_json()
    eligibility = Eligibility.query.filter_by(fare_class=fare_class).first()

    for key, value in data.items():
        setattr(eligibility, key, value)

    try:
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred updating the passenger."}), 500

    return jsonify(eligibility.json()), 201



if __name__ == '__main__':
    app.run(port = 5002, debug = True)
