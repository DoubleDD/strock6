import FreeCAD as App
from PySide import QtCore, QtWidgets


def set_angles(doc, azimuth, altitude):
    variables = doc.getObject("Variables")
    variables.azimuth_angle = azimuth
    variables.altitude_angle = altitude
    doc.recompute()
    if "TotalAssembly_Asm4" in App.listDocuments():
        App.getDocument("TotalAssembly_Asm4").recompute()


class DobMotionPanel(QtWidgets.QWidget):
    def __init__(self, doc):
        super().__init__()
        self.doc = doc
        self.setWindowTitle("Dob 旋转演示（Assembly4.1）")
        self.setWindowFlags(QtCore.Qt.Window)
        self.setMinimumWidth(560)

        layout = QtWidgets.QVBoxLayout(self)
        self.azimuth_slider, self.azimuth_spin = self.add_angle_control(
            layout, "方位角", "azimuth_angle"
        )
        self.altitude_slider, self.altitude_spin = self.add_angle_control(
            layout, "俯仰角", "altitude_angle"
        )

        buttons = QtWidgets.QHBoxLayout()
        reset_button = QtWidgets.QPushButton("归零")
        close_button = QtWidgets.QPushButton("关闭")
        buttons.addStretch(1)
        buttons.addWidget(reset_button)
        buttons.addWidget(close_button)
        layout.addLayout(buttons)

        note = QtWidgets.QLabel("输入范围仅用于交互演示，不代表机械限位。")
        note.setWordWrap(True)
        layout.addWidget(note)

        reset_button.clicked.connect(self.reset)
        close_button.clicked.connect(self.close)
        self.azimuth_slider.valueChanged.connect(self.update_angles)
        self.altitude_slider.valueChanged.connect(self.update_angles)

    def add_angle_control(self, layout, title, property_name):
        row = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(title)
        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setRange(-1800, 1800)
        slider.setSingleStep(1)
        slider.setPageStep(10)
        spin = QtWidgets.QDoubleSpinBox()
        spin.setRange(-180.0, 180.0)
        spin.setDecimals(1)
        spin.setSingleStep(0.1)
        spin.setSuffix(" °")
        spin.setKeyboardTracking(False)
        row.addWidget(label)
        row.addWidget(slider, 1)
        row.addWidget(spin)
        layout.addLayout(row)

        value = getattr(self.doc.getObject("Variables"), property_name).Value
        slider.setValue(round(value * 10))
        spin.setValue(value)
        slider.valueChanged.connect(lambda raw, box=spin: box.setValue(raw / 10.0))
        spin.valueChanged.connect(
            lambda degrees, control=slider: control.setValue(round(degrees * 10))
        )
        return slider, spin

    def update_angles(self):
        set_angles(
            self.doc,
            self.azimuth_slider.value() / 10.0,
            self.altitude_slider.value() / 10.0,
        )

    def reset(self):
        self.azimuth_slider.setValue(0)
        self.altitude_slider.setValue(0)
        self.update_angles()


def show_motion_panel():
    doc = App.getDocument("DobAssembly_Asm4")
    if doc is None:
        raise RuntimeError("请先打开 DobAssembly_Asm4.FCStd")
    panel = DobMotionPanel(doc)
    panel.show()
    panel.raise_()
    panel.activateWindow()
    return panel


if __name__ == "__main__":
    _motion_panel = show_motion_panel()
