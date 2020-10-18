from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# =============================================================================
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/flight_status'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


class DelayPlan(db.Model):
    __tablename__ = 'delay_plan'


    planid = db.Column(db.INTEGER, primary_key=True)
    flight_number = db.Column(db.INTEGER, nullable=False)
    delay_status = db.Column(db.VARCHAR(100), nullable=False)
    issue_datetime = db.Column(db.DATE, nullable=False)
    message = db.Column(db.VARCHAR(2000), nullable=False)
    is_active = db.Column(db.BOOLEAN, nullable=False)


    def __init__(self, planid, flight_number, delay_status, issue_datetime, message, is_active):

        self.planid = planid
        self.flight_number = flight_number
        self.delay_status = delay_status
        self.issue_datetime = issue_datetime
        self.message = message
        self.is_active = is_active

    def json(self):
            return {"planid": self.planid, "flight_number": self.flight_number, "delay_status": self.delay_status, "issue_datetime": self.issue_datetime, "message": self.message, "is_active": self.is_active}

import datetime
class Message(db.Model):
    __tablename__ = 'message'

    mid = db.Column(db.INTEGER, primary_key=True)
    message = db.Column(db.VARCHAR(2000), nullable=False)
    issue_datetime = db.Column(db.DATETIME, nullable=False)
    is_active = db.Column(db.BOOLEAN, nullable =False)

    def __init__(self, message, is_active):
        self.message = message
        self.issue_datetime = datetime.datetime.now()
        self.is_active = is_active

    def json(self):
        return {"mid":self.mid, "message":self.message, "issue_datetime":self.issue_datetime, "is_active":self.is_active}

class CurrentFlight(db.Model):

	__tablename__ = 'current_flight'

	fid = db.Column(db.VARCHAR(5), primary_key=True)
	depart = db.Column(db.VARCHAR(3), nullable=False)
	arrive = db.Column(db.VARCHAR(3), nullable=False)
	std = db.Column(db.VARCHAR(30), nullable=False)
	etd = db.Column(db.VARCHAR(30), nullable=False)
	sta = db.Column(db.VARCHAR(30), nullable=False)
	eta = db.Column(db.VARCHAR(30), nullable=False)
	status = db.Column(db.VARCHAR(100), nullable=False)

	def __init__(self, fid, depart, arrive, std, etd, sta, eta, status):

		self.fid = fid
		self.depart = depart
		self.arrive = arrive
		self.std = std
		self.etd = etd
		self.sta = sta
		self.eta = eta
		self.status = status

	def json(self):
		return {"fid":self.fid, "depart":self.depart, "arrive":self.arrive, "std":self.std, "etd":self.etd, "sta":self.sta, "eta":self.eta, "status":self.status}

@app.route("/checkflight")
def getflight():
	try:
		CurrentFlight.query.first()
	except:
		return jsonify({"message":"Error retrieving current flight"}),500

	return jsonify({"message": CurrentFlight.query.first().json()}),200


@app.route("/flight-status/message")
def get_all_messages():
    return jsonify({"message": [message.json() for message in Message.query.all()]}),200

@app.route("/flight-status/active-message")
def get_active_messages():
    return jsonify({"message": [message.json() for message in Message.query.filter_by(is_active=1)]}),200

@app.route("/flight-status/cancel_message/<int:mid>")
def cancel_message(mid):
    print(mid)
    try:
        message = Message.query.filter_by(mid=mid).first()
        print(message)
        setattr(message, "is_active", False)
        db.session.commit()
        return jsonify({"message": "200"}), 200
    except:
        return jsonify({"message": "An error occurred updating the annoucement."}), 500


@app.route("/flight-status/all-active")
def get_delay_status():
    return jsonify({"delay_status": [delay_status.json() for delay_status in DelayPlan.query.filter_by(is_active=1)]}),200

@app.route("/flight-status/delay_plan/<int:flight_number>")
def get_delay_plan(flight_number):
    return jsonify({"delay_status": [message.json() for message in DelayPlan.query.filter_by(flight_number=flight_number)]}),200

#modify


@app.route("/flight-status/modify/<int:flight_number>", methods=['POST'])
def modify_flight_status(flight_number):
    flight_status = DelayPlan.query.filter_by(flight_number=flight_number).first()
    if (not flight_status):
        return jsonify({"message": "No Flight status for flight '{}' ".format(flight_number)}), 400

    data = request.get_json()
    for key, value in data.items():
        setattr(flight_status, key, value)

    try:
        db.session.add(flight_status)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred updating the passenger."}), 500

    return jsonify(flight_status.json()), 201

#add
@app.route("/flight-status/new-message", methods=['POST'])
def add_message():
    data = request.get_json()
    message = Message(**data)

    # try:
    db.session.add(message)
    db.session.commit()
    # except:
    #     return jsonify({"message": "An error occurred creating new message."}), 500
    return jsonify(message.json()), 201

@app.route("/flight-status/delay-plan", methods=['POST'])
def add_delay_plan():
    data = request.get_json()
    planid = data['planid']
    if (DelayPlan.query.filter_by(planid=planid).first()):
        return jsonify({"message": "A Delay Plan with planid '{}' already exists.".format(planid)}), 400

    message = Message(**data)

    try:
        db.session.add(message)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating new message."}), 500
    return jsonify(message.json()), 201

@app.route("/current_status/modify/<string:fid>", methods=['POST'])
def modify_current_flight(fid):
    current_flight = CurrentFlight.query.filter_by(fid=fid).first()
    if (not current_flight):
        return jsonify({"message": "No Current Flight for fid '{}' ".format(fid)}), 400

    data = request.get_json()
    print(data)
    for key, value in data.items():
        setattr(current_flight, key, value)

    try:
        db.session.add(current_flight)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred updating the passenger."}), 500

    return jsonify(current_flight.json()), 201

if __name__ == '__main__':
    app.run(port = 5004, debug = True)
