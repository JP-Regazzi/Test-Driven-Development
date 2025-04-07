import connexion
import six

from swagger_server import util


def flights_flight_number_delete(flight_number):  # noqa: E501
    """DeleteFlight

     # noqa: E501

    :param flight_number: 
    :type flight_number: str

    :rtype: object
    """
    return 'do some magic!'


def flights_flight_number_get(flight_number):  # noqa: E501
    """GetFlight

     # noqa: E501

    :param flight_number: 
    :type flight_number: str

    :rtype: object
    """
    return 'do some magic!'


def flights_get(departure_city=None, arrival_city=None, _date=None):  # noqa: E501
    """SearchFlights

     # noqa: E501

    :param departure_city: 
    :type departure_city: str
    :param arrival_city: 
    :type arrival_city: str
    :param _date: 
    :type _date: str

    :rtype: None
    """
    return 'do some magic!'


def flights_post(body=None):  # noqa: E501
    """AddFlight

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: object
    """
    if connexion.request.is_json:
        body = str.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def random_flights_get(count=None):  # noqa: E501
    """RandomFlights

     # noqa: E501

    :param count: 
    :type count: int

    :rtype: object
    """
    return 'do some magic!'
