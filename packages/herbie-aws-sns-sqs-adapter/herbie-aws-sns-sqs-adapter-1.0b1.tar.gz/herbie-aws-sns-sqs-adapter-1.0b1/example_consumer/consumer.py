import json
import sys
import boto3
import os

if len(sys.argv) < 2:
    print('Please provide a Queue Name to consume from to e.g: "python consumer.py customer_queue"')
    exit()

queue_name = sys.argv[1]

# Create SQS client
sqs_client = boto3.client(
    "sqs",
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    endpoint_url=os.environ["AWS_SQS_SNS_ENDPOINT_URL"],
    region_name=os.environ["AWS_SQS_SNS_REGION"],
)

queue_url = f"{os.environ['AWS_SQS_SNS_ENDPOINT_URL']}/queue/{queue_name}"

print("Start Messages Long Polling!")

while True:
    # Long poll for messages on provided SQS queue; Getting one at a time
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        AttributeNames=["SentTimestamp"],
        MaxNumberOfMessages=1,
        MessageAttributeNames=["All"],
        WaitTimeSeconds=20,
    )

    if "Messages" in response:
        for message in response["Messages"]:

            body = message["Body"]
            content = json.loads(body)

            print(f"Received Message with ID: {message['MessageId']}")
            print(f"Message Content: {content['Message']}")

            # If the message is not deleted it goes back to the queue
            sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"])

    print("Queue is empty!")
