# This is written for PYTHON 3
# Don't forget to install requests package

import requests
import json
import datetime

apiKey = '0e5699be695712bf95845e1388604fd4'
	
def main():
	cid = '593812c2a73e4942cdafd74f'
	first = 'Gerda'
	last = 'Gottlieb'
	zipcode = '23881'
	aid = '59382b21ceb8abe24250e1a2'
		
	print checkname(cid, first, last, zipcode)
	print getaccounts(cid)
	print getdeposits(aid)
	print getwithdrawals(aid)


# checks whether customer information is correct
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
		return 0, 'Customer Information not correct'
	elif rlast.lower().strip() != lastName.lower().strip():
		return 0, 'Customer Information not correct'
	elif rzip != zipcode:
		return 0, 'Customer Information not correct'
	
	return 1, 'Customer information is correct'


# get the accounts associated with a specific customer id
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


# get the deposits associated with a specific account id
def getdeposits(accountId):
	url = 'http://api.reimaginebanking.com/accounts/{}/deposits?key={}'.format(accountId, apiKey)

	# Query For Response
	response = requests.get(url)
	
	rj = response.json()

	rdeposits = []
	for deposit in rj:
		dtransactiondate = datetime.strptime(deposit['transaction_date'], '%Y-%m-%d')
		dtuple = (deposit['_id'], dtransactiondate, deposit['status'], deposit['amount'])
		rdeposits.append(dtuple)
	
	return rdeposits


# get the withdrawals associated with a specific account id
def getwithdrawals(accountId):
	url = 'http://api.reimaginebanking.com/accounts/{}/withdrawals?key={}'.format(accountId, apiKey)

	# Query For Response
	response = requests.get(url)
	
	rj = response.json()

	rwithdrawals = []
	for withdrawal in rj:
		wtransactiondate = datetime.strptime(withdrawal['transaction_date'], '%Y-%m-%d')
		wtuple = (withdrawal['_id'], wtransactiondate, withdrawal['status'], withdrawal['amount'])
		rwithdrawals.append(wtuple)
	
	return rwithdrawals


# get the average intake per transaction in a certain amount of time
def getAverageIntakeSingleAccountPastDays(accountId, numDays):

	intake = 0.0
	count = 0.0

	adeposits = getdeposits(accountId)
	sorted(adeposits, key=lambda x: x[1], reverse=True)
	for deposit in adeposits:
		# if date is less than numDays days before current day
		if datetime.datetime.now() - timedelta(days=numDays) <= deposit[1]:
			intake += deposit[3]
			count += 1
		elif:
			break

	return intake / count


# get the average outflow per transaction and day of week
def getAverageOutflowSingleAccountPastDays(accountId, numDays):

	outflow = 0.0
	count = 0.0

	awithdrawals = getwithdrawals(accountId)
	sorted(awithdrawals, key=lambda x: x[1], reverse=True)
	for withdrawal in awithdrawals:
		# if date is less than numDays days before current day
		if datetime.datetime.now() - timedelta(days=numDays) <= withdrawal[1]:
			outflow += withdrawal[3]
			count += 1
		elif:
			break
	
	return outflow / count


# get the average of total income for weeks, hours, days
def getAverageIncomeSingleAccountPastDays(accountId, numDays):

	return getAverageIntakeSingleAccountPastDays(accountId, numDays) - getAverageOutflowSingleAccountPastDays(accountId, numDays)


# get the average intake per transaction for dayRange/2 days before and after middleDay
def getAverageIntakeSingleAccountRange(accountId, middleDay, dayRange):

	intake = 0.0
	count = 0.0

	for deposits in getdeposits(accountId):
		# if date is less than numDays days before current day
		if middleDay - dayRange / 2 <= deposit[1] && middleDay + dayRange / 2 >= deposit[1]:
			intake += deposit[3]
			count += 1
	
	return intake / count


# get the average outflow per transaction for dayRange/2 days before and after middleDay
def getAverageOutflowSingleAccountRange(accountId, middleDay, dayRange):

	outflow = 0.0
	count = 0.0

	for withdrawal in getwithdrawals(accountId):
		# if date is less than numDays days before current day
		if middleDay - dayRange / 2 <= withdrawal[1] && middleDay + dayRange / 2 >= withdrawal[1]:
			outflow += withdrawal[3]
			count += 1
	
	return outflow / count


# get the average intake per transaction for dayRange/2 days before and after middleDay
def getAverageIncomeSingleAccountRange(accountId, middleDay, numDays):

	return getAverageIntakeSingleAccountRange(accountId, middleDay, numDays) - getAverageOutflowSingleAccountRange(accountId, middleDay, numDays)




if __name__ == '__main__':
	main()
