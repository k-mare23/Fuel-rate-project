import unittest
import requests
#import views

class Test(unittest.TestCase):
        def test_create_profile(self):
            response = requests.get('http://127.0.0.1:5000/client_profile')
            self.assertEqual(response.status_code, 200)
        
        def test_full_name_length(self):
            response = requests.post('http://127.0.0.1:5000/client_profile',
                                 data={'fullname': '', 'address': 'abcd', 'address2': '1234',
                                       'city': 'Houston', 'state': 'TX', 'zip code': '1111111'})
            self.assertTrue('Full name must be between 1 and 50 characters.' in response.text)