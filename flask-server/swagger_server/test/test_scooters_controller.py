# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.array_of_scooter import ArrayOfScooter  # noqa: E501
from swagger_server.models.scooter import Scooter  # noqa: E501
from swagger_server.test import BaseTestCase


class TestScootersController(BaseTestCase):
    """ScootersController integration test stubs"""

    def test_add_scooter(self):
        """Test case for add_scooter

        Add a new scooter
        """
        body = Scooter()
        response = self.client.open(
            '/v2/scooters',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_scooter(self):
        """Test case for delete_scooter

        Deletes a scooter
        """
        response = self.client.open(
            '/v2/scooters/{licensePlate}'.format(licensePlate='licensePlate_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_available_scooters(self):
        """Test case for get_available_scooters

        Get all available scooters
        """
        response = self.client.open(
            '/v2/scooters',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_scooter_by_license_plate(self):
        """Test case for get_scooter_by_license_plate

        Find scooter by license plate
        """
        response = self.client.open(
            '/v2/scooters/{licensePlate}'.format(licensePlate='licensePlate_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_scooter(self):
        """Test case for update_scooter

        Update an existing scooter
        """
        response = self.client.open(
            '/v2/scooters/{licensePlate}'.format(licensePlate='licensePlate_example'),
            method='PUT',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
