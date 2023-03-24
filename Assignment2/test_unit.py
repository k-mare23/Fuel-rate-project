import unittest
import requests
#import views

class Test(unittest.TestCase):
        def test_create_profile(self):
            response = requests.get('http://127.0.0.1:5000/client_profile')
            self.assertEqual(response.status_code, 200)