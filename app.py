import requests
import traceback

from utils import config, host_delete_logging
from mq import kafka_consumer

logger = host_delete_logging.initialize_logging()


def handle_message(parsed):
    try:
        send_request(parsed["insights_id"], parsed["account"])
    except KeyError as e:
        logger.exception("Missing Key in Message: %s", e)


def send_request(insights_id, account):
    logger.debug("sending delete request to legacy")
    URL = "{0}/{1}?account_number={2}".format(config.LEGACY_URL, insights_id, account)

    if config.NAMESPACE is "platform-qa":
        r = requests.delete(URL, auth=(config.LEGACY_USERNAME, config.LEGACY_PASSWORD), 
                                headers={config.PROXY_TOKEN_HEADER: config.PROXY_TOKEN})                                
    else:
        r = requests.delete(URL, auth=(config.LEGACY_USERNAME, config.LEGACY_PASSWORD))

    if r.status_code not in [200, 204]:
        logger.error("Request failed with error: [%s] %s", r.status_code, r.text)


def main():

    logger = host_delete_logging.initialize_logging()
    logger.info("Starting legacy host deletion service")
    config.log_config()

    if not (config.LEGACY_USERNAME and config.LEGACY_PASSWORD):
        raise ValueError("Legacy Username and Password Required")

    consumer = kafka_consumer.init_consumer()

    for data in consumer:
        handle_message(data.value)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        the_error = traceback.format_exc()
        logger.error(f"Insights Host Delete Service failed with error: {the_error}")
