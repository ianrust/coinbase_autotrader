import csv
import matplotlib.pyplot as plt
import datetime

bit_history=[]

with open('bitHistory.csv','r') as bit_history_file:
	hist_reader=csv.reader(bit_history_file,delimiter=',')
	for line in hist_reader:
		bit_history.append({'unix_time':int(line[0]),'price':float(line[1]),'amount':float(line[2])})

day=86400/2


gains_vect=[]
ps_vect=[]
raw_money=[]

bit_history=[element for element in reversed(bit_history)]


for i in xrange(1,60):
	last_price=bit_history[0]['price']
	last_high_price=last_price
	last_trans_time=bit_history[0]['unix_time']-day
	coin_trade=50.0
	transaction_cost=0.01
	money=10000.0-coin_trade*last_price*(1.0+transaction_cost)-0.15
	percent_swing=0.01*float(i)
	print percent_swing
	have_coins=True
	start_time=last_trans_time
	old_time=last_trans_time
	print last_price
	for hist_bit in (bit_history[int(0.66666*len(bit_history)):]):
		# print hist_bit['price']-last_price
		# print hist_bit['unix_time']-old_time
		old_time=hist_bit['unix_time']
		# if hist_bit['price']>last_high_price and have_coins:
		# 	last_high_price=hist_bit['price']
		# if hist_bit['price']<last_price and not have_coins:
		# 	last_price=hist_bit['price']
		if hist_bit['unix_time']-day>last_trans_time:
			if hist_bit['price']>=(1.0+percent_swing)*last_price and have_coins:
				print "Sell - Cur: " + str(hist_bit['price']) + " Last: " +str(last_price)
				money=money+hist_bit['price']*coin_trade*(1.0-transaction_cost)-0.15
				last_price=hist_bit['price']
				last_trans_time=hist_bit['unix_time']
				have_coins=False
			elif hist_bit['price']<=(1.0-percent_swing)*last_price and (not have_coins):
			# elif not have_coins:
				print "Buy - Cur: " + str(hist_bit['price']) + " Last: " +str(last_price)
				# buy coins
				money=money-hist_bit['price']*coin_trade*(1.0+transaction_cost)-0.15
				last_price=hist_bit['price']
				last_trans_time=hist_bit['unix_time']
				have_coins=True
	print have_coins
	print bit_history[-1]['price']
	print len(bit_history)
	# if have_coins:
	# 	print money
	# 	money=money+bit_history[-1]['price']*coin_trade*(1-transaction_cost)
	# 	print money

	gains=(money/10000.0-1.0)*100.0*day/(bit_history[-1]['unix_time']-bit_history[0]['unix_time'])
	print str(gains) +"@"+str(int(percent_swing*100))+"%"
	gains_vect.append(gains)
	ps_vect.append(percent_swing)
	raw_money.append(money)

# plt.figure(2)
# plt.plot(ps_vect,gains_vect)
plt.figure(3)
plt.plot(ps_vect,raw_money)

# price=[element['price'] for element in bit_history]
# time_days=[float(element['unix_time'])/float(day) for element in bit_history]
# plt.figure(1)
# plt.plot(time_days,price)
plt.show()

