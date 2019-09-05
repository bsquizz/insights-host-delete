import os
import logging

APP_NAME = os.environ.get("APP_NAME", "insights-host-delete")

logger = logging.getLogger(APP_NAME)


def get_namespace():
    try:
        with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r") as f:
            namespace = f.read()
        return namespace
    except EnvironmentError:
        logger.info("Not running in openshift")


def log_config():
    """
    log_config prints out all the config options except for AWS keys
    """
    import sys
    for k, v in sys.modules[__name__].__dict__.items():
        if k == k.upper():
            if "AWS" in k.split("_"):
                continue
            elif "LEGACY" in k.split("_"):
                continue
            logger.info("Using %s: %s", k, v)


TOPIC = os.environ.get("KAFKA_TOPIC", "platform.inventory.events")
KAFKA_GROUP = os.environ.get("KAFKA_GROUP", "insights-host-delete")
BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092").split()
LEGACY_URL = "https://classicqa.cloud.paas.psi.redhat.com/r/insights/inventory"
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
LOG_GROUP = os.environ.get("LOG_GROUP", "platform-dev")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", None)
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
NAMESPACE = get_namespace()

LEGACY_USERNAME = os.environ.get("LEGACY_USERNAME", None)
LEGACY_PASSWORD = os.environ.get("LEGACY_PASSWORD", None)
