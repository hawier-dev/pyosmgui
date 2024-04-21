import importlib

import pyosmgui.widgets


class MapWidget:
    """
    Factory class to create the appropriate map widget based on the available GUI library.
    """
    def __new__(cls, *args, **kwargs):
        try:
            import PySide6.QtWidgets
            return pyosmgui.widgets.PySideMapWidget(*args, **kwargs)

        except ImportError as e:
            print(f"Import error: {e}")

        raise ImportError("No supported GUI library found")