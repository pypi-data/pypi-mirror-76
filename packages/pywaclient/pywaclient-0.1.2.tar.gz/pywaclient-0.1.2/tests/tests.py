import unittest
import logging
import os
import sys

from pywaclient import AragornApiClient

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

class TestEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = AragornApiClient(
            name='TEST APPLICATION',
            url='https://gitlab.com/SoulLink/world-anvil-api-client',
            application_key=os.environ.get('WA_APPLICATION_KEY'),
            authentication_token=os.environ.get('WA_AUTH_TOKEN'),
            version='0.1.0'
        )

    def testAuthenticatedUser(self):
        self.assertEqual('42eb1d6a-021b-49b4-bbbb-f7ddf6b135a4', self.client.user.authenticated_user_id)

    def testUserEndpointWorlds(self):
        self.assertEqual('8f312eff-fdcc-49d1-9626-a98af28ada54', self.client.user.worlds()[0]['id'])

    def testUserEndpointManuscripts(self):
        self.assertEqual('09ecd340-4cf4-4940-85d9-99648d221c29', self.client.user.manuscripts()[0]['id'])


if __name__ == '__main__':
    unittest.main()
