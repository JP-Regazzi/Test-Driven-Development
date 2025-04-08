# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestFlightsController(BaseTestCase):
    """FlightsController integration test stubs"""

    def test_flights_flight_number_delete(self):
        """Test case for flights_flight_number_delete

        DeleteFlight
        """
        response = self.client.open(
            '/Flights/{FlightNumber}'.format(flight_number='flight_number_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_flights_flight_number_get(self):
        """Test case for flights_flight_number_get

        GetFlight
        """
        response = self.client.open(
            '/Flights/{FlightNumber}'.format(flight_number='flight_number_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_flights_get(self):
        """Test case for flights_get

        SearchFlights
        """
        query_string = [('departure_city', 'departure_city_example'),
                        ('arrival_city', 'arrival_city_example'),
                        ('_date', '_date_example')]
        response = self.client.open(
            '/Flights',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_flights_post(self):
        """Test case for flights_post

        AddFlight
        """
        body = 'body_example'
        response = self.client.open(
            '/Flights',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_random_flights_get(self):
        """Test case for random_flights_get

        RandomFlights
        """
        query_string = [('count', 56)]
        response = self.client.open(
            '/RandomFlights',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
