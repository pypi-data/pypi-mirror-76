# AWS SNS/SQS Adapter

This Adapter is based on Django and provides a way to publish messages to AWS SNS/SQS. 

The default configuration creates a single SNS Topic on which a single SQS Queue subscribes for new messages.

An example [SQS consumer](example_consumer) is also available.

It is meant to be used with [Herbie](https://github.com/herbie/herbie).

## Installation

The package already provides a Django app that just needs to be registered in the main Django app using Herbie.

1. Run the following
```
    pip install herbie-aws-sns-sqs-adapter
```

or add it to your app requirements.txt and update them running:

    pip install -r requirements.txt

2. Add the adapter App to Django Installed Apllications:

```
INSTALLED_APPS = [
    ...
    'aws_sns_sqs_adapter.apps.HerbieAwsSnsSqsAdapterConfig',
    ...
]
```

3. Configure the _AWS environment variables_:

```
AWS_ACCESS_KEY_ID="access_key",
AWS_SECRET_ACCESS_KEY="secret_key",
AWS_SQS_SNS_ENDPOINT_URL="sns_sqs_endpoint",
AWS_SQS_SNS_REGION="sns_sqs_region",
```

4. Run command to create the SNS/SQS Topics/Queues according to the schemas available. 
This command will create 1 SNS Topic and 1 SQS Queue per schema available; the queue will subscribe to the respective created topic.

```
python manage.py init_sns_sqs
```

An example Django application using this adapter can be found at the [Herbie Sandbox](https://github.com/herbie/sandbox) repository.

## Developing/Testing

If you would like to further improve this package you'll need to install the dev/test requirmeents. 

To to this run in your `virtual environment`

```
    pip install -e .[tests]
```

This will install the needed packages (e.g: `pytest`) to run/test locally the package

### Black Formatter

This package uses [Black](https://github.com/psf/black) as a code formatter. You should run it before 
pushing the code as the CI pipeline checks against it.

```
    black --line-length 119 .
```
