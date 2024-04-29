"""Module "producer"."""

from .body import Producer


class CustomProducer(Producer):
    """Custom producer class.
    Preferences for implimentation of custom
    functions for working with data that needs
    to be pushed into a queue inside RabbitMQ.
    """

    event_queues = {"warn": "warns", "alert": "alerts"}

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

    async def command_alert(self, event, command_name, cmids: list = None):
        queue = self.event_queues["alert"]
        forward = ", ".join(cmids) if cmids else None
        data = {
            "alert_type": "command",
            "user_id": event.get("user_id"),
            "user_name": event.get("user_name"),
            "peer_name": event.get("peer_name"),
            "peer_id": event.get("peer_id"),
            "command_name": command_name,
            "forward": forward,
        }
        await self._send_data(data, queue)

    async def kick_alert(self, event, target_id, target_name, cmids: list = None):
        queue = self.event_queues["alert"]
        forward = ", ".join(cmids) if cmids else None
        data = {
            "alert_type": "command",
            "user_id": target_id,
            "user_name": target_name,
            "peer_name": event.get("peer_name"),
            "peer_id": event.get("peer_id"),
            "moderator_name": event.get("user_id"),
            "moderator_id": event.get("user_name"),
            "forward": forward,
        }
        await self._send_data(data, queue)


producer = CustomProducer()
