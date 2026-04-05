🏥 Hospital Management & Pharmacy System (HMS)
This repository contains multiple versions of a Hospital Management System and a dedicated Pharmacy Inventory module. The project demonstrates the evolution of the system from a basic entry form to an advanced version with automated features and a professional UI.

📂 Project Structure & Versions
The project is divided into different versions, each adding more advanced functionality:

hospital.py to hospital2.py: Initial versions focusing on basic patient data entry and database connectivity.

hospital3.py (Latest Version): The most advanced version featuring:

Auto-Increment Logic: Automatically calculates the next Reference No and NHS Number (Last Value + 1).

Smart Dropdowns: Replaced manual typing with Combobox for Doses (1 to 4 tablets), No. of Tablets, and Daily Dosage.

Professional UI: Improved grid alignment for a clean and symmetrical look.

inventry.py: A dedicated Pharmacy Inventory system to manage medicine stock, HSN codes, rack numbers, and expiry dates.

✨ Key Features
🏥 Hospital Management Features
Admin Login System: Secure access to the dashboard.

Automated Reference Numbers: No need to remember the last ID; the system fetches the latest ID from MySQL and adds 1.

Prescription & Billing: Generates a text-based bill that can be printed instantly.

Flexible Dosage Options: Dropdown menus for "1 Tablet", "2 Tablets", etc., and "As Needed" options.

Database Integration: Real-time Sync with MySQL for all patient records.

💊 Pharmacy Inventory Features
Stock Tracking: Manage medicine names, company, and category.

Warehouse Logistics: Track Rack Numbers, Batch Numbers, and HSN Codes.

Expiry Management: Integrated tkcalendar for accurate expiry date selection.

Price Management: Fields for MRP, Price per Unit, and Tax percentages.

🛠️ Tech Stack
Language: Python 3.x

Database: MySQL Server

Libraries: Tkinter, tkcalendar, mysql-connector-python.

📋 Installation & Setup
Install Dependencies:

Bash
pip install mysql-connector-python tkcalendar
Database Configuration:

Create a database named hospital_db.

Create tables hospital and medicines.

Note: Update the database credentials (User & Password) in the connection string within each .py file.

How to Run:

To see the latest Hospital features: python hospital3.py

To manage Medicine Stock: python inventry.py

📄 License
This project is open-source and available under the MIT License.

How to Push this to GitHub:
Save this text as README.md in your D:\Project\H M S folder.

=========================================================================================Database=====================================================================================

🗄️ Database Architecture & Relations
The system is powered by a relational database (hospital_db) consisting of three interconnected tables. Here is how they work together:

1. users Table (Authentication Layer)
This is the security gatekeeper of the application.

Role: Stores administrative credentials (usernames and passwords).

Connection: Every time a user launches hospital.py or inventry.py, the system queries this table to verify the login. Access to the patient and medicine data is only granted after a successful match.

2. medicines Table (Inventory Master Data)
This serves as the "Source of Truth" for all pharmaceutical products.

Role: Stores comprehensive details for each medicine, including HSN Codes, Rack Numbers, Batch IDs, Expiry Dates, and Unit Prices.

Data Flow: The hospital3.py module fetches the list of available medicines from this table to populate the dropdown menus. When a medicine is selected, the system pulls the Price per Unit and Rack Location from here to calculate the final bill.

3. hospital Table (Transaction & Patient Records)
This is the primary storage for patient history and prescriptions.

Role: Stores patient-specific information such as NHS Numbers, Reference IDs, and Addresses, along with the specific dosage prescribed.

Connection: It records which medicine was issued by linking the med_name from the medicines table to the patient's record. This allows the hospital to track which patient received which batch of medicine.

🟢 Logical Data Flow
Authorize: User validates identity via the users table.

Fetch: The system populates the UI by pulling medicine names from the medicines table.

Process: The system calculates the bill by multiplying the stock_qty from the user input with the price_per_unit from the medicines table.

Commit: All patient details, including the selected medicine and auto-generated Ref/NHS numbers, are saved into the hospital table for future reference.
Open your VS Code Terminal and run:

Bash
git add .
git commit -m "Added detailed README with version history"
git push origin main
