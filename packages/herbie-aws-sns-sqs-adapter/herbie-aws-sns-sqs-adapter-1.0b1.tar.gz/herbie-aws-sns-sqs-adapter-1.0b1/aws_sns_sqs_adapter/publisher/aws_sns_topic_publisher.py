import json
import logging
import boto3
from django.conf import settings
from herbie_core.models.message_models_and_serializers import Message
from herbie_core.services.message_publisher.abstract_publisher import AbstractPublisher


class AwsSnsTopicPublisher(AbstractPublisher):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._sns_client = boto3.client(
            "sns",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_SQS_SNS_ENDPOINT_URL,
            region_name=settings.AWS_SQS_SNS_REGION,
        )
        self._sqs_client = boto3.client(
            "sqs",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_SQS_SNS_ENDPOINT_URL,
            region_name=settings.AWS_SQS_SNS_REGION,
        )

    def get_name(self) -> str:
        return "aws_sns_sqs"

    def send_message(self, message: Message):
        serializer = message.get_serializer()

        topic = serializer.data["type"]
        # Topics are immutable to it's safe to call create as the already existing topic will be returned
        sns_topic = self.create_topic(topic)

        self._sns_client.publish(
            TopicArn=sns_topic["TopicArn"], Message=json.dumps({"default": serializer.data}),
        )

    def subscribe_queue_to_topic(self, topic_arn: str, queue_url: str):
        self._sns_client.subscribe(TopicArn=topic_arn, Protocol="sqs", Endpoint=queue_url)

    def create_topic(self, topic: str) -> dict:
        return self._sns_client.create_topic(Name=topic)

    def create_queue(self, queue_name) -> dict:
        return self._sqs_client.create_queue(QueueName=f"{queue_name}_queue")
