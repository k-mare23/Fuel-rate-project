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
        
    def test_sign_up(self):
        response = requests.get('http://127.0.0.1:5000/client_registration')
        self.assertEqual(response.status_code, 200)

    def test_correct_sign_up(self):
        letters = string.ascii_lowercase
        user_name = ''.join(random.choice(letters) for i in range(10))
        response = requests.post('http://127.0.0.1:5000/client_registration',
                                 data={'username': user_name, 'email': 'ppp@gmail.com', 'password1': '12345678',
                                       'password2': '12345678'})
        self.assertTrue('Account created!' in response.text)

    def test_exist_username_sign_up(self):
        response = requests.post('http://127.0.0.1:5000/client_registration',
                                 data={'username': 'xyz', 'email': 'ppp@gmail.com', 'password1': '12345678',
                                       'password2': '12345678'})
        self.assertTrue('Username already exists.' in response.text)

    def test_password_not_match_sign_up(self):
        response = requests.post('http://127.0.0.1:5000/client_registration',
                                 data={'username': 'aaaxxx', 'email': 'ppp@gmail.com', 'password1': '12345678',
                                       'password2': '123456789'})
        self.assertTrue('Passwords don&#39;t match.' in response.text)

    def test_password_too_short_sign_up(self):
        response = requests.post('http://127.0.0.1:5000/client_registration',
                                 data={'username': 'aaa', 'email': 'ppp@gmail.com', 'password1': '123',
                                       'password2': '123'})
        self.assertTrue('Password must be at least 8 characters.' in response.text)

#######################################################################################
    def test_logout(self):
        s = requests.Session()
        s.post('http://127.0.0.1:5000/login', data={'username': 'xyz', 'password1': '12345678'})

        response = s.get('http://127.0.0.1:5000/logout')
        self.assertTrue('Logged out successfully!' in response.text)

    
      
        
if __name__ == '__main__':
    unittest.main()
