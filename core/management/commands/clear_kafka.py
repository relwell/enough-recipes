"""Clear Kafka topics."""
from django.conf import settings
from django.core.management.base import BaseCommand

from kafka.admin import KafkaAdminClient
from kafka.errors import UnknownTopicOrPartitionError


class Command(BaseCommand):
    """Does the command."""

    def add_arguments(self, parser) -> None:
        parser.add_argument("topic_names", nargs="+", type=str)

    def handle(self, *args, **_options):
        [topic_names] = args
        try:
            KafkaAdminClient(
                bootstrap_servers=settings.KAFKA_BROKERS,
            ).delete_topics(topics=topic_names)
            print("Topic Deleted Successfully")
        except UnknownTopicOrPartitionError:
            print("Topic Doesn't Exist")
        except Exception as exc:  # pylint: disable=broad-except
            print(exc)
