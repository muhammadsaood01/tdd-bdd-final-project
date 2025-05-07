import unittest
from urllib.parse import quote_plus
from app import app, BASE_URL, Product
from flask import jsonify
from http import HTTPStatus as status


class TestProductAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test environment before any tests."""
        cls.client = app.test_client()

    def test_create_product(self):
        """It should create a new Product"""
        test_product = {"name": "Test Product", "category": "Test Category", "description": "Test Description", "price": 100}
        response = self.client.post(BASE_URL, json=test_product)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_product = response.get_json()
        self.assertEqual(created_product["name"], test_product["name"])
        self.assertEqual(created_product["category"], test_product["category"])

    def test_update_product(self):
        """It should Update an existing Product"""
        test_product = {"name": "Update Product", "category": "Update Category", "description": "Update Description", "price": 150}
        response = self.client.post(BASE_URL, json=test_product)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_product = response.get_json()
        new_product["description"] = "Updated Description"
        response = self.client.put(f"{BASE_URL}/{new_product['id']}", json=new_product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_product = response.get_json()
        self.assertEqual(updated_product["description"], "Updated Description")

    def test_delete_product(self):
        """It should Delete a Product"""
        test_product = {"name": "Delete Product", "category": "Delete Category", "description": "Delete Description", "price": 200}
        response = self.client.post(BASE_URL, json=test_product)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product = response.get_json()
        product_count = self.get_product_count()

        response = self.client.delete(f"{BASE_URL}/{product['id']}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)

        response = self.client.get(f"{BASE_URL}/{product['id']}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        new_count = self.get_product_count()
        self.assertEqual(new_count, product_count - 1)

    def test_get_product_list(self):
        """It should Get a list of Products"""
        self._create_products(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_query_by_name(self):
        """It should Query Products by name"""
        products = self._create_products(5)
        test_name = products[0].name
        name_count = len([product for product in products if product.name == test_name])
        response = self.client.get(BASE_URL, query_string=f"name={quote_plus(test_name)}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), name_count)
        for product in data:
            self.assertEqual(product["name"], test_name)

    def test_query_by_category(self):
        """It should Query Products by category"""
        products = self._create_products(10)
        category = products[0].category
        found = [product for product in products if product.category == category]
        found_count = len(found)
        response = self.client.get(BASE_URL, query_string=f"category={quote_plus(category)}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), found_count)
        for product in data:
            self.assertEqual(product["category"], category)

    def test_query_by_availability(self):
        """It should Query Products by availability"""
        products = self._create_products(5)
        available = [product for product in products if product["available"]]
        available_count = len(available)
        response = self.client.get(BASE_URL, query_string="available=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), available_count)
        for product in data:
            self.assertTrue(product["available"])

    def get_product_count(self):
        """Helper method to get the number of products"""
        response = self.client.get(BASE_URL)
        return len(response.get_json())

    def _create_products(self, count):
        """Helper method to create a list of products"""
        products = []
        for _ in range(count):
            product = {"name": "Test Product", "category": "Test Category", "description": "Test Description", "price": 100}
            response = self.client.post(BASE_URL, json=product)
            products.append(response.get_json())
        return products


if __name__ == "__main__":
    unittest.main()
