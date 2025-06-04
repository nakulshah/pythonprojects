import requests

class ShopsApiClient:
    def __init__(self, base_url='http://127.0.0.1:5000'):
        self.base_url = base_url

    def create_shelf(self, shelf_name):
        url = f"{self.base_url}/shop/shelves"
        response = requests.post(url, json={'shelf_name': shelf_name})
        return response.json(), response.status_code

    def add_product(self, shelf_name, product_name):
        url = f"{self.base_url}/shop/shelves/{shelf_name}/products"
        response = requests.post(url, json={'product': product_name})
        return response.json(), response.status_code

    def list_shelves(self):
        url = f"{self.base_url}/shop/shelves"
        response = requests.get(url)
        return response.json(), response.status_code

    def list_products(self, shelf_name):
        url = f"{self.base_url}/shop/shelves/{shelf_name}/products"
        response = requests.get(url)
        return response.json(), response.status_code

# Example usage:
if __name__ == "__main__":
    client = ShopsApiClient()
    print(client.create_shelf("Books"))
    print(client.add_product("Books", "Python 101"))
    print(client.list_shelves())
    print(client.list_products("Books"))