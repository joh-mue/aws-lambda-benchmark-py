import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def runBenchmark(event, context):
    start = context.get_remaining_time_in_millis()
    response = { "test": "v0.0.1" , "event": event }

    return response

def createPayload():
    logger.info("Creating Payload.")

def deployPayload():
    logger.info("Deploying Payload.")

def deployPayloadToS3():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucketName)
    for 

def retrievePayload():
    logger.info("Retrieving Payload.")

def invokingPayload():
    logger.info("Retrieving Payload.")
