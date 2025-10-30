import logging
import os
from pythonjsonlogger import jsonlogger
import watchtower
import boto3


class CloudWatchLogger:
    def __init__(self, log_group, log_stream, aws_region="us-east-1"):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Create formatter
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # CloudWatch handler if AWS credentials are available
        if all(k in os.environ for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY")):
            boto3_client = boto3.client("logs", region_name=aws_region)
            cw_handler = watchtower.CloudWatchLogHandler(
                log_group=log_group,
                log_stream_name=log_stream,
                boto3_client=boto3_client,
            )
            cw_handler.setFormatter(formatter)
            self.logger.addHandler(cw_handler)

    def get_logger(self):
        return self.logger


# Initialize logger
logger = CloudWatchLogger(log_group="AgenticAI", log_stream="app-logs").get_logger()
