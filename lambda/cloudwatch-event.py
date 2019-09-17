import boto3
import logging
import time
import os
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info("logging setup complete")
#Assumptions
#1. all instances have SSM Role

def lambda_handler(event, context):
    ssm = boto3.client('ssm')
    logger.info('initializing for instanceid: ' + event['detail']['instance-id'])
    #get InstanceID from the EC2 that generated the log in CloudWatch
    instanceid = event['detail']['instance-id']
    flagger = 0

    logger.info("Waiting for instance to Run")
    ec2_resource = boto3.resource('ec2')
    instance = ec2_resource.Instance(instanceid)
    instance.wait_until_running()

    ec2_client = boto3.client('ec2')

    logger.info("instance " + instanceid + " is running with status ready 2/2")
    time.sleep(30) 
    logger.info("instance " + instanceid + " has passed the timer")
   # arn_instance_profile = instance.iam_instance_profile
    InstanceId=str(event['detail']['instance-id'])
    Targets="Key=InstanceIds,Values="+InstanceId
    DocumentName=os.environ['DocumentName']
    response = ssm.send_command(
        #InstanceIds=[InstanceId],
        Targets=[
        {
            'Key': 'InstanceIds',
            'Values': [
                InstanceId
            ]
        },
    ],
        DocumentName=DocumentName,
        Comment='Installing Deep Security'
    )
