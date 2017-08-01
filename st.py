#!/usr/bin/env python3
''' A simple script to upload a random file to Amazon S3 and also display upload speeds
    Requires requests, and boto3 to be functional
'''
import os
import sys
import time
import csv
from pprint import pprint

from random import random
try:
    import boto3
except:
    print("Exception: Please install boto3 module from pip")
try:
    import requests
except:
    print("Exception: Please install requests module from pip")

def make_human(num, suffix='B'):
    ''' This function takes a number and returns a string with the corresponding suffix '''
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

#create temporary randomised file to prevent any compression from affecting the result
RANDOMFILE = '/tmp/tmpfile{}'.format(int(random()*1000))
os.system('dd if=/dev/urandom bs=100K count=1 iflag=fullblock of=' + RANDOMFILE + ' &> /dev/null')

S3RES = boto3.resource('s3')

# If nothing is passed in the cli
LOCATIONS = []
if len(sys.argv) == 1:
    try:
        LOCFILE = open('locations.txt', 'r')
    except:
        sys.exit('locations file missing')

    #Since us east does not require any location constraint attribute, deal with it separately
    with open('locations.txt', 'r') as f:
        for line in f:
            if line.find('#') == -1:
                LOCATIONS = LOCATIONS + [line.strip('\n'),]
else:

    if sys.argv[1] == "--locations":
        for i in sys.argv[2:]:
            LOCATIONS.append(i)

BUCKETS = []
FILES = []

USPEEDS = []
UTIMES = []
LATENCIES = []
SIZES = []

DSPEEDS = []
DTIMES = []

print("Running download and upload tests...\n")
for location in LOCATIONS:
    #Deal with us-east-1
    if location == 'us-east-1':
        NEWBUCKNAME = 'reisubtest-' + str(int(random()*1000))
        BUCKETS.append(NEWBUCKNAME)
        S3RES.create_bucket(
            Bucket=NEWBUCKNAME,
            # CreateBucketConfiguration={'LocationConstraint': location})
            )

        start = time.time()
        S3RES.Bucket(NEWBUCKNAME).put_object(Key='Test1', Body=open(RANDOMFILE, 'rb'))
        end = time.time()
        USPEED = os.stat(RANDOMFILE).st_size / (end - start)
        USPEEDS.append(USPEED)
        with open("reports/ul-"+location, 'a') as ufile:
            ufile.write(str(USPEED))
            ufile.write('\n')

        start = time.time()
        S3RES.Bucket(NEWBUCKNAME).download_file('Test1', '/tmp/file')
        end = time.time()
        DSPEED = os.stat(RANDOMFILE).st_size / (end - start)
        DSPEEDS.append(DSPEED)
        with open("reports/dl-"+location, 'a') as dfile:
            dfile.write(str(DSPEED))
            dfile.write('\n')

        SIZES.append(os.stat(RANDOMFILE).st_size)
    #Deal with the others
    else:
        newBuckName = 'reisubtest-' + str(int(random()*1000))
        BUCKETS.append(newBuckName)
        S3RES.create_bucket(
            Bucket=newBuckName,
            CreateBucketConfiguration={'LocationConstraint': location}
            )

        start = time.time()
        S3RES.Bucket(newBuckName).put_object(Key='Test1', Body=open(RANDOMFILE, 'rb'))
        end = time.time()
        USPEED = os.stat(RANDOMFILE).st_size / (end - start)
        USPEEDS.append(os.stat(RANDOMFILE).st_size / (end - start))
        with open("reports/ul-"+location, 'a') as ufile:
            ufile.write(str(USPEED))
            ufile.write('\n')

        start = time.time()
        S3RES.Bucket(newBuckName).download_file('Test1', '/tmp/file')
        end = time.time()
        DSPEED = os.stat(RANDOMFILE).st_size / (end - start)
        DSPEEDS.append(os.stat(RANDOMFILE).st_size / (end - start))
        with open("reports/dl-"+location, 'a') as dfile:
            dfile.write(str(DSPEED))
            dfile.write('\n')

        SIZES.append(os.stat(RANDOMFILE).st_size)

i = 0

for i in range(len(DTIMES)):
    DSPEEDS.append(make_human(SIZES[i] / DTIMES[i]) + '/s')
pprint(DSPEEDS)
for i in range(len(UTIMES)):
    USPEEDS.append(make_human(SIZES[i] / UTIMES[i]) + '/s')
pprint(USPEEDS)

for bucket in S3RES.buckets.all():
    if bucket.name.find('reisubtest') != -1:
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()

# Find the latencies by sending a HTTP request on port 80, ICMP ping command does not necessarily work on all regions.
# This does mean that the latency will be a bit larger than the expected value with ping command but
# however, the relative latencies of different S3 regions will be as expected
# RESPONSE = requests.get("http://s3.amazonaws.com")
# LATENCIES.append('{0:.2f}'.format((RESPONSE.elapsed.total_seconds() * 1000)) + 'ms')

print("Running latency tests...\n")
for location in LOCATIONS:
    curloc = location
    if location == 'us-east-1':
        curloc = ''
    response = requests.get("http://s3." + location + ".amazonaws.com")
    lat = response.elapsed.total_seconds() * 1000
    with open("reports/lat-" + location, 'a') as latfile:
        latfile.write(str(lat))
        latfile.write('\n')
    LATENCIES.append('{0:.2f}'.format(lat) + 'ms')
pprint(LATENCIES)

os.system('rm -rf ' + RANDOMFILE)
os.system('rm -rf ' + '/tmp/file')
