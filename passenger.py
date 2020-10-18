from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/passenger'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Passenger(db.Model):
    __tablename__ = 'passenger'

    pid = db.Column(db.INTEGER, primary_key=True)
    pnr = db.Column(db.INTEGER, nullable=False)
    passport_number = db.Column(db.VARCHAR(100), nullable=False)
    family_name = db.Column(db.VARCHAR(100), nullable=False)
    given_name = db.Column(db.VARCHAR(100), nullable=False)
    title = db.Column(db.VARCHAR(20), nullable=False)
    contact_number = db.Column(db.VARCHAR(50), nullable=False)
    eticket_number = db.Column(db.VARCHAR(100), nullable=False)
    email = db.Column(db.VARCHAR(200), nullable=False)
    seat_number = db.Column(db.VARCHAR(10), nullable=False)
    fare_class = db.Column(db.VARCHAR(30), nullable=False)
    remarks = db.Column(db.VARCHAR(1000), nullable=False)

    def __init__(self, pid, pnr, passport_number, family_name, given_name, title, contact_number, eticket_number, email, seat_number, fare_class, remarks):
        self.pid = pid
        self.pnr = pnr
        self.passport_number = passport_number
        self.family_name = family_name
        self.given_name = given_name
        self.title = title
        self.contact_number = contact_number
        self.eticket_number = eticket_number
        self.email = email
        self.seat_number = seat_number
        self.fare_class = fare_class
        self.remarks = remarks

    def json(self):
        return {"pid": self.pid, "pnr": self.pnr, "passport_number": self.passport_number, "family_name": self.family_name,
        "given_name": self.given_name, "title": self.title, "contact_number": self.contact_number,
        "eticket_number": self.eticket_number, "email": self.email, "seat_number": self.seat_number,
        "fare_class": self.fare_class, "remarks": self.remarks}


@app.route("/passenger-all")
def get_all():
    return jsonify({"Passengers": [passenger.json() for passenger in Passenger.query.all()]})

@app.route("/passenger-search/<int:pid>")
def find_by_pid(pid):
        passenger = Passenger.query.filter_by(pid=pid).first()
        # print(passenger.json())
        if passenger:
            return jsonify(passenger.json())
        return jsonify({"message": "Passenger not found."}), 404

    # if session.query(exists().where(Passenger.pid == pid)).scalar():
	# 	passenger = Passenger.query.filter_by(pid=pid).first()
	# 	return jsonify(passenger.json())
	# else:
	# 	print("PID not valid")
	# 	return jsonify({"message": "Passenger not found."}), 400

@app.route("/passenger/<int:pid>", methods=['POST'])
def create_pid(pid):
    if (Passenger.query.filter_by(pid=pid).first()):
        return jsonify({"message": "A passenger with pid '{}' already exists.".format(pid)}), 400

    data = request.get_json()
    passenger = Passenger(pid, **data)

    try:
        db.session.add(passenger)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the passenger."}), 500
    return jsonify(passenger.json()), 201

@app.route("/passenger-update/<string:pid>", methods=['POST'])
def update_pax(pid):
    passenger = Passenger.query.filter_by(pid=pid).first()
    if (not passenger):
        return jsonify({"message": "A passenger with pid '{}' does not exist".format(pid)}), 400

    data = request.get_json()
    for key, value in data.items():
        setattr(passenger, key, value)

    try:
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred updating the passenger."}), 500

    return jsonify(passenger.json()), 201

if __name__ == '__main__':
    app.run(port = 5003, debug = True)
