ef update_pax(pid):
    passenger = Passenger.query.filter_by(pid=pid).first()
    if (not passenger):
        return jsonify({"message": "A passenger with pid '{}' does not exist".format(pid)}), 400
    
    data = request.get_json()
    for key, value in data.items():
        setattr(passenger, key, value)

    try:
        db.session.add(passenger)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred updating the passenger."}), 500
    
    return jsonify(passenger.json()), 201