import unittest
import requests
from Fuel_go import views
from Fuel_go import auth
import random
import string
from Fuel_go import db
from Fuel_go import models


class MyTestCase(unittest.TestCase):
    # Ensure login behaves correctly given the correct credential
    def test_login(self):
        # Ensure that Flask was set up correctly
        response = requests.get('http://127.0.0.1:5000/login')
        self.assertEqual(response.status_code, 200)

    def test_correct_login(self):
        response = requests.post('http://127.0.0.1:5000/login', data={'username': 'Dave', 'password1': '12345678'})
        self.assertTrue('Logged in successfully!' in response.text)

    def test_not_an_user_login(self):
        response = requests.post('http://127.0.0.1:5000/login', data={'username': 'Anon', 'password1': '12345678'})
        self.assertTrue('Username does not exist.' in response.text)

    def test_wrong_password_login(self):
        response = requests.post('http://127.0.0.1:5000/login',
                                 data={'username': 'Dave', 'password1': '123456789'})
        self.assertTrue('Incorrect password, try again.' in response.text)

    def test_home(self):
        response = requests.post('http://127.0.0.1:5000/login', data={'username': 'Dave', 'password1': '12345678'})
        response = requests.get('http://127.0.0.1:5000/')
        self.assertEqual(response.status_code, 200)


        ############################################################################################
    #testing client registration 
    def test_sign_up(self):
        response = requests.get('http://127.0.0.1:5000/client_registration')
        self.assertEqual(response.status_code, 200)

    def test_correct_sign_up(self):
        letters = string.ascii_lowercase
        user_name = ''.join(random.choice(letters) for i in range(10))
        response = requests.post('http://127.0.0.1:5000/client_registration',
                                 data={'username': user_name, 'email': 'Dave@gmail.com', 'password1': '12345678',
                                       'password2': '12345678'})
        self.assertTrue('Account created!' in response.text)

    def test_exist_username_sign_up(self):
        response = requests.post('http://127.0.0.1:5000/client_registration',
                                 data={'username': 'Dave', 'email': 'Dave@gmail.com', 'password1': '12345678',
                                       'password2': '12345678'})
        self.assertTrue('Username already exists.' in response.text)

    def test_password_not_match_sign_up(self):
        response = requests.post('http://127.0.0.1:5000/client_registration',
                                 data={'username': 'Dave', 'email': 'Dave@gmail.com', 'password1': '12345678',
                                       'password2': '123456789'})
        self.assertTrue('Passwords do not match.' in response.text)

    def test_password_too_short_sign_up(self):
        response = requests.post('http://127.0.0.1:5000/client_registration',
                                 data={'username': 'Dave', 'email': 'Dave@gmail.com', 'password1': '123',
                                       'password2': '123'})
        self.assertTrue('Password must be at least 8 characters.' in response.text)

#######################################################################################
    #testing log out
    def test_logout(self):
        s = requests.Session()
        s.post('http://127.0.0.1:5000/login', data={'username': 'Dave', 'password1': '12345678'})

        response = s.get('http://127.0.0.1:5000/logout')
        self.assertTrue('Logged out successfully!' in response.text)

########################################################################################
    #Test create profile
    def test_create_profile(self):
        response = requests.get('http://127.0.0.1:5000/profilepage')
        self.assertEqual(response.status_code, 200)

    def test_post_create_profile(self):
        s = requests.Session()
        letters = string.ascii_lowercase
        user_name = ''.join(random.choice(letters) for i in range(10))
        response = s.post('http://127.0.0.1:5000/client_registration',
                          data={'username': user_name, 'email': 'Dave@gmail.com', 'password1': '12345678',
                                'password2': '12345678'})
        fullname = ''.join(random.choice(letters) for i in range(5))
        response = s.post('http://127.0.0.1:5000/profilepage',
                          data={'fullname': fullname, 'address1': '1234', 'address2': 'summer',
                                'city': 'Houston', 'state': 'TX', 'zipcode': '1111111'})
        self.assertTrue('Profile created!' in response.text)

    def test_full_name_too_short_profile(self):
        response = requests.post('http://127.0.0.1:5000/profilepage',
                                 data={'fullname': 'D', 'address1': '1234', 'address2': 'summer',
                                       'city': 'acb', 'state': 'TX', 'zipcode': '1111111'})
        self.assertTrue('Full name must be between 2 and 50 characters.' in response.text)

    def test_address_too_short_profile(self):
        response = requests.post('http://127.0.0.1:5000/profilepage',
                                 data={'fullname': 'xmnnc', 'address1': '1', 'address2': 'summer',
                                       'city': 'acb', 'state': 'TX', 'zipcode': '1111111'})
        self.assertTrue('Address must be between 2 and 100 characters.' in response.text)

    def test_city_too_short_profile(self):
        response = requests.post('http://127.0.0.1:5000/profilepage',
                                 data={'fullname': 'xmnnc', 'address1': '1234', 'address2': 'summer',
                                       'city': 'a', 'state': 'TX', 'zipcode': '1111111'})
        self.assertTrue('City must be between 2 and 100 characters.' in response.text)

    def test_state_not_two_profile(self):
        response = requests.post('http://127.0.0.1:5000/profilepage',
                                 data={'fullname': 'xmnnc', 'address1': '1234', 'address2': 'summer',
                                       'city': 'abc', 'state': 'TXS', 'zipcode': '1111111'})
        self.assertTrue('Reselect state.' in response.text)

    def test_zipcode_not_correct_profile(self):
        response = requests.post('http://127.0.0.1:5000/profilepage',
                                 data={'fullname': 'xmnnc', 'address1': '1234', 'address2': 'summer',
                                       'city': 'abc', 'state': 'TX', 'zipcode': '11'})
        self.assertTrue('Zipcode must be between 5 and 9 characters.' in response.text)


