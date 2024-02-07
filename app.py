import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QMessageBox

class OrderPickerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Layout
        layout = QVBoxLayout()

        # Description Label
        self.desc_label = QLabel("Copyright 2024 @team2C04 no right preserved.\n作者對腹瀉或踩雷不負任何責任！")
        layout.addWidget(self.desc_label)

        # Budget Input
        self.budget_input = QLineEdit()
        self.budget_input.setPlaceholderText("Enter your budget")
        layout.addWidget(self.budget_input)

        # Checkboxes
        self.cb_beverage = QCheckBox("Exclude Beverages")
        self.cb_burger = QCheckBox("Exclude Burgers")
        self.cb_pancake = QCheckBox("Exclude Pancakes")
        layout.addWidget(self.cb_beverage)
        layout.addWidget(self.cb_burger)
        layout.addWidget(self.cb_pancake)

        # Pick Order Button
        self.pick_button = QPushButton("Pick Order")
        self.pick_button.clicked.connect(self.pick_order)
        layout.addWidget(self.pick_button)

        # Set the layout
        self.setLayout(layout)

        # Window configurations
        self.setWindowTitle('Order Picker')
        self.setGeometry(300, 300, 300, 200)  # Modify as needed
        self.show()

    def pick_order(self):
        # Placeholder for order picking logic
        QMessageBox.information(self, "Order", "Order picked! (placeholder)")

# Main execution
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = OrderPickerApp()
    sys.exit(app.exec())
