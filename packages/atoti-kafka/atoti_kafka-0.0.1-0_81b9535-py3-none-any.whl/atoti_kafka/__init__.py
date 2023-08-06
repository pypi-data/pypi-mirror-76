"""Kafka extension for atoti."""

from pathlib import Path
from typing import Any

from .custom_deserializer import CustomDeserializer
from .source import KafkaDataSource

JAR_NAME = "atoti-kafka-source.jar"
JAR_PATH = (Path(__file__).parent / "data" / JAR_NAME).absolute()


def init_extension(session: Any):
    """Initialize the extension."""
    # pylint: disable = protected-access
    session._java_api.gateway.jvm.com.activeviam.chouket.loading.kafka.KafkaExtension.init()
