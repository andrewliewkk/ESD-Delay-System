import time
import json
import sys
import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests
from threading import Thread

# Communication patterns:
# Use a message-broker with 'direct' exchange to enable interaction
import pika

app = Flask(__name__)
CORS(app)

class PaymentItem:
    hotel_payment = {}

    def __init__(self):
        self.hotel_payment = {}

    def clear_payments(self):
        self.hotel_payment = {}

payment_dict = PaymentItem()

# @app.route("/payment", methods=['POST'])
def get_payment(data):
    hotelID = data["hotelID"]
    voucherID = data["voucherID"]
    amount = data["amount"]
    print(data)
    if hotelID in payment_dict.hotel_payment:
        payment_dict.hotel_payment[hotelID] = amount + payment_dict.hotel_payment[hotelID]
    else:
        payment_dict.hotel_payment[hotelID] = amount

    # print(payment_dict.hotel_payment)
    return payment_dict.hotel_payment

@app.route("/display-payment")
def stripe_payment():
    # print(payment_dict.hotel_payment)
    # payment_dict.clear_payments()
    # print(payment_dict.hotel_payment)
    payment()
    # print(payment_dict.hotel_payment)
    return payment_dict.hotel_payment

@app.route("/get-payments")
def payment():
    toReturn = []
    hostname = "project_rabbit" # default broker hostname
    port = 5672 # default port
    # connect to the broker and set up a communication channel in the connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    channel = connection.channel()

    # set up the exchange if the exchange doesn't exist
    exchangename="payment_direct"
    channel.exchange_declare(exchange=exchangename, exchange_type='direct')

    # prepare a queue for receiving messages
    channelqueue = channel.queue_declare(queue="paymenthandler", durable=True) # 'durable' makes the queue survive broker restarts
    queue_name = channelqueue.method.queue
    channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='payment.process') # bind the queue to the exchange via the key

    method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=True)
    while body != None:
        processingHotelpayment(json.loads(body))
        toReturn.append(json.loads(body))
        method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=True)

    print(toReturn)
    return jsonify({"vouchers": toReturn})

def processingHotelpayment(payment):
    print("Processing a hotel payment:")
    # url = "http://127.0.0.1:5005/payment"
    print(payment)
    hotelID = payment[0]
    voucherID = payment[1]
    amount = payment[2]
    data = {"hotelID": hotelID, "voucherID": voucherID, "amount": amount}
    get_payment(data)

@app.route('/charge', methods=['POST'])
def charge():
    api_key = 'sk_test_UW031AKQAKbNym0mu9SITQAx00Ai4PhNOm'
    # data = request.get_json()

    try:
        token = request.form.get('stripeToken')

        amount = float(request.form.get('total_amount')) * 100

        amount = int(amount)

        # todo: stripe stuff
        headers = {'Authorization' : f'Bearer {api_key}'}
        data = {
                'amount' : str(amount),
                'currency' : 'sgd',
                'description' : 'Another Charge',
                'source' : token
            }

        r = requests.post('https://api.stripe.com/v1/charges', headers=headers, data=data)

        print(r.text)
        print('its ok')
        print(amount)
        # return redirect('manager.html', code,302)
        return jsonify({"message": "payment successful"}),200
    except:
        print("Error processing payment")
        return jsonify({"message": "An error occurred when processing the payment."}), 500


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("This is " + os.path.basename(__file__) + ": processing payment request...")
    app.run(host='0.0.0.0',port = 5005, debug = True)
