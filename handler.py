from __future__ import print_function
import logging
import boto3
import subprocess

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def run_benchmark(event, context):
    print("Running Benchmark.")
    start = context.get_remaining_time_in_millis()
    response = {"test": "v0.2 - loading from dynamodb session", "event": event}
    
    response["ddb_response"] = load_code_from_ddb(event["tableName"], event["payloadName"], context)
    # response["s3_client_times"] = load_code_from_s3_client(event["bucketName"], event["payloadName"])
    # response["s3_resource_times"] = load_code_from_s3_resource(event["bucketName"], event["payloadName"], context)

    return response

### DOWNLOADS ###
def load_code_from_s3_client(bucketName, payloadName):
    print("Retrieving " + str(payloadName) + " from bucket: " + str(bucketName))
    s3_client = boto3.client('s3')
    s3_client.download_file(bucketName, payloadName, payloadName)
    print(open(payloadName).read())

def load_code_from_s3_resource(bucketName, payloadName, context):
    print("Retrieving payload.")
    result = {}
    
    result["timeToConnect"] = context.get_remaining_time_in_millis()
    # -> lambda cannot contain assignment!
    # result["timeToConnect"] = timed_exec(lambda x: s3 = boto3.resource('s3'), "nothing")
    s3 = boto3.resource('s3')
    result["timeToConnect"] -= context.get_remaining_time_in_millis()
    
    result["timeToLoadBucket"] = context.get_remaining_time_in_millis()
    bucket = s3.Bucket(bucketName)
    result["timeToLoadBucket"] -= context.get_remaining_time_in_millis()

    result["timeToLoadObject"] = context.get_remaining_time_in_millis()
    # bucket.download_file(payloadName, str("/tmp/" + payloadName))
    # with open('/tmp/payload.txt', 'wb') as data:
        # bucket.download_fileobj(payloadName, data)
    bucket.download_file(payloadName, "/tmp/payload.py")
    with open('/tmp/payload.py', 'r') as file:
        print(file.read())
    # print(data)
    result["timeToLoadObject"] -= context.get_remaining_time_in_millis()

    result["timeToExecute"] = context.get_remaining_time_in_millis()
    invoke_payload("/tmp/payload.py")
    result["timeToExecute"] -= context.get_remaining_time_in_millis()

    return result

def load_code_from_ddb(tableName, payloadName, context):
    print("Retrieving payload from dynamoDB")
    result = {}
    result["timeToConnectToTable"] = context.get_remaining_time_in_millis()
    dynamodb = boto3.resource('dynamodb').Table(tableName)
    result["timeToConnectToTable"] -= context.get_remaining_time_in_millis()
    
    result["timeToScanTable"] = context.get_remaining_time_in_millis()
    dbResponse = dynamodb.scan()
    result["timeToScanTable"] -= context.get_remaining_time_in_millis()

    result["timeToGetDBItem"] = context.get_remaining_time_in_millis()
    dbResponse = dynamodb.get_item(Key={'name':'payload1'})
    result["timeToGetDBItem"] -= context.get_remaining_time_in_millis()

    result["ddbResponse"] = dbResponse['Item']
    return result

def timed_exec(function, *args):
    remaining = context.get_remaining_time_in_millis()
    function(*args)
    return difference - context.get_remaining_time_in_millis()

### INVOKE ###
def invoke_payload(payload):
    print("Invoking payload...")
    subprocess.call(['python',payload])

### UPLOADs ###
def deploy_payload_to_s3_client(bucketName, payloadName, payload):
    print("Deploying payload to " + str(bucketName))
    # s3_client.upload_file(payloadName, bucketName)

def deploy_payload_to_s3_resource(s3, bucketName):
    print("Deploying payload to " + str(bucketName))
    # s3_client.upload_file(payloadName, bucketName)
