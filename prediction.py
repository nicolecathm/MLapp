from joblib import load
import numpy as np
import json

myModel = load('predTS.pkl')
polyTransf = load('polyTransf.pkl')

def ticketSales(price, time, capacity, month, day, quarter):
	monthNum = {1: 0, 2: 31, 3: 59, 4: 90, 5: 120, 6: 151, 7: 181, 8: 212, 9:243, 10: 273, 11: 304, 12: 334 }
 	dayIndex = (monthNum[month] + day)
	
	jinputs = [(price, dayIndex, time, capacity, month, quarter, day)]
	inputs = np.array(jinputs);
  
  
 	prediction = myModel.predict(polyTransf.transform(inputs)) // predicts total sales

 	tSales = prediction / ticket_price
	if(tSales > capacity):
 		prediction = capacity*ticket_price

	if(prediction <= 0):
		prediction = 0
		tSales = 0

	tSales_str = json.dumps(tSales);

	return tSales_str

def totalsales(price, time, capacity, month, day, quarter):
	monthNum = {1: 0, 2: 31, 3: 59, 4: 90, 5: 120, 6: 151, 7: 181, 8: 212, 9:243, 10: 273, 11: 304,12: 334 }

 	dayIndex = (monthNum[month] + day)

	jinputs = [(price, dayIndex, time, capacity, month, quarter, day)]
	inputs = np.array(jinputs);
  
  
 	prediction = myModel.predict(polyTransf.transform(inputs)) // prediction holds total sales

 	tSales = prediction / ticket_price
	if(tSales > capacity):
 		prediction = capacity*ticket_price

	if(prediction <= 0):
		prediction = 0
		tSales = 0

	pred_str = json.dumps(prediction);

	return pred_str
