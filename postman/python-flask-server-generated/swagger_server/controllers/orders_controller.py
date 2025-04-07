import connexion
import six

from swagger_server import util


def flight_orders_delete():  # noqa: E501
    """DeleteAllOrders

     # noqa: E501


    :rtype: object
    """
    return 'do some magic!'


def flight_orders_get(customer_name=None):  # noqa: E501
    """GetCustomerOrder

     # noqa: E501

    :param customer_name: 
    :type customer_name: str

    :rtype: str
    """
    return 'do some magic!'


def flight_orders_order_number_delete(order_number):  # noqa: E501
    """DeleteOrder

     # noqa: E501

    :param order_number: 
    :type order_number: str

    :rtype: object
    """
    return 'do some magic!'


def flight_orders_order_number_get(order_number):  # noqa: E501
    """GetOrder

     # noqa: E501

    :param order_number: 
    :type order_number: str

    :rtype: object
    """
    return 'do some magic!'


def flight_orders_order_number_patch(order_number, body=None):  # noqa: E501
    """UpdateOrder

     # noqa: E501

    :param order_number: 
    :type order_number: str
    :param body: 
    :type body: dict | bytes

    :rtype: object
    """
    if connexion.request.is_json:
        body = object.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def flight_orders_post(body=None):  # noqa: E501
    """BookFight

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = object.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
