import os
from pathlib import Path

import geocoder
from PySide6.QtGui import QResizeEvent
from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import QUrl, Slot, QTimer, QObject, Signal
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
import os

from pyosmgui.enums.event_type import EventType
from pyosmgui.utils.web_page import WebPage

os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = "9222"


class PySideMapWidget(QWidget):
    mouse_position_changed = Signal(float, float)
    zoom_level_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.browser = QWebEngineView(self)
        self.web_page = WebPage()
        self.web_page.message_received.connect(self._on_event_received)

        self.browser.setPage(self.web_page)
        self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
        self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.SpatialNavigationEnabled, True)

        self.browser.contextMenuEvent = lambda a: None

        layout = QVBoxLayout(self)
        layout.addWidget(self.browser)
        self.setLayout(layout)
        self._load_map()

    def resizeEvent(self, event):
        self._resize_map()

    def _resize_map(self):
        height = self.browser.height()
        self._run_javascript(f"resizeMap({height});")

    def go_to_location(self, lat, lon, zoom=16):
        """
        Centers the map view on a specified geographic location.

        Parameters:
            lat (float): The latitude of the location to which the map view should be centered.
            lon (float): The longitude of the location to which the map view should be centered.
            zoom (int, optional): The zoom level for the map view. Defaults to 16, which represents
                                  a detailed street-level view.

        Example:
            >>> map_widget.go_to_location(51.5074, -0.1278)
            This will center the map on London with a default zoom level of 16.
        """

        self._run_javascript(f"goToLocation({lat}, {lon}, {zoom});")

    def add_marker(self, lat, lon, popup_text="", icon=None, icon_size=None):
        """
        Adds a marker to the map view at a specified geographic location.

        Parameters:
            lat (float): The latitude of the location where the marker should be placed.
            lon (float): The longitude of the location where the marker should be placed.
            popup_text (str): The text that should be displayed when the marker is clicked.
            icon (str, optional): The path to the icon to be used for the marker
            icon_size (str, optional): The size of the icon to be used for the marker.

        Example:
            >>> map_widget.add_marker(51.5074, -0.1278, "London", "default", 20)
            This will add a marker to the map at London with a popup text "London".
        """

        self._run_javascript(f"addMarker({lat}, {lon}, '{popup_text}', '{icon}', '{icon_size}')")

    def add_current_location_marker(self, popup_text="You are here!", icon=None, icon_size=None):
        """
        Adds a marker to the map view at the current geographic location.

        Parameters:
            popup_text (str, optional): The text that should be displayed when the marker is clicked. Defaults to "You are here!".
            icon (str, optional): The path to the icon to be used for the marker
            icon_size (str, optional): The size of the icon to be used for the marker.
        """
        g = geocoder.ip('me')
        if icon is not None:
            icon = Path(icon).as_uri()
        self._run_javascript(f"addCurrentLocationMarker({g.latlng[0]}, {g.latlng[1]}, '{popup_text}', '{icon}', '{icon_size}')")

    def _run_javascript(self, script):
        self.browser.page().runJavaScript(script)

    def _on_event_received(self, event_type, event_data):
        if event_type == EventType.MOUSE_MOVE:
            lat, lon = event_data.split(", ")
            self.mouse_position_changed.emit(float(lat), float(lon))

        elif event_type == EventType.MAP_LOADED:
            self._resize_map()

        elif event_type == EventType.ZOOM_LEVEL:
            self.zoom_level_changed.emit(int(event_data))

    def _load_map(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_file_path = os.path.join(current_dir, '..', 'resources', 'html', 'leaflet_map.html')
        html_url = QUrl.fromLocalFile(html_file_path)
        self.browser.page().load(html_url)

