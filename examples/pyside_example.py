import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, \
    QPushButton

from pyosmgui import MapWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PySide Example')
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()

        main_layout = QVBoxLayout()

        lat_lon_layout = QHBoxLayout()
        self.lat_lineedit = QLineEdit()
        self.lat_lineedit.returnPressed.connect(self.go_to_location)
        self.lon_lineedit = QLineEdit()
        self.lon_lineedit.returnPressed.connect(self.go_to_location)
        lat_lon_layout.addWidget(self.lat_lineedit)
        lat_lon_layout.addWidget(self.lon_lineedit)

        main_layout.addLayout(lat_lon_layout)
        self.map_widget = MapWidget()
        self.map_widget.mouse_position_changed.connect(self.mouse_position_changed)
        main_layout.addWidget(self.map_widget)

        self.mouse_position_label = QLabel()
        self.mouse_position_label.setFixedHeight(20)
        main_layout.addWidget(self.mouse_position_label)

        self.locate_button = QPushButton("Locate")
        self.locate_button.clicked.connect(self.map_widget.add_current_location_marker)
        main_layout.addWidget(self.locate_button)

        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

    def go_to_location(self):
        self.map_widget.go_to_location(float(self.lat_lineedit.text()), float(self.lon_lineedit.text()), 19)

    def mouse_position_changed(self, lat, lon):
        self.mouse_position_label.setText(f"Lat: {lat}, Lon: {lon}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
