import serial, os, boto, uuid
import time
from time import gmtime, strftime, sleep
from boto.s3.key import Key 



connect_retry_time = 5
oldfile = ""



# store AWS_ACCESS_KEY_ID & AWS_SECRET_ACCESS_KEY in ~/.aws/credentials
print "connecting to aws"
startTime = time.time()
s3 = boto.connect_s3()
print startTime
#sleep(connect_retry_time)


# check if bucket exists, if not then create
bucket_name = "wenis" # per hive you only get 100
if s3.lookup(bucket_name):
	print bucket_name + " already exists"
	bucket = s3.lookup(bucket_name)
else:
	endTime = time.time()
	if endTime - startTime > 30:
		print 'it was bigger'
		os._exit()
	# fix - this could fail if someone else owns bucket
	print "creating new bucket with name: " + bucket_name
	bucket = s3.create_bucket(bucket_name)

k = Key(bucket)


# checks for standard osx and raspi serial port names
def get_serial_port():
	ser_devs = [dev for dev in os.listdir('/dev') if dev.startswith('ttyACM') or dev.startswith('tty.usbmodem')]
	if len(ser_devs) > 0:
		return '/dev/' + ser_devs[0]
	return None



# collect data via serial
def collect_upload(ser):
	global oldfile
	global k
	cleanup = 0
	num_writes = 0
	num_write_upload_threshold = 50
	while(1):

		# update filename, won't change if same day as last write
		# fix - write to usb directory
		newfile = strftime("%Y-%m-%d") + ".csv" # add a minute to test
		if newfile != oldfile:
			print 'creating new file: ' + newfile
			deletefile = oldfile
			cleanup = 1
			oldfile = newfile


		data = ser.readline()
		#print data
		data = data.replace("\t",",")
		data = strftime("%H-%M-%S") + ',' + data
		print data

		# write to file with day, files will auto create daily w log
		with open(newfile, 'a') as f:
			f.write(data)

		# write to S3.  there are no object limits or really upload rate limits.
		# sucks to have a ton of objects though, maybe upload data every minute?
		if num_writes == num_write_upload_threshold:
			# write to aws
			print 'uploading to aws'
			k.key = '/data/count/' + newfile

			# get all the data from file
			with open(newfile, 'r') as f:
				all_data_from_file = f.read()
			k.set_contents_from_string(all_data_from_file)
			all_data_from_file = ""

			num_writes = 0

			if cleanup == 1 and deletefile != "":
				# try to delete old file to save space only after uploading to S3
				# fix - add a check that upload was successful
				print 'deleting old file:' + deletefile
				os.remove(deletefile)
				cleanup = 0
				

		num_writes += 1

while(1):
	# try to connect to usb
	ser = serial.Serial(get_serial_port(),9600)
	if ser.name != None:
		print 'connected to ' + ser.name
		try:
			collect_upload(ser)
		except Exception, e:
			print e
			pass
		
	else:
		print 'failed to connect.  waiting ' + str(connect_retry_time) + ' seconds.'
		# upload zeros/msg/log to aws?
		sleep(connect_retry_time)

	






