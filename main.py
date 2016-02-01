import serial, os, boto, uuid
import time
import thread
from datetime import datetime
from datetime import timedelta
from time import gmtime, strftime, sleep
from boto.s3.key import Key 

# Store AWS_ACCESS_KEY_ID & AWS_SECRET_ACCESS_KEY in ~/.aws/credentials

# Check for standard osx and raspi serial port names
def get_serial_port():
	ser_devs = [dev for dev in os.listdir('/dev') if dev.startswith('ttyACM') or dev.startswith('tty.usbmodem')]
	if len(ser_devs) > 0:
		return '/dev/' + ser_devs[0]
	return None

# Connect to teensy
def connect_to_serial_port():
	ser = serial.Serial(get_serial_port(),9600)
	if ser.name:
		print 'connected to ' + ser.name
		return ser
	else:
		print 'not connected to teensy'

# Read line from serial port and format
def read_format_data(ser):
	data = ser.readline()
	data = data.replace("\t",",")
	data = strftime("%Y:%m:%d %H:%M:%S") + ',' + data
	return data

# Write data to day file
def write_to_file(data):
	filename = strftime("%Y-%m-%d") + ".csv"
	with open(filename, 'a') as f:
		f.write(data)

# Connect to AWS
def connect_to_aws():
	print "connecting to aws"
	s3 = boto.connect_s3()
	return s3

# Check if bucket exists, if not then create
def check_bucket(s3, bucket_name):
	print 'looking up bucket:', bucket_name# per hive you only get 100
	if s3.lookup(bucket_name):
		print bucket_name + " already exists"
		bucket = s3.lookup(bucket_name)
	return bucket

# Needs to be done in thread
def write_file_to_s3(filename):
	print 'uploading to S3'
	filename = filename + ".csv"
	s3 = connect_to_aws()
	bucket = check_bucket(s3, bucket_name)
	k = Key(bucket)
	k.key = '/data/count/' + filename

	# get all the data from file
	try:
		with open(filename, 'r') as f:
			all_data_from_file = f.read()
			print 'write', filename, 'to s3'
			k.set_contents_from_string(all_data_from_file)
	except IOError as e:
		print e

def get_minute():
	return strftime('%M')

def get_date():
	return strftime("%Y-%m-%d")

# Initialization vars
bucket_name = 'wenis'
connect_retry_time = 5
last_minute = get_minute()
last_date = get_date() 
filename = None
ser = None


while True:

	# Read data from Teensy
	if ser:
		try:
			data = read_format_data(ser)
			write_to_file(data)
			print data
		except Exception, e:
			print "Failed to read in the usual spot: ", e
	else:
		ser = connect_to_serial_port()
		time.sleep(1)
 
	# Execute daily tasks
	date_now = get_date()
	if date_now != last_date:
		print 'day:',date_now
		print 'write to AWS in thread'
		thread.start_new_thread(write_file_to_s3,(last_date,))
		last_date = date_now

	# Execute minutely tasks
	minute_now = get_minute()
	if minute_now != last_minute:
		print 'minute:',minute_now
		print 'write to mysql in thread'

		last_minute = minute_now

	

	# time.sleep(10)








		
	

	






