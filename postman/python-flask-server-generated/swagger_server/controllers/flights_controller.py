import connexion
import six
from flask import jsonify, make_response

# In-memory data stores for demonstration
FLIGHTS = {
    "11120": {
        "Airline": "NW",
        "ArrivalCity": "London",
        "ArrivalTime": "05:31 PM",
        "DepartureCity": "Paris",
        "DepartureTime": "03:50 PM",
        "FlightNumber": 11120,
        "Price": 147.4,
        "PriceFirst": 176.88,
        "PriceBusiness": 191.62,
        "SeatsAvailable": 250,
        "DayOfWeek": "Friday"
    }
}

import random
import datetime


def flights_flight_number_delete(flight_number):  # noqa: E501
    """DeleteFlight"""
    if flight_number in FLIGHTS:
        del FLIGHTS[flight_number]
        return jsonify({"true": f"Flight deleted {flight_number} "})
    return make_response(jsonify({"error": "Flight not found"}), 404)


def flights_flight_number_get(flight_number):  # noqa: E501
    """GetFlight"""
    flight = FLIGHTS.get(flight_number)
    if flight:
        return jsonify(flight)
    return make_response(jsonify({"error": "Flight not found"}), 404)


def flights_get(departure_city=None, arrival_city=None, _date=None):  # noqa: E501
    """SearchFlights"""
    results = [f for f in FLIGHTS.values() if
               (not departure_city or f["DepartureCity"] == departure_city) and
               (not arrival_city or f["ArrivalCity"] == arrival_city)]

    if not results:
        return make_response("""
            <!doctype html><html lang=en><title>500 Internal Server
            Error</title><h1>Internal Server Error</h1><p>The server
            encountered an internal error and was unable to complete your
            request. Either the server is overloaded or there is an error in
            the application.</p>
        """, 500)
    return jsonify(results)


def flights_post(body=None):  # noqa: E501
    """AddFlight"""
    if connexion.request.is_json:
        data = connexion.request.get_json()
        new_flight_number = str(random.randint(10000, 99999))
        flight = {
            "Airline": data["Airline"],
            "ArrivalCity": data["ArrivalCity"],
            "ArrivalTime": data["ArrivalTime"],
            "DepartureCity": data["DepartureCity"],
            "DepartureTime": data["DepartureTime"],
            "FlightNumber": new_flight_number,
            "Price": data["Price"],
            "PriceFirst": data["PriceFirst"],
            "PriceBusiness": data["PriceBusiness"],
            "SeatsAvailable": data["SeatsAvailable"],
            "DayOfWeek": data["DayOfWeek"]
        }
        FLIGHTS[new_flight_number] = flight
        return make_response(jsonify(flight), 201)
    return make_response(jsonify({"error": "Invalid input"}), 400)


def random_flights_get(count=None):  # noqa: E501
    """RandomFlights"""
    try:
        count = int(count) if count else 1
    except ValueError:
        return make_response(jsonify({"error": "Invalid count"}), 400)

    sample_flights = list(FLIGHTS.values())[:count]
    return jsonify(sample_flights)