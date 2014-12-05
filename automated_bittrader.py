import json,urllib2,csv,time,smtplib,string,os

os.chdir('/home/ian/Documents')

# Buy and sell urls
sell_url = "https://coinbase.com/api/v1/sells"
buy_url = "https://coinbase.com/api/v1/buys"
sell_price_url = "https://coinbase.com/api/v1/prices/sell"
buy_price_url = "https://coinbase.com/api/v1/prices/buy"
headers = {'content-type': 'application/json'}
price_payload={'qty':1.0}

# gmail login info
gmailUser='iancharlesrust@gmail.com'
gmailPassword='' #password omitting *facepalm*

#function for interacting with coinbase
def req_and_ret(url,req_input,header,url_type='GET'):
	if url_type=='POST':
		url = urllib2.Request(url, json.dumps(req_input), header)
	f = urllib2.urlopen(url)
	json_response = f.read()
	list_response = json.loads(json_response)
	f.close()
	return list_response,json_response
	

#Reading in current state
with open('trader_state.csv','r') as trader_state:
	trader_state_csv=csv.reader(trader_state,delimiter=',')
	for line in trader_state_csv:
		if line[0]=='api_key':
			vars()[line[0]]=line[1]
		else:
			vars()[line[0]]=float(line[1])
	trader_state.close()

#Get Current Bitcoin Prices for buy/sell

buy_price_response,throwaway = req_and_ret(buy_price_url,price_payload,headers)
buy_price=buy_price_response['subtotal']['amount']
sell_price_response,throwaway = req_and_ret(sell_price_url,price_payload,headers)
sell_price=sell_price_response['subtotal']['amount']

# Assembling Message

transaction_payload = {'api_key':api_key,'qty':amount_to_trade}

# Decide to make transaction
transaction_type=''
make_transaction=False
current_unix_time=time.time()

if current_unix_time-time_between_transactions>last_transaction_time:
#decide on type of transaction
	if coins==amount_to_trade and sell_price>=(1.0+percent_swing)*last_price:
		transaction_type='sell'
		make_transaction=True
	elif coins==0 and buy_price<=(1.0-percent_swing)*last_price:
		transaction_type='buy'
		make_transaction=True

#transact

success=False
transaction_response={'success':'False'}
trans_resp_string=''

last_price_new=last_price
coins_new=coins

if make_transaction:
	if transaction_type=='sell':
		transaction_response,trans_resp_string=req_and_ret(sell_url,transaction_payload,headers,'POST')
		coins_new=0
		last_price_new=sell_price
	else:
		transaction_response,trans_resp_string=req_and_ret(buy_url,transaction_payload,headers,'POST')
		coins_new=amount_to_trade
		last_price_new=buy_price

success=transaction_response['success']
errors=''
if not success:
	errors=transaction_response['errors']

# if there are problems, send an email to Ian Rust. Likewise, if there is a succesful transaction, tell Ian Rust
subject=""
to_addr="iancharlesrust@gmail.com"
from_addr="autobittrader@rpi.com"
text=''
mailServer = smtplib.SMTP('smtp.gmail.com', 587)
mailServer.ehlo()
mailServer.starttls()
mailServer.ehlo()
mailServer.login(gmailUser, gmailPassword)

if make_transaction:
	if not success:
		subject="Got Problems With Your Bitcoin Trader"
		text="Hello Sir \n\n I just had trouble making an api based "+transaction_type+" bitcoin transaction on coinbase. Coinbase gave the following error: \r\n "+str(errors)+"\r\n You have 1 day from the time these email was sent to fix the problem. \n\n Yours Truly, \n\n RPI BitTrader \r\n PS This is the whole response: \r\n" +str(trans_resp_string)
	else:
		subject="Successful "+transaction_type+" On the Part of Your Bitcoin Trader"
		text="Hello Sir \n\n I just made a "+transaction_type+" order successfully on coinbase. \r\n The price was "+str(last_price)+" for "+str(amount_to_trade)+"BTC \n\n Yours Truly, \n\n RPI BitTrader"

	body=string.join(("From: %s" % from_addr,"To: %s" % to_addr,"Subject: %s" % subject ,"",text), "\r\n")
	mailServer.sendmail(from_addr, [to_addr], body)

mailServer.close()


# record the state
with open('trader_state.csv','w') as trader_state:
	last_transaction_time_towrite=last_transaction_time
	last_price_towrite=last_price
	coins_towrite=coins
	if make_transaction and success:
		last_transaction_time_towrite=current_unix_time
		last_price_towrite=last_price_new
		coins_towrite=coins_new
	trader_state.write('last_price,'+str(last_price_towrite)+'\nlast_transaction_time,'+str(int(last_transaction_time_towrite))+'\ncoins,'+str(coins_towrite)+'\namount_to_trade,'+str(amount_to_trade)+'\npercent_swing,'+str(percent_swing)+'\ntime_between_transactions,'+str(time_between_transactions)+'\napi_key,'+str(api_key)+'\nlast_check_time,'+str(int(current_unix_time)))
