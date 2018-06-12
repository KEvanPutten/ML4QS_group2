import sys
import csv
import datetime

START = datetime.datetime.strptime('06 06 2018 - 16:10', '%d %m %Y - %H:%M')

EPOCH = datetime.datetime.utcfromtimestamp(0)
def unix_time_millis(dt):
        return (dt - EPOCH).total_seconds() * 1000.0

def readfile(name, date):
    ret = ''
    with open(name, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        reader.next() # skip header
        
        for row in reader:
            # get values
            time_passed = float(row[0])
            x = float(row[1])
            y = float(row[2])
            z = float(row[3])

            # convert datetime
            # crowdsignals: Time points are expressed in
            #               nanoseconds since the start of time
            #               (which is January 1st 1970 following the UNIX convention).
            # so an epoch with 19 characters...

            last = dt = date + datetime.timedelta(seconds=time_passed)
            milis = unix_time_millis(dt)
            nanos = int(milis*1000000)

            ret += '\nmagnetometer,smartphone,{},{},{},{}'.format(nanos,x,y,z)
    return [ret, last]

files = ['sitting/Magnetometer.csv', 'walking/Magnetometer.csv',
         'running/Magnetometer.csv', 'running/Magnetometer.csv']

output = open("magnetometer.csv", 'w');
output.write('sensor_type,device_type,timestamps,x,y,z')
date = START
for f in files:
    out = readfile(f, date)
    output.write(out[0])
    date = out[1]
print('bye')
output.close()
