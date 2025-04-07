import connexion
import six

from swagger_server import util


def cities_city_code_delete(city_code):  # noqa: E501
    """DeleteCity

     # noqa: E501

    :param city_code: 
    :type city_code: str

    :rtype: object
    """
    return 'do some magic!'


def cities_city_code_patch(city_code, body=None):  # noqa: E501
    """UpdateCity

     # noqa: E501

    :param city_code: 
    :type city_code: str
    :param body: 
    :type body: dict | bytes

    :rtype: object
    """
    if connexion.request.is_json:
        body = str.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def cities_get(city_code=None):  # noqa: E501
    """GetCityByCode

     # noqa: E501

    :param city_code: 
    :type city_code: str

    :rtype: object
    """
    return 'do some magic!'


def cities_post(body=None):  # noqa: E501
    """AddCity

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: object
    """
    if connexion.request.is_json:
        body = object.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
