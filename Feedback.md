# Feedback Received

## Design Stage

### Feedback 1
* From: Matt
* Date: 2025-10-07  
**Feedback:**
    ```
    Hey Nick, nice job on your ERD 👍
    You have clearly separated the main entities (companies, ships, docks, bookings, cargo types). It makes the flow easy to follow, and the relationships, especially how bookings connect ships and docks, feel realistic.

    A couple of things you might want to look at:
        •    For dock and cargo type, right now each dock only links to one cargo type. In practice, a dock might handle multiple cargo types, so you could think about a small junction table (e.g. DockCargoTypes) to give it more flexibility. For example, one dock might be set up for both container ships and oil tankers.
        •    The bookings table is solid, but maybe consider adding a status column (e.g. using an ENUM like pending, confirmed, cancelled). That would make it more practical for CRUD operations since a booking can move through different stages.
        •    One thing I noticed is that in your text description you call it booking_duration, but in the table it is written as booking_hours. Just checking if those are meant to be the same field. 
    Overall though it is a really strong design and it is clear how it would translate into API endpoints. Nice work 👌
    ```
    **Actions:**
    1. Created Junction table for Docks & Cargo Types
    2. Added booking_status to Bookings table
    3. Clarified booking_hours as column name

    <hr>
### Feedback 2
* From: Josh
* Date: 2025-10-07  
**Feedback:**
    ```
    Hey Nick,
    This looks good. Just a few things to make managing your data easier.

    I would change cargo_types to cargo with cargo_types removed from the ships table and into the shipment_bookings junction table (this can be the same bookings table). 

    The ships table can be made more atomic and not be tied to the comings and goings of cargo containers. Ships can contain many cargo containers and not necessarily the same type. The ship data will be easier to manage as containers are always moving on and off the ship.

    The same with the docks table. This can also be a junction table called docked_cargo, using the dockID and cargoID as foreign keys.
    ```
    **Actions:**
    1. Retained current Ships table structure - cargo type is a property of the ship for this implementation where cargo types would be e.g. container ship, oil tanker, vehicle carrier, etc.
    Since these are broad cargo types and dependant on the structure of the ship itself, they would not be expected to change for the ships lifetime.
    2. Junction table has now been implemented between Docks and Cargo Types.

    <hr>

### Feedback 3
* From: Lillie
* Date: 2025-10-08  
**Feedback:**
    ```
    A solid ERD! There is clear entity relationships, well defined and descriptive names. Everything makes sense from a real world perspective.

    Suggestions:

    cargo_types = cargo_name and could include: max_weight, hazard_level, description.

    ships could also include: capacity, year_built, country_of_origin.

    shipping_companies could also include: email, phone, address.

    is it best practice to name entities/tables singularly?

    Do ships have only one cargo type? Or would they carry many different cargo types? Are we talking big ships that have lots of containers of different things or is it ships that only transport one exact thing?
    ```
    **Actions:**
    1. Retained current columns in Cargo_Types table, as cargo types are broad categories (e.g. container ship, oil tanker, vehicle carrier) rather than specific cargo items.
    2. Added country of origin to Ships table, other suggested columns not implemented as they are not required for this implementation.
    3. Added suggested columns to Shipping_Companies table.
    4. Re. questions:
        * Tables are named in plural as they contain multiple records (The API implementation will use singular for the model names)
        * Ships will have a single cargo type as a broad category, as explained above.

    <hr>

## Design Stage

### Feedback 1
* From: Matt
* Date: 2025-10-23  
**Feedback:**
    ```
    hey nick , nice shipping api 😁
    after taking a look i noticed: 
    1. right now in ship_routes.py the update route is letting you change ship_id, but that’s the primary key and shouldn’t be editable. instead, it should allow updates to company_id, so admins can move a ship to a different company. swapping ship_id for company_id in the allowed updates would fix this.
    2. in  booking_routes.py, if booking_start is missing or blank the code still tries to parse it with datetime.strptime, which gives you a 500 err. add a simple check before parsing so it throws a BodyError and returns a clean 400 instead.
    otherwise looks great !
    ```
    **Actions:**
    1. Fixed `ship_routes.py` issue, changed ship_id to company_id in allowed update fields.
    2. Fixed potential error in `booking_routes.py` by raising BodyError before attempting to parse datetime strings.

    <hr>