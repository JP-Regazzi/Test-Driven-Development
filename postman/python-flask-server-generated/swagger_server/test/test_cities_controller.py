# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestCitiesController(BaseTestCase):
    """CitiesController integration test stubs"""

    def test_cities_city_code_delete(self):
        """Test case for cities_city_code_delete

        DeleteCity
        """
        response = self.client.open(
            '/Cities/{CityCode}'.format(city_code='city_code_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cities_city_code_patch(self):
        """Test case for cities_city_code_patch

        UpdateCity
        """
        body = 'body_example'
        response = self.client.open(
            '/Cities/{CityCode}'.format(city_code='city_code_example'),
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cities_get(self):
        """Test case for cities_get

        GetCityByCode
        """
        query_string = [('city_code', 'city_code_example')]
        response = self.client.open(
            '/Cities',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cities_post(self):
        """Test case for cities_post

        AddCity
        """
        body = None
        response = self.client.open(
            '/Cities',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
