from flask import Flask, render_template, request, flash, send_file
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

class item:

	## self object
	def __init__(
		self,
		cogs,
		WACC,
		aov,
		cagr,
		organicTraffic,
		organicCVR, 
		paidTraffic,
		paidCVR, 
		paidCPC,
		fulfillmentCost,
		refundRate,
		paymentRate,
		partnerCommissionRate,
		partnerOrderPercentage,
		initialOutlay
		):

		## Assign to self object
		self.cogs = cogs
		self.WACC = WACC
		self.aov = aov
		self.cagr = cagr
		self.organicTraffic = organicTraffic
		self.organicCVR = organicCVR
		self.paidTraffic = paidTraffic
		self.paidCVR = paidCVR
		self.paidCPC = paidCPC
		self.fulfillmentCost = fulfillmentCost
		self.refundRate = refundRate
		self.paymentRate = paymentRate
		self.partnerCommissionRate = partnerCommissionRate
		self.partnerOrderPercentage = partnerOrderPercentage
		self.initialOutlay = initialOutlay

	def organicGMV1stYear(self):
		return self.organicTraffic * self.organicCVR * self.aov

	def organicCost1stYear(self):
		return self.organicTraffic * self.organicCVR * (self.cogs + self.fulfillmentCost + self.aov * self.partnerCommissionRate * self.partnerOrderPercentage + self.refundRate * (self.fulfillmentCost + self.cogs) + self.aov * self.paymentRate)

	def paidGMV1stYear(self):
		return self.paidTraffic * self.paidCVR * self.aov

	def paidCost1stYear(self):
		return self.paidTraffic * self.paidCVR * (self.cogs + self.fulfillmentCost + self.aov * self.partnerCommissionRate * self.partnerOrderPercentage + self.refundRate * (self.fulfillmentCost + self.cogs) + self.aov * self.paymentRate) + self.paidCPC * self.paidTraffic

	# def cagrSmartHomeElectronics(self):
	# 	return self.cagr

	# def WACC1(self):
	# 	return self.WACC

	# def initialOutlay1(self):
	# 	return self.initialOutlay

app = Flask(__name__)
app.secret_key = "lousieasy2digital_8888001"

@app.route("/hello")
def index():
	flash("Sponsored by www.easy2digital.com : Please enter the variable factors to evaluate the investment potential (input must be greater or equal to 0)")
	return render_template("index.html")

@app.route("/StoreUrl", methods=["POST", "GET"])
def StoreUrl():
	cogs1 = float(request.form['name_input'])
	WACC3 = float(request.form['WACC'])
	aov1 = float(request.form['aov'])
	cagr1 = float(request.form['cagr'])
	organicTraffic1 = float(request.form['organicTraffic'])
	organicCVR1 = float(request.form['organicCVR'])
	paidTraffic1 = float(request.form['paidTraffic'])
	paidCVR1 = float(request.form['paidCVR'])
	paidCPC1 = float(request.form['paidCPC'])
	fulfillmentCost1 = float(request.form['fulfillmentCost'])
	refundRate1 = float(request.form['refundRate'])
	paymentRate1 = float(request.form['paymentRate'])
	partnerCommissionRate1 = float(request.form['partnerCommissionRate'])
	partnerOrderPercentage1 = float(request.form['partnerOrderPercentage'])
	initialOutlay3 = float(request.form['initialOutlay'])
	YearstoInvest = int(request.form['YearstoInvest'])

	totalProfit = item(cogs1,WACC3,aov1,cagr1,organicTraffic1,organicCVR1,paidTraffic1,paidCVR1,paidCPC1,fulfillmentCost1,refundRate1,paymentRate1,partnerCommissionRate1,partnerOrderPercentage1,initialOutlay3)

	# cagrSmartHomeElectronics2 = totalProfit.cagrSmartHomeElectronics()
	# WACC2 = totalProfit.WACC1()
	# initialOutlay2 = totalProfit.initialOutlay1()

	## Organic Block##

	organicGMV1st = round(totalProfit.organicGMV1stYear(),0)
	organicCost1st = round(totalProfit.organicCost1stYear(),0)
	organicProfit1st = organicGMV1st - organicCost1st

	## Paid Block##

	paidGMV1st = round(totalProfit.paidGMV1stYear(),0)
	paidCost1st = round(totalProfit.paidCost1stYear(),0)
	paidProfit1st = paidGMV1st - paidCost1st

	## Total Profit in 1st year Block##

	totalGrossProfit1st = organicProfit1st + paidProfit1st

	## PV in 1st year block ##

	PV1st = round((totalGrossProfit1st / (int(1) + WACC3)), 0)

	## Sum of PV in the whole investment window block ##

	if YearstoInvest == int(1):
		SumOfPV = round(PV1st,0)

	elif YearstoInvest == int(2):
		SumOfPV = round(PV1st + PV1st * (int(1) + cagr1) ** int(2))

	elif YearstoInvest == int(3):
		SumOfPV = round(PV1st + PV1st * (int(1) + cagr1) ** int(2) + PV1st * (int(1) + cagr1) ** int(3),0)

	elif YearstoInvest == int(4):
		SumOfPV = round(PV1st + PV1st * (int(1) + cagr1) ** int(2) + PV1st * (int(1) + cagr1) ** int(3) + PV1st * (int(1) + cagr1) ** int(3) + PV1st * (int(1) + cagr1) ** int(4), 0)

	elif YearstoInvest == int(5):
		SumOfPV = round(PV1st + PV1st * (int(1) + cagr1) ** int(2) + PV1st * (int(1) + cagr1) ** int(3) + PV1st * (int(1) + cagr1) ** int(3) + PV1st * (int(1) + cagr1) ** int(4) + PV1st * (int(1) + cagr1) ** int(5), 0)

	else:
		flash("Please input 5 or less than 5 years")
		return render_template("result.html", cogs1=cogs1, WACC3=WACC3, aov1=aov1, cagr1=cagr1, organicTraffic1=organicTraffic1, organicCVR1=organicCVR1, paidTraffic1=paidTraffic1, paidCVR1=paidCVR1, paidCPC1=paidCPC1, fulfillmentCost1=fulfillmentCost1, refundRate1=refundRate1, paymentRate1=paymentRate1, partnerCommissionRate1=partnerCommissionRate1, partnerOrderPercentage1=partnerOrderPercentage1, initialOutlay3=initialOutlay3, YearstoInvest=YearstoInvest)

	## NPV block##

	NPV = SumOfPV - initialOutlay3

	if NPV > 0:
		result = f'US$ {NPV} is profitable, you can consider {YearstoInvest} years:)'
		# result = NPV

	elif NPV < 0:
		result = f'US$ {NPV} is losing money, be cautious! Might try extending more years or find alternatives'

	else:
		result = f'US$ {NPV} is Break even, but you can earn company assets and customer data'

	return render_template("result.html", cogs1=cogs1, WACC3=WACC3, aov1=aov1, cagr1=cagr1, organicTraffic1=organicTraffic1, organicCVR1=organicCVR1, paidTraffic1=paidTraffic1, paidCVR1=paidCVR1, paidCPC1=paidCPC1, fulfillmentCost1=fulfillmentCost1, refundRate1=refundRate1, paymentRate1=paymentRate1, partnerCommissionRate1=partnerCommissionRate1, partnerOrderPercentage1=partnerOrderPercentage1, initialOutlay3=initialOutlay3, YearstoInvest=YearstoInvest, result=result)
