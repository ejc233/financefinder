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
	zipcode = '23881'
	aid = '59382b21ceb8abe24250e1a2'
		
	print checkname(cid, first, last, zipcode)
	print getaccounts(cid)
	print getdeposits(aid)

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
	
	if rfirst.lower().strip() != firstName.lower().strip():
		return -1, 'Customer Information not correct'
	elif rlast.lower().strip() != lastName.lower().strip():
		return -1, 'Customer Information not correct'
	elif rzip != zipcode:
		return -1, 'Customer Information not correct'
	
	
	return 0, 'Customer information is correct'


def getaccounts(customerId):
	url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerId, apiKey)


	# Query For Response
	response = requests.get(url)
	
	rj = response.json()

	raccounts = []
	for account in rj:
		atuple = (account['_id'], account['nickname'], account['rewards'], account['type'], account['balance'])
		raccounts.append(atuple)
	
	return raccounts


def getdeposits(accountId):
	url = 'http://api.reimaginebanking.com/accounts/{}/deposits?key={}'.format(accountId, apiKey)


	# Query For Response
	response = requests.get(url)
	
	rj = response.json()

	rdeposits = []
	for deposit in rj:
		dtuple = (deposit['_id'], deposit['transaction_date'], deposit['status'], deposit['amount'])
		rdeposits.append(dtuple)
	
	return rdeposits

if __name__ == '__main__':
	main()
