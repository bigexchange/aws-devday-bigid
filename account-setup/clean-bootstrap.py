#!/usr/bin/env python

import boto3

bucket_name = ""
cft  = boto3.client('cloudformation')
s3  = boto3.resource('s3')

res = cft.describe_stacks(StackName = "CDKToolkit")
for output in res['Stacks'][0]['Outputs']:
    if output['OutputKey'] == "BucketName":
        bucket_name = output['OutputValue']
        break

bucket = s3.Bucket(bucket_name)
bucket.object_versions.delete()
bucket.delete()
cft.delete_stack(StackName="CDKToolkit")