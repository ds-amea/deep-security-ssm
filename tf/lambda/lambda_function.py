import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info("logging setup complete")


def lambda_handler(event, context):
    logger.info('initializing for instanceid: ' + event['detail']['instance-id'])
    #get InstanceID from the EC2 that generated the log in CloudWatch
    instanceid = event['detail']['instance-id']
    flagger = 0
    #Wait EC2 to be with status Running
    ec2_resource = boto3.resource('ec2')
    instance = ec2_resource.Instance(instanceid)
    instance.wait_until_running()

    #Wait Instance to be with Status check to be ready (2/2)
    ec2_client = boto3.client('ec2')
    #waiter = ec2_client.get_waiter('instance_status_ok')
    #waiter.wait(InstanceIds=[instanceid])

    logger.info("instance " + instanceid + " is running with status ready 2/2")

    #get the Instance Profile (ARN) from the EC2 if it has already
    arn_instance_profile = instance.iam_instance_profile

    #Check if the EC2 has the Tag DSADeploy if not add Tag Install DSA with Value 'Yes'
    if instance.tags == None:
        logger.info("instance " + instanceid + " has no tags; adding")
        #Call the function addTag
        addTag(ec2_client, instanceid)
    else:
        #Check if there are any Tag associated with the Ec2 with the name InstallDSA and with the Value set up as "No" or "no", if yes stop the script
        for tags in instance.tags:
            if tags['Key'] == "DSADeploy":
                flagger = 1 
                if (tags["Value"] == 'No') or (tags["Value"] == 'no') or (tags["Value"] == 'NO'):
                    #If the tag Install DSA is no exit the lambda Function
                    logger.info("instance " + instanceid + " has tag InstallDSA == no; aborting")
                    return 0
                elif (tags["Value"] != 'yes') or (tags["Value"] != 'Yes') or (tags["Value"] != 'YES'):
                    addTag(ec2_client, instanceid)
                    break

        if flagger == 0:
            addTag(ec2_client, instanceid)
            
    return 0

def addTag(ec2_client, instanceid):
    #Use function from boto3 to add Tag to the EC2
    logger.info("instance " + instanceid + " is getting the InstallDSA tag")
    response = ec2_client.create_tags(
                Resources=[
                    instanceid,
                ],
                Tags=[
                    {
                        'Key': 'DSADeploy',
                        'Value': 'yes'
                    },
                ]
            )
