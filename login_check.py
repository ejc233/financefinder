# This is written for PYTHON 3
# Don't forget to install requests package

import requests
import json
import datetime
from datetime import datetime, timedelta

apiKey = '0e5699be695712bf95845e1388604fd4'
	
def main():
	cid = '593854d8ceb8abe2425176c3'
	first = 'Sherlock'
	last = 'Holmes'
	zipcode = '11111'
	aidc = '593854d8ceb8abe2425176c4'
	aids = '593854d8ceb8abe2425176c5'
		
	print checkname(cid, first, last, zipcode)
	# print getaccounts(cid)
	# print getdeposits(aidc)
	# print getwithdrawals(aidc)
	print getAverageIntakeSingleAccountPastDays(aidc, datetime(2017, 6, 1, 0, 0), 7)
	print getAverageOutflowSingleAccountPastDays(aidc, datetime(2017, 6, 1, 0, 0), 7)
	print getAverageIncomeSingleAccountPastDays(aidc, datetime(2017, 6, 1, 0, 0), 7)
	print getAverageIntakeSingleAccountPastRange(aidc, datetime(2017, 6, 1, 0, 0), 7, 30)
	print getAverageOutflowSingleAccountPastRange(aidc, datetime(2017, 6, 1, 0, 0), 7, 30)
	print getAverageIncomeSingleAccountPastRange(aidc, datetime(2017, 6, 1, 0, 0), 7, 30)


# checks whether customer information is correct
#
# returns 0 and error message if customer information incorrect
# returns 1 and correct message if customer information correct
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
		return 0, 'Customer Information not correct1'
	elif rlast.lower().strip() != lastName.lower().strip():
		return 0, 'Customer Information not correct2'
	elif rzip != zipcode:
		return 0, 'Customer Information not correct3'
	
	return 1, 'Customer information is correct'


# get the accounts associated with a specific customer id
#
# returns a list of tuples, where each tuple represents an account and contains 
# that account's id, nickname, rewards, type, and balance
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
#
# returns a list of tuples, where each tuple represents a deposit and contains 
# that deposit's id, date made (as a datetime), status, and amount
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
#
# returns a list of tuples, where each tuple represents a withdrawal and contains 
# that withdrawal's id, date made (as a datetime), status, and amount

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
#
# returns the total intake from summing the deposits for an account in a certain
# window range divided by the number of deposits made in that time
def getAverageIntakeSingleAccountPastDays(accountId, startDay, windowSize):

	intake = 0.0
	count = 0.0

	adeposits = getdeposits(accountId)
	sorted(adeposits, key=lambda x: x[1], reverse=True)
	for deposit in adeposits:
		# if date is less than windowSize days before current day
		if startDay - timedelta(days=windowSize) <= deposit[1] and deposit[1] <= startDay:
			intake += deposit[3]
			count += 1

	if intake == 0.0:
		return 0.0

	return intake / count


# get the average outflow per transaction and day of week
#
# returns the total outflow from summing the withdrawals for an account in a
# certain window range divided by the number of withdrawals made in that time
def getAverageOutflowSingleAccountPastDays(accountId, startDay, windowSize):

	outflow = 0.0
	count = 0.0

	awithdrawals = getwithdrawals(accountId)
	sorted(awithdrawals, key=lambda x: x[1], reverse=True)
	for withdrawal in awithdrawals:
		# if date is less than windowSize days before current day
		if startDay - timedelta(days=windowSize) <= withdrawal[1] and withdrawal[1] <= startDay:
			outflow += withdrawal[3]
			count += 1
	
	if outflow == 0.0:
		return 0.0

	return outflow / count


# get the average of total income for weeks, hours, days
#
# returns the average income in a certain window range by taking the average
# intake and subtracting the average outflow
def getAverageIncomeSingleAccountPastDays(accountId, startDay, windowSize):

	return getAverageIntakeSingleAccountPastDays(accountId, startDay, windowSize) - getAverageOutflowSingleAccountPastDays(accountId, startDay, windowSize)


# get the list of numDays-day intake averages starting from startDay and going
# numDays back
#
# windowSize is the number of days the average is taken over
# numDays represents how many days the graph diplays the results
#
# returns a list of (x,y) tuples where x represents a day before or at startDay,
# while y represents the intake average on that day
def getAverageIntakeSingleAccountPastRange(accountId, startDay, windowSize, numDays):

	avgintakes = []
	for i in range(numDays - 1, -1, -1):
		newDay = startDay - timedelta(days=i)
		intaketuple = (newDay, getAverageIntakeSingleAccountPastDays(accountId, newDay, windowSize))
		avgintakes.append(intaketuple)
	
	return avgintakes


# get the list of numDays-day outflow averages starting from startDay and going
# numDays back
#
# windowSize is the number of days the average is taken over
# numDays represents how many days the graph diplays the results
#
# returns a list of (x,y) tuples where x represents a day before or at startDay,
# while y represents the outflowaverage on that day
def getAverageOutflowSingleAccountPastRange(accountId, startDay, windowSize, numDays):

	avgoutflows = []
	for i in range(numDays - 1, -1, -1):
		newDay = startDay - timedelta(days=i)
		outflowtuple = (newDay, getAverageOutflowSingleAccountPastDays(accountId, newDay, windowSize))
		avgoutflows.append(outflowtuple)
	
	return avgoutflows


# get the list of numDays-day income averages starting from startDay and going
# numDays back
#
# windowSize is the number of days the average is taken over
# numDays represents how many days the graph diplays the results
#
# returns a list of (x,y) tuples where x represents a day before or at startDay,
# while y represents the incomeaverage on that day
def getAverageIncomeSingleAccountPastRange(accountId, startDay, windowSize, numDays):

	avgincomes = []
	for i in range(numDays - 1, -1, -1):
		newDay = startDay - timedelta(days=i)
		incometuple = (newDay, getAverageIncomeSingleAccountPastDays(accountId, newDay, windowSize))
		avgincomes.append(incometuple)
	
	return avgincomes


if __name__ == '__main__':
	main()
