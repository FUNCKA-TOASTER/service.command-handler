"""File describing the types of actions of VK keyboard buttons.
"""


class BaseAction(object):
    """VK keyboard button action base class.
    """
    def __init__(self, action_type: str):
        self.type = action_type
        self.owner_id = None


    def set_owner(self, value: int):
        """Sets a value to a field
        keyboard owner.

        Args:
            value (int): Keyboard owner id.
        """
        self.owner_id = value


    @property
    def data(self) -> dict:
        """Returns a dictionary representation of the button
        action feilds.
        
        Returns:
            dict: Action dictionary.
        """
        data = {
            key: value for key, value in vars(self).items()
        }

        return data



class Text(BaseAction):
    """Text button. Sends a message with
    the text specified in label.
    """
    def __init__(self, label: str, payload: dict):
        super().__init__("text")

        self.label = label
        self.payload = payload
        self.payload.setdefault("owner_id", self.owner_id)



class OpenLink(BaseAction):
    """Link key. Opens the specified link.
    """
    def __init__(self, url: str, label: str, payload: dict):
        super().__init__("open_link")

        self.link = url
        self.label = label
        self.payload = payload
        self.payload.setdefault("owner_id", self.owner_id)



class Location(BaseAction):
    """When clicked, it sends the location to
    a dialogue with a bot or conversation.
    """
    def __init__(self, url: str, label: str, payload: dict):
        super().__init__("location")

        self.link = url
        self.label = label
        self.payload = payload
        self.payload.setdefault("owner_id", self.owner_id)



class VKPay(BaseAction):
    """Opens the VKPay payment window with
    predefined parameters. The button is called
    “Pay via VKPay”, VKPay is displayed as a logo.
    """
    def __init__(self, payment_hash: str, label: str, payload: dict):
        super().__init__("vkpay")

        self.hash = payment_hash
        self.label = label
        self.payload = payload
        self.payload.setdefault("owner_id", self.owner_id)



class OpenApp(BaseAction):
    """Opens the specified VK Mini Apps
    application.
    """
    def __init__(self, app_hash: str, label: str, payload: dict, app_id: int, owner_id: int):
        super().__init__("open_app")

        self.hash = app_hash
        self.label = label
        self.payload = payload
        self.payload.setdefault("owner_id", self.owner_id)
        self.app_id = app_id
        self.owner_id = owner_id



class Callback(BaseAction):
    """Allows you to receive a notification
    about pressing a button without sending
    a message from the user and perform the
    necessary action.
    """
    def __init__(self, label: str, payload: dict):
        super().__init__("callback")

        self.label = label
        self.payload = payload
        self.payload.setdefault("owner_id", self.owner_id)
