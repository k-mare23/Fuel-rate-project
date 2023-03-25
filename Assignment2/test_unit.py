import unittest
import requests
#import views

class Test(unittest.TestCase):
    def test_login(self):
        # Ensure that Flask was set up correctly
        response = requests.get('http://127.0.0.1:5000/login')
        self.assertEqual(response.status_code, 200)

    def test_correct_login(self):
        response = requests.post('http://127.0.0.1:5000/login', data={'username': 'xyz', 'password1': '12345678'})
        self.assertTrue('Logged in successfully!' in response.text)

    def test_not_an_user_login(self):
        response = requests.post('http://127.0.0.1:5000/login', data={'username': 'xxx', 'password1': '12345678'})
        self.assertTrue('Username does not exist.' in response.text)

    def test_wrong_password_login(self):
        response = requests.post('http://127.0.0.1:5000/login',
                                 data={'username': 'xyz', 'password1': '123456789'})
        self.assertTrue('Incorrect password, try again.' in response.text)

    def test_home(self):
        response = requests.post('http://127.0.0.1:5000/login', data={'username': 'xyz', 'password1': '12345678'})
        response = requests.get('http://127.0.0.1:5000/')
        self.assertEqual(response.status_code, 200)
    
      
        
if __name__ == '__main__':
    unittest.main()
