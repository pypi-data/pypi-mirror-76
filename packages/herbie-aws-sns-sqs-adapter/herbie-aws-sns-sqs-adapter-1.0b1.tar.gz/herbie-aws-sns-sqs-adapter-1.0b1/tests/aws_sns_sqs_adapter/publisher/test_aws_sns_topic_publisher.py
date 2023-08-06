from unittest import mock
from unittest.mock import Mock

from django.test import SimpleTestCase

from aws_sns_sqs_adapter.publisher.aws_sns_topic_publisher import AwsSnsTopicPublisher


class AwsSnsTopicPublisherTestCase(SimpleTestCase):
    def setUp(self) -> None:
        self._sns_client_mock = Mock()
        self._sqs_client_mock = Mock()

    @mock.patch("aws_sns_sqs_adapter.publisher.aws_sns_topic_publisher.boto3")
    def test_send_message(self, mock_boto3):
        self._sns_client_mock.create_topic.return_value = {"TopicArn": "aws-topic-arn-endpoint"}
        mock_boto3.client.side_effect = [self._sns_client_mock, self._sqs_client_mock]

        serializer_mock = Mock(data={"type": "aws-type", "payload": {"field": "value"}})

        message_mock = Mock()
        message_mock.get_serializer.return_value = serializer_mock

        publisher = AwsSnsTopicPublisher()
        publisher.send_message(message_mock)

        self._sns_client_mock.create_topic.assert_called_with(Name="aws-type")
        self._sns_client_mock.publish.assert_called_with(
            TopicArn="aws-topic-arn-endpoint",
            Message='{"default": {"type": "aws-type", "payload": {"field": "value"}}}',
        )
