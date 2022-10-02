# First Lambda Function (SerializeImageData)

import json
import boto3
import base64

s3 = boto3.client('s3')


def lambda_handler(event, context):
    """A function to serialize target data from S3"""

    # Get the s3 address from the Step Function event input
    key = event['s3_key']  ## TODO: fill in
    bucket = event['s3_bucket']

    # Download the data from s3 to /tmp/image.png
    ## TODO: fill in
    s3.download_file(bucket, key, "/tmp/image.png")
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }

####################################################################################################

# Second Lambda Function (Classification)

import json
import base64
import boto3

# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-2022-10-02-14-36-17-143"  ## TODO: fill in
runtime = boto3.Session().client('sagemaker-runtime')


def lambda_handler(event, context):
    # Decode the image data
    image = base64.b64decode(event['image_data'])  ## TODO: fill in

    # Instantiate a Predictor
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT, ContentType='image/png', Body=image)

    event["inferences"] = json.loads(response['Body'].read().decode())  ## TODO: fill in
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }

##############################################################################################################

# Third Lambda Function (Filter_Low_Confidence_Inferences)

import json

THRESHOLD = .91


def lambda_handler(event, context):
    # Grab the inferences from the event
    inferences = event['inferences']

    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = any([True for i in inferences if i > THRESHOLD])  ## TODO: fill in

    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise ("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
