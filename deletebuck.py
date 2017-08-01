#!/usr/bin/env python3
''' A simple script to upload a random file to Amazon S3 and also display upload speeds'''
import os
import timeit
import time
import pprint

from random import random
import boto3

global S3RES
S3RES = boto3.resource('s3')

for bucket in S3RES.buckets.all():
    if bucket.name.find('reisubtest') != -1:
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()
