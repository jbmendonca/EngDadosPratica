# Visitor Management System for Sebrae Roraima

This is a simple Flask application to register visitors, manage users and generate a visitor badge with QRCode.

## Requirements
- Python 3.8+
- Microsoft SQL Server 2022
- The packages listed in `requirements.txt`

## Running
1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure the connection string in `app.py` with your SQL Server credentials.
3. Create the database tables running the SQL script `schema.sql` on your database.
4. Start the application:
   ```bash
   python app.py
   ```
5. Access `http://localhost:5000` in your browser.

## Users and Roles
- **Administrador**: full access to user management
- **Gerente**: can register visitors and view reports
- **Recepcionista**: register visitors only

## Features
- Visitor registration form with name, CPF, phone and destination sector
- QRCode generation and badge printing
- User authentication with roles

This project is a template and may require adjustments for production use.
