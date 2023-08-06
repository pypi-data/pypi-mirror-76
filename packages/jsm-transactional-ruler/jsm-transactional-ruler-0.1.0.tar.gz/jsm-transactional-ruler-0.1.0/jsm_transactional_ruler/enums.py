from enum import Enum


class EventType(Enum):
    T_EVENT_REGISTERED_USER = "T_EVENT_REGISTERED_USER"
    T_EVENT_GENERAL_ORDER_MADE = "T_EVENT_GENERAL_ORDER_MADE"
    T_EVENT_MOBILE_RECHARGE_ORDER_MADE = "T_EVENT_MOBILE_RECHARGE_ORDER_MADE"

    @classmethod
    def get_choices(cls):
        return tuple(item.value for item in cls)
