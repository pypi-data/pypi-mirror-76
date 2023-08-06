import logging
from django.core.management import BaseCommand
from herbie_core.services.schema_package import SchemaPackage
from aws_sns_sqs_adapter.publisher.aws_sns_topic_publisher import AwsSnsTopicPublisher


class Command(BaseCommand):
    help = "initialize SNS Topics and SQS Queues"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._logger = logging.getLogger(__name__)
        self._publisher = AwsSnsTopicPublisher()
        self._schema_package = SchemaPackage()

    def handle(self, *args, **kwargs):
        names = self._schema_package.get_all_schema_names()
        print(f"Schemas Available: {names}")

        for name in names:
            topic = self._publisher.create_topic(name)
            queue = self._publisher.create_queue(name)

            self._publisher.subscribe_queue_to_topic(topic["TopicArn"], queue["QueueUrl"])

            print(f'Created SNS Topic and SQS Queue for Schema: "{name}"')
