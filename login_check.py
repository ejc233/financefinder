# This is written for PYTHON 3
# Don't forget to install requests package

import requests
import json

apiKey = '0e5699be695712bf95845e1388604fd4'

def addaccount():
	url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerId,apiKey)
	payload = {
	  "type": "Savings",
	  "nickname": "testman",
	  "rewards": 10000,
	  "balance": 10000,	
	}
	# Create a Savings Account
	response = requests.post( 
		url, 
		data=json.dumps(payload),
		headers={'content-type':'application/json'},
		)

	print(response.status_code)

	if response.status_code == 201:
		print('account created')

	else:
		print('failure')
	
def main():
	cid = '593812c2a73e4942cdafd74f'
	first = 'Gerda'
	last = 'Gottlieb'
	zipcode = '23381'
		
	print checkname(cid, first, last, zipcode)

def checkname(customerId, firstName, lastName, zipcode):
	url = 'http://api.reimaginebanking.com/customers/{}?key={}'.format(customerId, apiKey)


	# Query For Response
	response = requests.get(url)
	
	
	if response.status_code == 404:
		return -1, 'Customer ID does not exist'
	
	rj = response.json()
		
	rfirst = rj['first_name']
	rlast = rj['last_name']
	rzip = rj['address']['zip']
	
	if rfirst.lower().trim() != firstName.lower().trim():
		return -1, 'Customer Information not correct'
	elif rlast.lower().trim() != lastName.lower().trim():
		return -1, 'Customer Information not correct'
	elif str(rzip).lower().trim() != str(zipcode).lower().trim():
		return -1, 'Customer Information not correct'
	
	
	return 0, 'Customer information is correct'
		

if __name__ == '__main__':
	main()
