# Senior-Project---CYBR-4350

# Data Breach Impact Estimator

The **Data Breach Impact Estimator** is a PyQt5-based desktop application designed to help users estimate fines and costs associated with data breaches at both the state and federal levels. The tool leverages data from an Excel file and provides an interactive interface for calculations based on user inputs.

---

## Features
- **Interactive GUI**: Built with PyQt5, providing a clean and responsive interface.
- **State and Federal Regulations**: Incorporates state and federal laws for precise calculations.
- **Dropdown Selection**:
  - Choose from various states and regulations.
  - Update options dynamically based on user input.
- **Cost Estimation**:
  - Calculates minimum and maximum fines for data breaches.
  - Includes credit monitoring costs based on the number of breached records.
- **Detailed Output**:
  - Displays fine breakdowns for both state and federal levels.
  - Provides additional context based on selected laws and violations.

---

## Installation

### Prerequisites
1. Python 3.8 or higher
2. Required Python libraries:
   - `pandas`
   - `numpy`
   - `PyQt5`
3. An Excel file named `Blen_Asmare_Project_draft.xlsx` containing:
   - **State Regulations** sheet
   - **Federal Regulations** sheet

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Data-Breach-Impact-Estimator.git
