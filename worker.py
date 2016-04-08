import json
import boto3

# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue
queue = sqs.get_queue_by_name(QueueName='tweets')

# Process messages by printing out body and optional author name
message = queue.receive_messages()
print message.body
message.delete()