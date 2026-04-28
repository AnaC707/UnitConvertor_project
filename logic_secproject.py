from PyQt6.QtWidgets import *
from gui_secproject import *
import csv
import os

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.from_box.clear()
        self.to_box.clear()
        self.from_box.setPlaceholderText("Select unit")
        self.to_box.setPlaceholderText("Select unit")

        self.units = {
            "Length": ["Meters", "Kilometers", "Miles", "Feet"],
            "Weight": ["Grams", "Kilograms", "Pounds"],
            "Temperature": ["Celsius", "Fahrenheit"]
        }
        self.connections()

    def connections(self):
        self.length_button.toggled.connect(self.update_units)
        self.weight_button.toggled.connect(self.update_units)
        self.temp_button.toggled.connect(self.update_units)

        self.enter_button.clicked.connect(self.handle_convert)

    def update_units(self):
        category = self.get_category()
        if not category:
            return

        self.results_label.setText("")
        units = self.units[category]

        self.from_box.clear()
        self.to_box.clear()
        self.from_box.addItems(units)
        self.to_box.addItems(units)
        self.from_box.setCurrentIndex(-1)
        self.to_box.setCurrentIndex(-1)
        self.results_label.setText("Results")

    def get_category(self):
        if self.length_button.isChecked():
            return "Length"
        elif self.weight_button.isChecked():
            return "Weight"
        elif self.temp_button.isChecked():
            return "Temperature"
        else:
            return None

    def handle_convert(self):
        try:
            value = float(self.initial_value.text().strip())
            category = self.get_category()
            if not category:
                self.results_label.setText("Select a category")
                return

            from_unit = self.from_box.currentText()
            to_unit = self.to_box.currentText()
            if not from_unit or not to_unit:
                self.results_label.setText("Select both units")
                return

            result = self.convert(value, category, from_unit, to_unit)
            self.results_label.setText(f"{value:.4f} {from_unit} --> {result:.4f} {to_unit}")
            self.save_data(category, value, from_unit, result, to_unit)
            self.initial_value.setFocus()
            self.initial_value.selectAll()

        except ValueError:
            self.results_label.setText("Please enter numbers")
            self.initial_value.setFocus()
            self.initial_value.selectAll()

    def convert(self, value, category, from_unit, to_unit):
        if from_unit == to_unit:
            return value

        if category == "Length":
            base = {
                "Meters": 1,
                "Kilometers": 1000,
                "Miles": 1609.34,
                "Feet": 0.3048
            }
            return value * base[from_unit] / base[to_unit]

        elif category == "Weight":
            base = {
                "Grams": 0.001,
                "Kilograms": 1,
                "Pounds": 0.453592
            }
            return value * base[from_unit] / base[to_unit]

        elif category == "Temperature":
            if from_unit == "Celsius" and to_unit == "Fahrenheit":
                return value * 9/5 + 32
            elif from_unit == "Fahrenheit" and to_unit == "Celsius":
                return (value - 32) * 5/9

        return value

    def save_data(self, category, value, from_unit, result, to_unit):
        file_exists = os.path.isfile("conversions.csv")

        with open("conversions.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(["Category", "Input", "From", "Result", "To"])

            writer.writerow([category, f"{value:.4f}", from_unit, f"{result:.4f}", to_unit])
