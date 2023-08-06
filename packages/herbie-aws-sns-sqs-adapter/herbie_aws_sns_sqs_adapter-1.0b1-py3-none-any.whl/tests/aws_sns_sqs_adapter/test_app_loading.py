from unittest import mock

from django.apps import apps
from django.test import SimpleTestCase

from aws_sns_sqs_adapter.apps import HerbieAwsSnsSqsAdapterConfig


class AppLoadingTestCase(SimpleTestCase):
    def tearDown(self):
        apps.clear_cache()

    @mock.patch("aws_sns_sqs_adapter.publisher.aws_sns_topic_publisher.AwsSnsTopicPublisher")
    def test_loading_app(self, mock_sns_topic_publisher):
        with self.settings(
            INSTALLED_APPS=["aws_sns_sqs_adapter.apps.HerbieAwsSnsSqsAdapterConfig"],
            AWS_ACCESS_KEY_ID="key",
            AWS_SECRET_ACCESS_KEY="secret",
            AWS_SQS_SNS_ENDPOINT_URL="endpoint",
            AWS_SQS_SNS_REGION="region",
        ):
            mock_sns_topic_publisher()

            self.assertIsNotNone(apps.get_app_config(HerbieAwsSnsSqsAdapterConfig.name))
