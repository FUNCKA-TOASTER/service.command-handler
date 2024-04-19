"""Module "producer"."""

from .body import Producer


class CustomProducer(Producer):
    """Custom producer class.
    Preferences for implimentation of custom
    functions for working with data that needs
    to be pushed into a queue inside RabbitMQ.
    """

    event_queues = {
        "warn": "warns",
    }

    async def initiate_warn(self, event, warns, target, target_name, target_cmid):
        queue = self.event_queues["warn"]
        data = {
            "author_id": event.get("user_id"),
            "author_name": event.get("user_name"),
            "reason_message": "модератор вынес вам предупреждение!",
            "setting": None,
            "target_id": target,
            "target_name": target_name,
            "peer_id": event.get("peer_id"),
            "cmid": event.get("cmid"),
            "warn_count": warns,
            "target_message_cmid": target_cmid,
        }
        await self._send_data(data, queue)


producer = CustomProducer()
