from joblib import load
from flask import jsonify
import numpy as np
import json

myModel = load('pyDir/predTS.pkl')
polyTransf = load('pyDir/polyTransf.pkl')

def list():
	list = []
	list.append("~~~~~~FUNCTIONS:~~~~~~")
	list.append("/tickets")
	list.append("/totalsale")
	list.append("~~~~~~SPECIFICATION OF INPUT:~~~~~~")
	list.append("/tickets/{price}/{time}/{capacity}/{month}/{day}/{quarter}")
	list.append("/totalsale/{price}/{time}/{capacity}/{month}/{day}/{quarter}")

	return jsonify(list)

def ticketSales(price, time, capacity, month, day, quarter):
	monthNum = {1:0,2:31,3:59,4:90,5:120,6:151,7:181,8:212,9:243,10:273,11:304,12:334}
	dayIndex = (monthNum[month] + day)
	
	inputs = [(price, dayIndex, time, capacity, month, quarter, day)]

	
	prediction = myModel.predict(polyTransf.transform(inputs)) # predicts total sales

	tSales = prediction / price
	if(tSales > capacity):
		prediction = capacity * price
		
	if(prediction <= 0):
		prediction = 0
		tSales = 0
		
	tSales_str = json.dumps(int(tSales))	
	return tSales_str

def totalsales(price, time, capacity, month, day, quarter):
	monthNum = {1:0,2:31,3:59,4:90,5:120,6:151,7:181,8:212,9:243,10:273,11:304,12:334}

	dayIndex = (monthNum[month] + day)
	
	inputs = [(price, dayIndex, time, capacity, month, quarter, day)]
  
  
	prediction = myModel.predict(polyTransf.transform(inputs)) # prediction holds total sales

	tSales = prediction / price
	if(tSales > capacity):
		prediction = capacity*price
		
	if(prediction <= 0):
		prediction = 0
		tSales = 0

	pred_str = json.dumps(int(prediction))

	return pred_str
