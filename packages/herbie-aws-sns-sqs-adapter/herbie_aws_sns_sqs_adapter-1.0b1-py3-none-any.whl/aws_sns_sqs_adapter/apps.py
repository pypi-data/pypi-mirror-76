from django.apps import AppConfig


class HerbieAwsSnsSqsAdapterConfig(AppConfig):
    name = "aws_sns_sqs_adapter"
    verbose_name = "HerbieAwsSnsSqsAdapter"

    def ready(self):
        from herbie_core.services.message_publisher.registry import Registry
        from aws_sns_sqs_adapter.publisher.aws_sns_topic_publisher import AwsSnsTopicPublisher

        Registry.add_publisher(AwsSnsTopicPublisher())
