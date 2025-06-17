import random
import requests


class MathClient:
    def __init__(self, server_url='http://127.0.0.1:5000'):
        self.server_url = server_url

    def add(self, a, b):
        url = f"{self.server_url}/mathapi/add/{a}/{b}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('result')
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def subtract(self, a, b):
        #throw not implemented error
        raise NotImplementedError("Subtract method is not implemented yet.")

    def multiply(self, a, b):
        # throw not implemented error
        raise NotImplementedError("multiply method is not implemented yet.")

    def divide(self, a, b):
        # throw not implemented error
        raise NotImplementedError("divide method is not implemented yet.")

# Example usage:
if __name__ == "__main__":
    client = MathClient()
    try:
        a = random.randint(1, 100)
        b = random.randint(1, 100)

        result = client.add(a, b)
        print(f"{a} + {b} = {result}")

        result = client.subtract(a, b)
        print(f"{a} + {b} = {result}")
    except Exception as e:
        print(e)