from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtWebEngineCore import QWebEnginePage

from pyosmgui.enums.event_type import EventType


class WebPage(QWebEnginePage):
    message_received = Signal(EventType, str)

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        print(f"Console message: {msg}")
        try:
            event_split = msg.split(":")
            event_type = EventType(event_split[0])
            event_data = event_split[1]
            self.message_received.emit(event_type, event_data)
        except:
            event_type = EventType.UNKNOWN
            event_data = msg
            self.message_received.emit(event_type, event_data)
