from enum import Enum

class State(Enum):
    NONE = None
    REQUEST = "request"
    SC = "sc"
    RELEASE = "release"

class TokenState(Enum):
    Null = None
    Waiting = "waiting"
    Active = "active"
    Inactive = "inactive"
    Released = "released"
    Requested = "requested"
    Received = "received"
    SC = "sc"