
import requests
def agify_clientapi():
    print('welcome to agify client api')
    url = 'https://api.agify.io/?name[]=michael&name[]=bill&country_id=EG'
    response = requests.get(url)
    print(response.status_code)
    print(response.json())
    print(response.json()[0]['name'] + ' is ' + str(response.json()[0]['age']) + ' years old in ' + response.json()[0]['country_id'])
agify_clientapi()

