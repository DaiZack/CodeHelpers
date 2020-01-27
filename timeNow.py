import pytz, datetime
utc_now = pytz.utc.localize(datetime.datetime.utcnow())
pst_now = utc_now.astimezone(pytz.timezone('Canada/Eastern'))
timenow = str(pst_now)
print(timenow)
