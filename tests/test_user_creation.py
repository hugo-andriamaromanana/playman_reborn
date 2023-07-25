from src.user_creation import *
import unittest

class TestUserCreation(unittest.TestCase):
    
    def test_get_channel_ID(self):
        self.assertEqual(get_channel_ID('Hugo'), 'UCsJ6SLKMBc_ek9BEkdqjfWQ')
        self.assertNotEqual(get_channel_ID('Luc'), 'UCsJ6SLKMBc_ek9BEkdqjfWQ')
    
    def test_user_exist(self):
        self.assertTrue(user_exist('Hugo'))
        self.assertFalse(user_exist('Harold'))
    
    