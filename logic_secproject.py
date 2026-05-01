from PyQt6.QtWidgets import *
from gui_secproject import *
import csv
import os

class Logic(QMainWindow, Ui_MainWindow):
    """
    A class that sets the application logic for the unit converter.
    """
    def __init__(self)->None:
        """
        The method initializes the main window, sets the units available, and
        calls the connections function. Also, AI helped me configure the combo
        boxes to show no selected item by default until the user chooses a unit.
        """
        super().__init__()
        self.setupUi(self)

        self.from_box.setPlaceholderText("Select unit")
        self.to_box.setPlaceholderText("Select unit")
        self.from_box.setCurrentIndex(-1)
        self.to_box.setCurrentIndex(-1)

        self.units = {
            "Length": ["Meters", "Kilometers", "Miles", "Feet"],
            "Weight": ["Grams", "Kilograms", "Pounds"],
            "Temperature": ["Celsius", "Fahrenheit"]
        }
        self.connections()

    def connections(self)->None:
        """
        This method connects the UI buttons to their respective functions.
        """
        self.length_button.toggled.connect(self.update_units)
        self.weight_button.toggled.connect(self.update_units)
        self.temp_button.toggled.connect(self.update_units)
        self.enter_button.clicked.connect(self.handle_convert)

    def update_units(self)->None:
        """
        This method checks if a category is selected, updates the unit combo
        boxes depending on the selected category, clears previous results,
        and resets the combo box selections.
        """
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

    def get_category(self)->str|None:
        """
        The method returns the selected category or None if not selected.
        :return: name of selected category or None.
        """
        if self.length_button.isChecked():
            return "Length"
        elif self.weight_button.isChecked():
            return "Weight"
        elif self.temp_button.isChecked():
            return "Temperature"
        else:
            return None

    def handle_convert(self)->None:
        """
        The method handles the process when the Enter button is clicked. It also
        validates input, checks if units are selected, displays results, and saves data.
        AI gave me the suggestion to highlight the current input value after a
        conversion is done, so I implemented it.
        """
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

    def convert(self, value: float, category: str, from_unit: str, to_unit: str)->float:
        """
        The method converts the input value to the desired unit.
        Because the base units are Meters and Kilograms, the other units are converted
        to the equivalent of 1 meter or kilogram. AI helped me on how to implement it.
        :param value: user's input value
        :param category: conversion category
        :param from_unit: unit to convert from
        :param to_unit: unit to convert to
        :return: the converted value; result
        """
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

    def save_data(self, category: str, value: float, from_unit: str, result: float, to_unit: str)->None:
        """
        This method saves the conversion process to the csv file and checks if
        the file exists, or creates a new one if needed.
        :param category: conversion category
        :param value: user's input value
        :param from_unit: starting unit
        :param result: converted value
        :param to_unit: ending unit
        """
        file_exists = os.path.isfile("conversions.csv")

        with open("conversions.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(["Category", "Input", "From", "Result", "To"])

            writer.writerow([category, f"{value:.4f}", from_unit, f"{result:.4f}", to_unit])
