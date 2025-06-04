import unittest
from shopsapi import create_app, db

class ShopsApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_hello_shop(self):
        response = self.client.get('/shop/hello')
        # pretty print the response for debugging
        print(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': 'Hello, Shop!'})

    def test_create_shelf(self):
        response = self.client.post('/shop/shelves', json={'shelf_name': 'Books'})
        # pretty print the response for debugging
        print(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 201)
        self.assertIn('Shelf Books created.', response.get_json()['message'])

    def test_create_duplicate_shelf(self):
        self.client.post('/shop/shelves', json={'shelf_name': 'Books'})
        response = self.client.post('/shop/shelves', json={'shelf_name': 'Books'})
        # pretty print the response for debugging
        print(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 400)
        self.assertIn('Shelf already exists.', response.get_json()['error'])

    def test_add_product(self):
        self.client.post('/shop/shelves', json={'shelf_name': 'Books'})
        response = self.client.post('/shop/shelves/Books/products', json={'product': 'Python 101'})
        # pretty print the response for debugging
        print(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 201)
        self.assertIn('Product added to Books.', response.get_json()['message'])

    def test_add_product_to_nonexistent_shelf(self):
        response = self.client.post('/shop/shelves/Unknown/products', json={'product': 'Python 101'})
        self.assertEqual(response.status_code, 404)
        # pretty print the response for debugging
        print(response.get_data(as_text=True))
        self.assertIn('Shelf does not exist.', response.get_json()['error'])

    def test_list_shelves(self):
        self.client.post('/shop/shelves', json={'shelf_name': 'Books'})
        self.client.post('/shop/shelves', json={'shelf_name': 'Games'})
        response = self.client.get('/shop/shelves')
        # pretty print the response for debugging
        print(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Books', response.get_json())
        self.assertIn('Games', response.get_json())

    def test_list_products(self):
        self.client.post('/shop/shelves', json={'shelf_name': 'Books'})
        self.client.post('/shop/shelves/Books/products', json={'product': 'Python 101'})
        self.client.post('/shop/shelves/Books/products', json={'product': 'Flask for Fun'})
        response = self.client.get('/shop/shelves/Books/products')
        # pretty print the response for debugging
        print(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Python 101', response.get_json())
        self.assertIn('Flask for Fun', response.get_json())

    def test_list_products_nonexistent_shelf(self):
        response = self.client.get('/shop/shelves/Unknown/products')
        # pretty print the response for debugging
        print(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 404)
        self.assertIn('Shelf does not exist.', response.get_json()['error'])

if __name__ == '__main__':
    unittest.main()