from enum import Enum


class EventType(Enum):
    UNKNOWN = "unknown"
    MOUSE_MOVE = "mouse_move"
    MAP_LOADED = "map_loaded"
    ZOOM_LEVEL = "zoom_level"
