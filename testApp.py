import unittest
import json
from flask import Flask
from pymongo import MongoClient
from bson.objectid import ObjectId

# Import the app from your main file
from app import app, collection

class CRUDTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setup before any tests are run
        cls.client = app.test_client()
        cls.client.testing = True
        cls.test_data = {"name" : "hello","img" : "https://bit.ly/2Pzczl8", "summary" :"Adrift in space with no food or water, Tony Stark sends a message to P…" }

    

    def test_add_record_failure(self):
        self.test_data = "{name : hello}"
        response = self.client.post('/api/add_record', json=self.test_data)
        self.assertEqual(response.status_code, 500)

    def test_add_record_success(self):
        response = self.client.post('/api/add_record', json=self.test_data)
        self.assertEqual(response.status_code,201)

    def test_update_item_failure(self):
        response = self.client.put('/api/items/664f902b8ef72f886636d99b', json=self.test_data)
        self.assertEqual(response.status_code,404)

    def test_update_item_success(self):
        response = self.client.put('/api/items/66508ab4453efe3b77d68205', json=self.test_data)
        self.assertEqual(response.status_code,200)
    
    def test_delete_item_success(self):
        response = self.client.delete('/api/delete_record/665097549bd99192c31e3330', json=self.test_data)
        self.assertEqual(response.status_code,201)

        

    
if __name__ == '__main__':
    unittest.main()