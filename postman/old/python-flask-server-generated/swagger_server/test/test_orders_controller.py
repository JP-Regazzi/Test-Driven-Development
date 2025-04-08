# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestOrdersController(BaseTestCase):
    """OrdersController integration test stubs"""

    def test_flight_orders_delete(self):
        """Test case for flight_orders_delete

        DeleteAllOrders
        """
        response = self.client.open(
            '/FlightOrders',
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_flight_orders_get(self):
        """Test case for flight_orders_get

        GetCustomerOrder
        """
        query_string = [('customer_name', 'customer_name_example')]
        response = self.client.open(
            '/FlightOrders',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_flight_orders_order_number_delete(self):
        """Test case for flight_orders_order_number_delete

        DeleteOrder
        """
        response = self.client.open(
            '/FlightOrders/{OrderNumber}'.format(order_number='order_number_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_flight_orders_order_number_get(self):
        """Test case for flight_orders_order_number_get

        GetOrder
        """
        response = self.client.open(
            '/FlightOrders/{OrderNumber}'.format(order_number='order_number_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_flight_orders_order_number_patch(self):
        """Test case for flight_orders_order_number_patch

        UpdateOrder
        """
        body = None
        response = self.client.open(
            '/FlightOrders/{OrderNumber}'.format(order_number='order_number_example'),
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_flight_orders_post(self):
        """Test case for flight_orders_post

        BookFight
        """
        body = None
        response = self.client.open(
            '/FlightOrders',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
