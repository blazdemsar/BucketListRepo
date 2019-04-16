import unittest
from unittest import TestCase

from flask import url_for, session

from app import app, users
from activity import Activity 
from user import User
from bucketlist import BucketList

class BucketListTest(TestCase):
    def setUp(self):        
        app.config['SECRET_KEY'] = 'seasasaskrit!'
        # creates a test client
        self.client = app.test_client()
        
        self.client.testing = True
        
    
    def test_success(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.client.get('/login')
        self.assertEqual(result.status_code, 200)

    def test_failure(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.client.get('/nonexistant.html')
        self.assertEqual(result.status_code, 404)
    
    def test_login_page_loads(self):
        # assert login page loads correctly
        result = self.client.get('/login')
        self.assertTrue(b'The best way to keep track of your dreams and goals' in result.data)

    # def test_logout_redirects_user(self):
    #     user = User('hermano', 'herm@email.com', 'hard')
    #     users['herm@email.com'] = user

    #     self.client.post('login', data={
    #         'username': 'hermano',
    #         'password': 'hard'
    #     })
    #     # assert login page loads correctly
    #     result = self.client.get('/logout')
    #     self.assertTrue(result.status_code == 302)

    def test_signup_page_posts_and_redirects(self):
        result = self.client.post('signup', data={
            'username': 'hermano',
            'email': 'herm@email.com',
            'password': 'hard',
            'confirm_password': 'hard'
        })
        self.assertTrue(result.status_code == 302)

    def test_signup_redirects_to_add_bucketlist(self):
        result = self.client.post('signup', data={
            'username': 'hermano',
            'email': 'herm@email.com',
            'password': 'hard',
            'confirm_password': 'hard'
        }, follow_redirects = True)
        self.assertIn(b'My Bucket Lists', result.data)

    # def test_login_page_posts_and_redirects(self):
    #     user = User('hermano', 'herm@email.com', 'hard')
    #     users['herm@email.com'] = user

    #     result = self.client.post('login', data={
    #         'username': 'hermano',
    #         'password': 'hard'
    #     })
    #     self.assertTrue(result.status_code == 302)

    def test_successful_login_redirects_to_managelists(self):
        user = User('hermano', 'herm@email.com', 'hard')
        users['herm@email.com'] = user

        result = self.client.post('login', data={
            'username': 'hermano',
            'password': 'hard'
        }, follow_redirects = True)
        self.assertIn(b'My Bucket Lists', result.data)

    def test_add_bucketlist_successfully_to_user(self):
        user = User('hermano', 'herm@email.com', 'hard')
        users['herm@email.com'] = user
        
        initial_no_of_bucketlists = len(user.bucketlists)

        bktlist = BucketList('Recipes', 'Learn to cook different')
        user.bucketlists['Recipes'] = bktlist

        self.assertEqual(len(user.bucketlists) - initial_no_of_bucketlists, 1)

    def test_add_activity_successfully_to_bucketlist(self):
        bucketlist = BucketList('Travels', 'Tour Africa')
        activity = Activity('Egypt', 'Visit the Pyramids')
        
        initial_no_of_activities = len(bucketlist.activities)

        bucketlist.add_activity(activity)

        self.assertEqual(len(bucketlist.activities) - initial_no_of_activities, 1)

    def test_user_has_property_bucketlists(self):
        user = User('hermano', 'herm@email.com', 'hard')
        users['herm@email.com'] = user
        self.assertTrue(hasattr(user, 'bucketlists'))

    def test_bucket_list_is_instance_of_BucketList(self):
        bktlist = BucketList('Recipes', 'Learn to cook different')
        self.assertEqual(isinstance(bktlist, BucketList), True)


    

if __name__ == '__main__':
    unittest.main()