########################################################################################################
    #Test fuel quote form
    def test_get_fuel_quote_form(self):
        s = requests.Session()
        s.post('http://127.0.0.1:5000/loginpage', data={'username': 'Dave', 'password1': '12345678'})
        response = s.get('http://127.0.0.1:5000/fuel-quote')
        self.assertEqual(response.status_code, 200)

    def test_post_fuel_quote_form(self):
        s = requests.Session()
        s.post('http://127.0.0.1:5000/loginpage', data={'username': 'Dave', 'password1': '12345678'})
        response = s.post('http://127.0.0.1:5000/fuel-quote',
                          data={'Total_Gallons_Requested': '100', 'delivery_date': '2023-01-01',
                                'delivery_Address': 'xysdgahdgsahd, FL'})
        self.assertTrue('Suggest price created!' in response.text)

    def test_first_post_fuel_quote_form(self):
        s = requests.Session()
        letters = string.ascii_lowercase
        user_name = ''.join(random.choice(letters) for i in range(10))
        response = s.post('http://127.0.0.1:5000/registration',
                          data={'username': user_name, 'email': 'Dave@gmail.com', 'password1': '12345678',
                                'password2': '12345678'})
        fullname = ''.join(random.choice(letters) for i in range(5))
        response = s.post('http://127.0.0.1:5000/profilepage',
                          data={'fullname': fullname, 'address1': '1234', 'address2': 'summer',
                                'city': 'xyz', 'state': 'TX', 'zipcode': '1111111'})
        response = s.post('http://127.0.0.1:5000/fuel-quote',
                          data={'Total_Gallons_Requested': '1050', 'delivery_date': '2023-01-01',
                                'delivery_Address': '1800 summer, TX'})
        self.assertTrue('Suggest price created!' in response.text)

    def test_get_fuel_quote_result(self):
        s = requests.Session()
        s.post('http://127.0.0.1:5000/loginpage', data={'username': 'Dave', 'password1': '12345678'})
        s.post('http://127.0.0.1:5000/fuel-quote',
               data={'Total_Gallons_Requested': '100', 'delivery_date': '2023-01-01',
                     'delivery_Address': '5200 winter, CO'})

        response = s.get('http://127.0.0.1:5000/fuel-quote-result')
        self.assertEqual(response.status_code, 200)

    def test_post_fuel_quote_result(self):
        s = requests.Session()
        s.post('http://127.0.0.1:5000/loginpage', data={'username': 'Dave', 'password1': '12345678'})
        s.post('http://127.0.0.1:5000/fuel-quote',
               data={'Total_Gallons_Requested': '100', 'delivery_date': '2023-01-01',
                     'delivery_Address': '3493 spring, NY'})

        response = s.post('http://127.0.0.1:5000/fuel-quote-result')
        self.assertTrue('Quote result added!' in response.text)

    def test_get_fuel_history(self):
        s = requests.Session()
        s.post('http://127.0.0.1:5000/loginpage', data={'username': 'Dave', 'password1': '12345678'})
        response = s.get('http://127.0.0.1:5000/fuel-quote-history')
        self.assertEqual(response.status_code, 200)


###########################################################################################################
    #Test home page
    def test_homepage(self):
        response = requests.get('http://127.0.0.1:5000/homepage')
        self.assertEqual(response.status_code, 200) 

###########################################################################################################
    def test_db_user(self):
        new_user = models.User(first_name="Dave", email="Dave@gmail.com", password=
                    "12345678")
        db.session.add(new_user)
        db.session.commit()
        user = models.User.query.filter_by(first_name = "Dave")
        self.assertTrue(user)

    def test_db_profile(self):
        new_user_profile = models.Profile(full_name= "Dave", address1="1234", address2="Summer Shine", city="Houston",
                                      state="TX", zipcode="1111111")
        db.session.add(new_user_profile)
        db.session.commit()
        profile = models.Profile.query.filter_by(address1 = "1234").first()
        self.assertTrue(profile)

    def test_db_quote(self):
        new_quote_result = models.Quote(gallons_requested=100,
                                 delivery_address="Summer lane",
                                 date="2023-01-01",
                                 suggest_price=49.99,
                                 total_price=75
                                 )
        db.session.add(new_quote_result)
        db.session.commit()
        quote = models.Quote.query.filter_by(gallons_requested = 100).first()
        self.assertTrue(quote)


if __name__ == '__main__':
    unittest.main()
