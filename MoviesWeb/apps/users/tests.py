from django.test import TestCase

# Create your tests here.

class UsersTestCase(TestCase):
    def test_register_user(self):
        response = self.client.post('/apps/users/', {'username': 'TestAntoLDM17', 'password': 'Password123'})
        self.assertEqual(response.status_code, 201)
        self.assertTrue('id' in response.data)
        self.assertTrue('username' in response.data)
        self.assertTrue('password' not in response.data)
        
    def test_login_user(self):
        response = self.client.post('/apps/users/', {'username': 'TestAntoLDM17', 'password': 'Password123'})
        self.assertEqual(response.status_code, 201)
        
        response = self.client.post('/apps/users/login/', {'username': 'TestAntoLDM17', 'password': 'Password123'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)
        
        
        