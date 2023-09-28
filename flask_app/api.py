import requests
import json

# business_id

API_KEY = 'jzvN63lO1O2HKV-LwLdQeDpOmyoEI4IkMG4qJfQK2hWP4rOAZsy0XdziYkUusfWH5g5FKT3d5ANY4Q5U79CUqjFe3OwEjlDmkLO6mPGHILUwBjt2k4Y9gj3P42WeZHYx'
ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': 'bearer %s' % API_KEY}


PARAMETERS = {'term': 'Food',
                'limit': 50,
                'radius': 1000,
                'location': 'San Francisco' }

# This will make a request from the yelp API
response = requests.get(url = ENDPOINT, params = PARAMETERS, headers = HEADERS)

# convert the JSON String this will convert it to a dictionary
business_data = response.json()

# Print the response
print(json.dumps(business_data, indent=3))

for biz in business_data['businesses']:
    print(biz['name'])
