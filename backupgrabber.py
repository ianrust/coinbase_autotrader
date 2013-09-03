import urllib2 as ul
import time,datetime

start_day="11/7/2012"
unix_time_start=time.mktime(datetime.datetime.strptime(start_day, "%d/%m/%Y").timetuple())
stop_day="11/7/2013"
unix_time_stop=time.mktime(datetime.datetime.strptime(stop_day, "%d/%m/%Y").timetuple())
unix_end=unix_time_stop

url="http://bitcoincharts.com/t/trades.csv?symbol=mtgoxUSD&start="+str(int(unix_time_start))+"&end="+str(int(unix_time_stop))

print url
bithistlog=open('bitHistory.csv','w')
bitHistoryUrl=ul.urlopen(url)
bitHistory=bitHistoryUrl.read()
bithistlog.write(bitHistory)
bithistlog.close()
lines=bitHistory.split('\n')
unix_time_stop=int(lines[-1].split(',')[0])

def get_data(timeget):

	url="http://bitcoincharts.com/t/trades.csv?symbol=mtgoxUSD&start="+str(int(unix_time_start))+"&end="+str(int(timeget))
	try:
		bitHistoryUrl=ul.urlopen(url)
		bitHistory=bitHistoryUrl.read()
		return bitHistory
	except:
		get_data(timeget)
	

while unix_time_stop>unix_time_start+86400*2:
	print (unix_time_stop-unix_time_start)/(unix_end-unix_time_start)
	get_data(unix_time_stop)

	bithistlog=open('bitHistory.csv','a')
	bithistlog.seek(0)
	bitHistory=get_data(unix_time_stop)
	print bitHistory
	bithistlog.write(bitHistory)
	bithistlog.close()
	# time.sleep(5)

	lines=bitHistory.split('\n')
	unix_time_stop=int(lines[-1].split(',')[0])

print "Done Getting Bitcoin Price History"