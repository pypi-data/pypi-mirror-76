import environ
from django.conf import settings

env = environ.Env()


def pytest_configure():
    settings.configure(
        AWS_ACCESS_KEY_ID="key",
        AWS_SECRET_ACCESS_KEY="secret",
        AWS_SQS_SNS_ENDPOINT_URL="endpoint",
        AWS_SQS_SNS_REGION="region",
        DEBUG=True,
        SECRET_KEY="thisisthesecretkey",
        MIDDLEWARE_CLASSES=(
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ),
        INSTALLED_APPS=("herbie_core", "django.contrib.contenttypes", "django.contrib.auth",),
    )
