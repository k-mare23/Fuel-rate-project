import unittest
import requests
#import views

class Test(unittest.TestCase):
        #client profile module unit test
        def test_create_profile(self):
            response = requests.get('http://127.0.0.1:5000/client_profile')
            self.assertEqual(response.status_code, 200)
        
        def test_full_name_length(self):
            response = requests.post('http://127.0.0.1:5000/client_profile',
                                 data={'fullname': '', 'address': 'abcd', 'address2': '1234',
                                       'city': 'Houston', 'state': 'TX', 'zip code': '1111111'})
            self.assertTrue('Full name must be between 1 and 50 characters.' in response.text)

        def test_address_length(self):
            response = requests.post('http://127.0.0.1:5000/client_profile',
                                 data={'fullname': 'abcd', 'address': '', 'address2': '1234',
                                       'city': 'Houston', 'state': 'TX', 'zip code': '1111111'})
            self.assertTrue('Address must be between 1 and 100 characters.' in response.text)

        def test_city_length(self):
            response = requests.post('http://127.0.0.1:5000/client_profile',
                                 data={'fullname': 'abcd', 'address': 'abcd', 'address2': '1234',
                                       'city': '', 'state': 'TX', 'zip code': '1111111'})
            self.assertTrue('City must be between 1 and 100 characters.' in response.text)

        def test_state_length(self):
            response = requests.post('http://127.0.0.1:5000/client_profile',
                                 data={'fullname': 'abcd', 'address': 'abcd', 'address2': '1234',
                                       'city': 'Houston', 'state': 'TXS', 'zip code': '1111111'})
            self.assertTrue('State must be in two character format' in response.text)

        def test_zipcode_length(self):
            response = requests.post('http://127.0.0.1:5000/client_profile',
                                 data={'fullname': 'abcd', 'address': 'abcd', 'address2': '1234',
                                       'city': 'Houston', 'state': 'TX', 'zipcode': '11'})
            self.assertTrue('Zip code must be between 5 and 9 characters.' in response.text)
        #end client profile module unit test