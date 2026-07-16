# MediCare Pro — Hospital Management System

A desktop Hospital Management System built in Python using Tkinter, featuring a 
modern sidebar-based dashboard, secure authentication, live data visualizations, 
and full patient/doctor/appointment/billing management — all with persistent 
JSON-based storage.

## Features

### Authentication
- Sign Up / Login system with multiple user accounts (stored securely in JSON)
- Clean, card-based login UI with a splash screen on startup

### Dashboard
- Real-time stats: total patients, doctors, appointments, and revenue collected
- Live revenue chart (line graph) built with Matplotlib
- Doctor specialization breakdown (pie chart)
- Recent appointments table
- Quick Action shortcuts for common tasks

### Patient Management
- Add, search, edit, and delete patient records (name, age, disease)

### Doctor Management
- Add and remove doctor records with specialization

### Appointment Booking
- Book appointments by linking a patient with a doctor
- Set consultation fees per appointment

### Billing
- Track appointment payment status
- Mark appointments as paid
- View total revenue collected in real time

## Tech Stack
- Python
- Tkinter (GUI)
- Matplotlib (data visualization, embedded via FigureCanvasTkAgg)
- JSON (data persistence)

## Files
- `hospital_dashboard.py` — main application (GUI, dashboard, all features)
- `hospital_data.json` — stores all patients, doctors, appointments, and user 
  accounts; auto-generated with sample data on first run

## How to Run
1. Install dependencies
 2. Run the application
 3. Sign up for a new account, or use the default admin login (if sample data is 
   present)
4. Explore the dashboard, manage patients/doctors, book appointments, and track 
   billing

## Key Highlights
- Clean blue-and-white medical UI design with a card-based layout
- Sidebar navigation for smooth switching between modules
- Data visualizations give the dashboard real analytical value, not just static 
  numbers
- Fully persistent — all data is saved automatically and reloaded on the next run

## Future Improvements
- Role-based access (Admin, Doctor, Patient views)
- Appointment date/time scheduling with calendar view
- Exportable billing receipts (PDF)
- Migration from JSON storage to a proper database (SQLite/MySQL)
