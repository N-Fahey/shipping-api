# Shipping-API
**Nick Fahey | 2025-JUN**  
https://github.com/N-Fahey/shipping-api  
Coder Academy DEV1002 Assignment 3: Web API Server

## Description
A RESTful web API built with Flask, SQLAlchemy & Marshmallow for managing bookings of ships into a freight terminal.  

## Requirements
* Windows, Linux or Mac
* PostgreSQL server with a configured user & database
* Python 3.10 or greater
* External libraries (see requirements.txt list)

## Installation
1. **[Install Python](https://www.python.org/about/gettingstarted/) on your Windows, Mac, or Linux machine**
2. **Clone the repo**
    ```
    git clone git@github.com:N-Fahey/shipping-api.git\
    cd shipping-api
    ```
3. **Create Python virtual environment**
    ```
    python3 -m venv .venv
    ```
4. **Activate the virtual enviroment**  
    Windows:
    ```
    .venv\Scripts\activate.bat
    ```
    Linux/Mac:  
    ```
    source .venv/bin/activate
    ```
5. **Install dependencies**
    ```
    pip install -r requirements.txt
    ```
6. **Define environment variables**  
    Create .env file by copying default:
    ```
    cp .env.example .env
    ```
    Open .env file with any text editor, and update the following variables with your PostgreSQL credentials:
    ```
    DB_USER=username
    DB_PASSWORD=password
    DB_HOST=localhost:5432
    DB_NAME=database_name
    ```
7. **Populate database**
    ```
    flask db create
    ```
    Optionally, seed demo data:
    ```
    flask db seed
    ```
8. **Launch the app**
    ```
    flask run
    ```

## API Reference

All endpoints are prefixed with `/api/v1`.

### Company
- `POST /company/CreateCompany` — Create a new company
- `GET /company/<company_id>` — Get a company by ID
- `GET /company/GetAllCompanies` — List all companies
- `PUT/PATCH /company/UpdateCompany/<company_id>` — Update a company
- `DELETE /company/DeleteCompany/<company_id>` — Delete a company

### Cargo
- `POST /cargo/CreateCargo` — Create a new cargo type
- `GET /cargo/GetCargoTypes` — List all cargo types
- `DELETE /cargo/DeleteCargo/<cargo_id>` — Delete a cargo type

### Ship
- `POST /ship/CreateShip` — Create a new ship
- `GET /ship/<ship_id>` — Get a ship by ID
- `GET /ship/GetAllShips` — List all ships
- `PUT/PATCH /ship/UpdateShip/<ship_id>` — Update a ship
- `DELETE /ship/DeleteShip/<ship_id>` — Delete a ship

### Dock
- `POST /dock/CreateDock` — Create a new dock
- `GET /dock/<dock_id>` — Get a dock by ID
- `GET /dock/GetAllDocks` — List all docks
- `PUT/PATCH /dock/UpdateLength/<dock_id>` — Update dock length
- `PUT/PATCH /dock/UpdateCargo/<dock_id>` — Update dock cargo types
- `DELETE /dock/DeleteDock/<dock_id>` — Delete a dock

### Booking
- `POST /booking/CreateBooking` — Create a new booking
- `GET /booking/<booking_id>` — Get a booking by ID
- `GET /booking/GetAllBookings` — List all bookings (filterable)
- `PUT/PATCH /booking/UpdateBooking/<booking_id>` — Update a booking
- `DELETE /booking/DeleteBooking/<booking_id>` — Delete a booking

See each route's docstring for required parameters and request body details.
