from joblib import load
from flask import jsonify
import numpy as np
import json

myModel = load('pyDir/bestMod.pkl')

def list():
	list = []
	list.append("~~~~~~FUNCTIONS:~~~~~~")
	list.append("/tickets")
	list.append("/totalsale")
	list.append("/list")
	list.append("~~~~~~SPECIFICATION OF INPUT:~~~~~~")
	list.append("/tickets/{price}/{time}/{capacity}/{month}/{day}")
	list.append("/totalsale/{price}/{time}/{capacity}/{month}/{day}")

	return jsonify(list)

def ticketSales(price, time, capacity, month, day):
	monthNum = {1:0,2:31,3:59,4:90,5:120,6:151,7:181,8:212,9:243,10:273,11:304,12:334}
	
	if (price < 0) or (time < 0) or (capacity < 0):
		return(['Negative values not within possible range of input'])

	if month not in monthNum: # ensure within range of months
		return(['Month Specified not within 1-12'])

	if day not in range(1,32):
		return(['Day not within in range 1-31'])

	dayIndex = (monthNum[month] + day)
	
	if(month<4):
		quarter = 1
	elif(month<7):
		quarter = 2
	elif(month<10):
		quarter = 3
	else:
		quarter = 4

	inputs = [(price, dayIndex, time, capacity, month, quarter, day)]

	
	prediction = myModel.predict(inputs) # predicts total sales

	tSales = prediction / price
	if(tSales > capacity):
		prediction = capacity * price
		tSales = capacity
		
	if(prediction <= 0):
		prediction = 0
		tSales = 0

	sales = ["Predicted Ticket Sales:"]		
	sales.append(int(tSales))	
	return sales

def totalsales(price, time, capacity, month, day):
	monthNum = {1:0,2:31,3:59,4:90,5:120,6:151,7:181,8:212,9:243,10:273,11:304,12:334}

	if (price < 0) or (time < 0) or (capacity < 0):
		return(['Negative values not within possible range of input'])

	if month not in monthNum: # ensure within range of months
		return(['Month Specified not within 1-12'])

	if day not in range(1,32): # ensure day 1-31, doesnt yet account for change in # of day
		return(['Day not within in range 1-31'])

	dayIndex = (monthNum[month] + day)
	
	if(month<4):
		quarter = 1
	elif(month<7):
		quarter = 2
	elif(month<10):
		quarter = 3
	else:
		quarter = 4

	inputs = [(price, dayIndex, time, capacity, month, quarter, day)]
  
  
	prediction = myModel.predict(inputs) # prediction holds total sales

	tSales = prediction / price
	if(tSales > capacity):
		prediction = capacity*price
		tSales = capacity
		
	if(prediction <= 0):
		prediction = 0
		tSales = 0

	sales = ["Predicted Total Sales:"]
	sales.append(int(prediction))	
	return sales
