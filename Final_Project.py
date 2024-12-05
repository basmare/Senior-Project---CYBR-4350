import sys
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QSizePolicy
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt
import locale



class DataBreachEstimator(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the window (minimal flags to include a close button)
        self.setWindowFlags(Qt.Window)

        # Load data
        self.load_data()

        # Set up the window
        self.setWindowTitle("Data Breach Impact Estimator")
        self.setGeometry(0, 0, 1920, 1080)  # Full-screen size

        # Background Image
        self.background_label = QLabel(self)
        self.background_pixmap = QPixmap("background.png")  # Replace with your image file
        self.background_pixmap = self.background_pixmap.scaled(
            self.width(), self.height(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation
        )
        self.background_label.setPixmap(self.background_pixmap)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.setScaledContents(True)

        # Semi-transparent overlay
        self.overlay = QWidget(self)
        self.overlay.setGeometry(self.width() // 6, self.height() // 6, self.width() * 2 // 3, self.height() * 2 // 3)
        self.overlay.setAutoFillBackground(True)
        overlay_palette = self.overlay.palette()
        overlay_palette.setColor(QPalette.Window, QColor(255, 255, 255, 300))  # Semi-transparent
        self.overlay.setPalette(overlay_palette)

        # Layout for the overlay
        layout = QVBoxLayout(self.overlay)

        # Title
        title = QLabel("Data Breach Impact Estimator", self.overlay)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: black;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # State Dropdown
        self.state_label = QLabel("Select State:", self.overlay)
        self.state_label.setStyleSheet("font-size: 18px; color: black;")  
        self.state_dropdown = QComboBox(self.overlay)
        self.state_dropdown.addItem("")  # Add an empty option
        self.state_dropdown.addItems(self.states)  # Populate with unique states
        self.state_dropdown.setStyleSheet("""
            QComboBox {
                background-color: #FFFFFF;  /* Background color */
                font-size: 13px;
                padding: 8px;  /* Padding to make it look more rectangular */
                color: #000000;  /* Light gold text color */
                border: 2px solid #014421;  /* Light gold border */
                border-radius: 10px;  /* Rounded corners for a modern look */
            }
            QComboBox::drop-down {
                border: 0px;  /* Remove drop-down border */
            }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;  /* Same background for dropdown */
                color: #000000;  /* Same text color */
                selection-background-color: #000000;  /* Highlight color when an option is selected */
                selection-color: #FFFFFF;  /* Inverse color for text when highlighted */
            }
        """)
        layout.addWidget(self.state_label)
        layout.addWidget(self.state_dropdown)

        # Regulation Dropdown
        self.reg_label = QLabel("State Regulation:", self.overlay)
        self.reg_label.setStyleSheet("font-size: 18px; color: black;")  # Set label color to black for consistency
        self.reg_dropdown = QComboBox(self.overlay)
        self.reg_dropdown.addItem("")  # Add an empty option
        self.update_regulations()  # Initially populate based on the first state
        self.state_dropdown.currentIndexChanged.connect(self.update_regulations)  # Update regulations dynamically
        self.reg_dropdown.setStyleSheet("""
            QComboBox {
                background-color: #FFFFFF;  /* Background color */
                font-size: 13px;
                padding: 8px;  /* Padding to make it look more rectangular */
                color: #000000;  /* Light gold text color */
                border: 2px solid #014421;  /* Light gold border */
                border-radius: 10px;  /* Rounded corners for a modern look */
            }
            QComboBox::drop-down {
                border: 0px;  /* Remove drop-down border */
            }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;  /* Same background for dropdown */
                color: #000000;  /* Same text color */
                selection-background-color: #000000;  /* Highlight color when an option is selected */
                selection-color: #FFFFFF;  /* Inverse color for text when highlighted */
            }
        """)
        layout.addWidget(self.reg_label)
        layout.addWidget(self.reg_dropdown)

        # Federal Regulation Dropdown
        self.fed_reg_label = QLabel("Federal Regulation:", self.overlay)
        self.fed_reg_label.setStyleSheet("font-size: 18px; color: black;")  # Set label color to black for consistency
        self.fed_reg_dropdown = QComboBox(self.overlay)
        self.fed_reg_dropdown.addItem("")  # Add an empty option
        self.fed_reg_dropdown.addItems(self.federal_regulations['Regulation'].unique())
        self.fed_reg_dropdown.setStyleSheet("""
            QComboBox {
                background-color: #FFFFFF;  /* Background color */
                font-size: 13px;
                padding: 8px;  /* Padding to make it look more rectangular */
                color: #000000;  /* Light gold text color */
                border: 2px solid #014421;  /* Light gold border */
                border-radius: 10px;  /* Rounded corners for a modern look */
            }
            QComboBox::drop-down {
                border: 0px;  /* Remove drop-down border */
            }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;  /* Same background for dropdown */
                color: #000000;  /* Same text color */
                selection-background-color: #000000;  /* Highlight color when an option is selected */
                selection-color: #FFFFFF;  /* Inverse color for text when highlighted */
            }
        """)
        layout.addWidget(self.fed_reg_label)
        layout.addWidget(self.fed_reg_dropdown)

        # Federal Violation Dropdown
        self.fed_viol_label = QLabel("Federal Violation:", self.overlay)
        self.fed_viol_label.setStyleSheet("font-size: 18px; color: black;")  # Set label color to black for consistency
        self.fed_viol_dropdown = QComboBox(self.overlay)
        self.fed_viol_dropdown.addItem("")  # Add an empty option
        self.update_federal_violations()  # Initially populate based on the first federal regulation
        self.fed_reg_dropdown.currentIndexChanged.connect(self.update_federal_violations)
        self.fed_viol_dropdown.setStyleSheet("""
            QComboBox {
                background-color: #FFFFFF;  /* Background color */
                font-size: 13px;
                padding: 8px;  /* Padding to make it look more rectangular */
                color: #000000;  /* Light gold text color */
                border: 2px solid #014421;  /* Light gold border */
                border-radius: 10px;  /* Rounded corners for a modern look */
            }
            QComboBox::drop-down {
                border: 0px;  /* Remove drop-down border */
            }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;  /* Same background for dropdown */
                color: #000000;  /* Same text color */
                selection-background-color: #000000;  /* Highlight color when an option is selected */
                selection-color: #FFFFFF;  /* Inverse color for text when highlighted */
            }
        """)
        layout.addWidget(self.fed_viol_label)
        layout.addWidget(self.fed_viol_dropdown)

        # Records Input
        self.records_label = QLabel("Number of Records:", self.overlay)
        self.records_label.setStyleSheet("font-size: 18px; color: black;")  # Set label color to black for consistency
        self.records_input = QLineEdit(self.overlay)
        self.records_input.setPlaceholderText("Enter the number of records breached")
        self.records_input.setStyleSheet("""
            background-color: #FFFFFF; 
            font-size: 13px; 
            padding: 8px; 
            color: #000000; 
            border: 2px solid #014421; 
            border-radius: 10px; 
        """)
        layout.addWidget(self.records_label)
        layout.addWidget(self.records_input)
       
        # Calculate Button
        self.calculate_button = QPushButton("Calculate Fines", self.overlay)
        self.calculate_button.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                font-size: 13px;
                padding: 12px;
                color: #FEDC97;
                border: 2px solid #014421;
                border-radius: 10px;
                min-width: 150px;
            }
        """)
        self.calculate_button.clicked.connect(self.calculate_fines)
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.calculate_button, alignment=Qt.AlignCenter)
        layout.addLayout(button_layout)

      # Output Label
        self.output_label = QLabel("", self.overlay)
        self.output_label.setStyleSheet("""
            QLabel {
                background-color: #FFFFFF;  /* Background color */
                font-size: 15px;  /* Text size */
                padding: 8px;  /* Reduce padding for a smaller box */
                color: #000000;  /* Text color */
                border: 2px solid #014421;  /* Border color */
                border-radius: 10px;  /* Rounded corners */
                min-height: 150px;  /* Reduce minimum height */
            }
        """)
        self.output_label.setWordWrap(True)  # Enable word wrapping
        self.output_label.setMinimumHeight(150)  # Reduce the minimum height
        self.output_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)  # Allow vertical shrinking
        layout.addWidget(self.output_label)

        # Footer
        footer_label = QLabel("© Blen Asmare, 2024", self.overlay)  
        footer_label.setStyleSheet("font-size: 14px; color: black;")
        footer_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer_label)



    def load_data(self):
        """
        Load data from Excel file.
        """
        excel_file_path = "Blen_Asmare_Project_draft.xlsx"
        try:
            # Prevent default NaN conversion
            data = pd.ExcelFile(excel_file_path)
            self.state_regulations = data.parse("State Regulations", keep_default_na=False, na_values=[])
            self.federal_regulations = data.parse("Federal Regulations", keep_default_na=False, na_values=[])

            self.states = self.state_regulations['State'].unique()  # Unique list of states
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            sys.exit()

    def update_regulations(self):
        """
        Update the state regulations dropdown based on the selected state.
        """
        selected_state = self.state_dropdown.currentText()
        filtered_regulations = self.state_regulations[
            self.state_regulations['State'] == selected_state
        ]['Regulation'].unique()
        self.reg_dropdown.clear()
        self.reg_dropdown.addItem("")  # Add an empty option
        self.reg_dropdown.addItems(filtered_regulations)

    def update_federal_violations(self):
        """
        Update the federal violations dropdown based on the selected federal regulation.
        """
        selected_fed_regulation = self.fed_reg_dropdown.currentText()
        filtered_violations = self.federal_regulations[
            self.federal_regulations['Regulation'] == selected_fed_regulation
        ]['Violation Type'].unique()
        self.fed_viol_dropdown.clear()
        self.fed_viol_dropdown.addItem("")  # Add an empty option
        self.fed_viol_dropdown.addItems(filtered_violations)

    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    def calculate_fines(self):
        """
        Perform the fine calculations based on user inputs.
        """
        try:
            # Retrieve inputs
            state = self.state_dropdown.currentText()
            state_reg = self.reg_dropdown.currentText()
            fed_reg = self.fed_reg_dropdown.currentText()
            fed_viol = self.fed_viol_dropdown.currentText()
            records = int(self.records_input.text())

            # Lookup state fines
            state_row = self.state_regulations[
                (self.state_regulations['State'] == state) &
                (self.state_regulations['Regulation'] == state_reg)
            ]
            state_min = state_row['Min Fine'].values[0] if not state_row.empty else "N/A"
            state_max = state_row['Max Fine'].values[0] if not state_row.empty else "N/A"

            # Lookup federal fines
            fed_row = self.federal_regulations[
                (self.federal_regulations['Regulation'] == fed_reg) &
                (self.federal_regulations['Violation Type'] == fed_viol)
            ]
            fed_min = fed_row['Min Fine'].values[0] if not fed_row.empty else "N/A"
            fed_max = fed_row['Max Fine'].values[0] if not fed_row.empty else "N/A"

            # Ensure numerical values for fines
            state_min = float(state_min) if state_min != "N/A" else "N/A"
            state_max = float(state_max) if state_max != "N/A" else "N/A"
            fed_min = float(fed_min) if fed_min != "N/A" else "N/A"
            fed_max = float(fed_max) if fed_max != "N/A" else "N/A"

            # Calculate total fines
            state_min_total = state_min * records if isinstance(state_min, (int, float)) else "N/A"
            state_max_total = state_max * records if isinstance(state_max, (int, float)) else "N/A"
            fed_min_total = fed_min * records if isinstance(fed_min, (int, float)) else "N/A"
            fed_max_total = fed_max * records if isinstance(fed_max, (int, float)) else "N/A"
            credit_cost = records * 20  # Example: $20 per record

            # Total calculated fines (state + federal)
            total_min_fine = (
                (state_min_total if isinstance(state_min_total, (int, float)) else 0) +
                (fed_min_total if isinstance(fed_min_total, (int, float)) else 0)
            )
            total_max_fine = (
                (state_max_total if isinstance(state_max_total, (int, float)) else 0) +
                (fed_max_total if isinstance(fed_max_total, (int, float)) else 0)
            )

            # Format numbers as currency
            state_min_total = locale.currency(state_min_total, grouping=True) if isinstance(state_min_total, (int, float)) else "N/A"
            state_max_total = locale.currency(state_max_total, grouping=True) if isinstance(state_max_total, (int, float)) else "N/A"
            fed_min_total = locale.currency(fed_min_total, grouping=True) if isinstance(fed_min_total, (int, float)) else "N/A"
            fed_max_total = locale.currency(fed_max_total, grouping=True) if isinstance(fed_max_total, (int, float)) else "N/A"
            total_min_fine = locale.currency(total_min_fine, grouping=True) if isinstance(total_min_fine, (int, float)) else "N/A"
            total_max_fine = locale.currency(total_max_fine, grouping=True) if isinstance(total_max_fine, (int, float)) else "N/A"
            credit_cost = locale.currency(credit_cost, grouping=True)

            # Generate separate details for state and federal fines
            federal_details = self.generate_details(fed_min_total, fed_max_total, "Federal", fed_reg, fed_viol)
            state_details = self.generate_details(state_min_total, state_max_total, "State", state_reg, state)

            # Display results
            self.output_label.setText(
                f"Federal Fine: Min: {fed_min_total}, Max: {fed_max_total}\n"
                f"State Fine: Min: {state_min_total}, Max: {state_max_total}\n"
                f"Total Calculated Fine: Min: {total_min_fine}, Max: {total_max_fine}\n"
                f"Credit Monitoring Cost: {credit_cost}\n\n"
                f"Details: \n"
                f"{federal_details}\n\n"
                f"{state_details}\n\n"
            )

            # Adjust size of the label to ensure the output is fully displayed
            self.output_label.adjustSize()

        except ValueError:
            self.output_label.setText("Please enter a valid number of records!")
            self.output_label.adjustSize()
        except Exception as e:
            self.output_label.setText(f"Error: {e}")
            self.output_label.adjustSize()

    def generate_details(self, min_fine, max_fine, level, regulation, violation_or_state):
        """
        Generate details for the fines based on whether Min or Max is N/A.
        """
        if min_fine == "N/A" and max_fine == "N/A":
            return (
                f"According to the {level} law of {regulation}, in regards to {violation_or_state}, "
                f"the fines vary case by case."
            )
        elif max_fine == "N/A":
            return (
                f"According to the {level} law of {regulation}, in regards to {violation_or_state}, "
                f"the fine starts from {min_fine} depending on the case."
            )
        elif min_fine == "N/A":
            return (
                f"According to the {level} law of {regulation}, in regards to {violation_or_state}, "
                f"the fine goes up to {max_fine} depending on the case."
            )
        else:
            return (
                f"According to the {level} law of {regulation}, in regards to {violation_or_state}, "
                f"the fine ranges from {min_fine} to {max_fine}."
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataBreachEstimator()
    window.showFullScreen()  # Ensure the application opens in full-screen mode
    sys.exit(app.exec_())




           
