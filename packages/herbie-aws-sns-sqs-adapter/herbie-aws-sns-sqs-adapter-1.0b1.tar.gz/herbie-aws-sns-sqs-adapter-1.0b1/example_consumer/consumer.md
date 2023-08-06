# Example SQS Consumer

This simple script checks for messages in a SQS Queue using a Long polling feature that reduces
the amount of calls/cost of using Amazon SQS.

The Consumer docker container connects to the AWS SNS/SQS emulator and polls for new messages in an infinite loop.


## How to run

- The Consumer should use the same network where the AWS SNS/SQS emulator runs 
(if needed change the docker compose file).

```
networks:
  sandbox_herbie-network:
    external: true
```

Build/Run the Docker Container

```
docker-compose -f docker-compose-sqs-consumer.yml up
```

The consumer will fetch and delete the messages available in the Queue.

Consumer Example Output:

```
Attaching to herbie-sqs-consumer
herbie-sqs-consumer    | Start Messages Long Polling!
herbie-sqs-consumer    | Received Message with ID: 9ba69015-9da5-430e-bd76-289bc093fc97
herbie-sqs-consumer    | Message Content: {"default": {"tags": [], "action": "update", "type": "customer", "key": "asfasff", "version": "v1", "payload": {"firstName": "Name", "lastName": "Last"}, "created": "2020-07-20 14:47:30.362115+00:00", "modified": "2020-07-20 14:47:30.362115+00:00"}}
herbie-sqs-consumer    | Queue is empty!

```