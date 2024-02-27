"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src import status


class CounterTest(TestCase):
    """Counter tests"""

    def setUp(self):
        self.client = app.test_client()

    def test_create_a_counter(self):
        """It should create a counter"""
        result = self.client.post("/counters/foo")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post("/counters/bar")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post("/counters/bar")
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """It should update the counter by 1 when a PUT request is made"""

        # Post a new counter called 'jordan'
        name = "jordan"
        result = self.client.post(f"/counters/{name}")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        counter = result.get_json()[name]

        # Update the counter via PUT
        result = self.client.put(f"/counters/{name}")
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        new_counter = result.get_json()[name]

        self.assertEqual(new_counter, counter + 1)

    def test_get_a_counter(self):
        """It should GET a counter"""

        # Post a new counter called 'jordan'
        name = "businge"
        result = self.client.post(f"/counters/{name}")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        counter = result.get_json()

        # Retrieve the counter via GET
        result = self.client.get(f"/counters/{name}")
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        retrieved_counter = result.get_json()

        self.assertEqual(counter, retrieved_counter)

    def test_delete_a_counter(self):
        """It should delete the specified counter"""

        # Create a new counter called 'marks
        name = "marks"
        result = self.client.post(f"/counters/{name}")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        # Delete the newly created counter.
        result = self.client.delete(f"/counters/{name}")
        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)

        # Ensure the counter was actually deleted.
        result = self.client.get(f"/counters/{name}")
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)
