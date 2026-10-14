# Smart Table Management System

## Project Overview

Smart Table Management System is a web-based application designed to simplify customer interactions at restaurant tables. Customers can browse the menu, place orders, request assistance, and view their bill through a simple interface.

## Features

- Home page with three main options.
- Digital menu with food items and prices.
- Interactive cart with quantity controls and automatic total calculation.
- Order confirmation with a unique order reference.
- Help request form for customer assistance.
- Bill page displaying saved order details.
- Demo payment options for UPI and cash.
- SQLite database for storing orders and help requests.
- Automated tests using pytest and Selenium.

## Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- SQLite
- pytest
- Selenium
- Git and GitHub

## Project Structure

```text
SmartTableManagement/
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
├── static/
│   ├── style.css
│   └── script.js
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── menu.html
│   ├── help.html
│   ├── bill.html
│   └── confirmation.html
└── tests/
    ├── test_app.py
    └── test_selenium.py
```

## Requirements

- Python 3
- Google Chrome
- Visual Studio Code (recommended)

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/shreeyamahabaleshwarkar-hub/Smart-Table-Management-System.git
```

### 2. Navigate to the Project Folder

```bash
cd Smart-Table-Management-System
```

### 3. Create a Virtual Environment

```powershell
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### 6. Run the Application

```powershell
python app.py
```

### 7. Open the Website

Open the following address in your browser:

http://127.0.0.1:5000

The application initializes the SQLite database and stores orders and assistance requests locally.

## Testing

Run the automated tests using:

```powershell
python -m pytest -v
```

Ensure the Flask application is running before executing the Selenium browser tests.

## Payment Disclaimer

The payment functionality is for demonstration purposes only. No real payments are processed.

## Project Scope

This project focuses on the customer-facing restaurant table interface. Kitchen management, staff dashboards, and real payment gateway integration are outside the current scope.
