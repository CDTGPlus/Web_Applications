from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create SQLite database engine
engine = create_engine('sqlite:///vehicles.db', echo=True)

# Create base class for declarative class definitions
Base = declarative_base()

# Define Vehicle class representing the 'vehicle' table
class Vehicle(Base):
    __tablename__ = 'vehicle'

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    make = Column(String)
    model = Column(String)
    vin_number = Column(String)
    miles = Column(Integer)

# Create table in the database
Base.metadata.create_all(engine)

# Function to add a new vehicle record
def add_vehicle(year, make, model, vin_number, miles):
    Session = sessionmaker(bind=engine)
    session = Session()
    vehicle = Vehicle(year=year, make=make, model=model, vin_number=vin_number, miles=miles)
    session.add(vehicle)
    session.commit()
    session.close()

# Function to update an existing vehicle record
def update_vehicle(vehicle_id, year=None, make=None, model=None, vin_number=None, miles=None):
    Session = sessionmaker(bind=engine)
    session = Session()
    vehicle = session.query(Vehicle).filter_by(id=vehicle_id).first()
    if vehicle:
        if year:
            vehicle.year = year
        if make:
            vehicle.make = make
        if model:
            vehicle.model = model
        if vin_number:
            vehicle.vin_number = vin_number
        if miles:
            vehicle.miles = miles
        session.commit()
    session.close()

# Function to delete a vehicle record
def delete_vehicle(vehicle_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    vehicle = session.query(Vehicle).filter_by(id=vehicle_id).first()
    if vehicle:
        session.delete(vehicle)
        session.commit()
    session.close()

#Function to search vehicle based on multople criteria
def search_vehicle(vehicle_id=None, year=None, make=None, model=None, vin_number=None, miles=None):
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Vehicle)
    if vehicle_id:
        query = query.filter(Vehicle.id == vehicle_id)
    if year:
        query = query.filter(Vehicle.year == year)
    if make:
        query = query.filter(Vehicle.make == make)
    if model:
        query = query.filter(Vehicle.model == model)
    if vin_number:
        query = query.filter(Vehicle.vin_number == vin_number)
    if miles:
        query = query.filter(Vehicle.miles == miles)
    # Execute query
    results = query.all()
    session.close()
    
    return results

# Function to select vehicle by ID
def select_vehicle(vehicle_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    vehicle = session.query(Vehicle).filter_by(id=vehicle_id).first()
    session.close()
    return vehicle

# Example usage:
# add_vehicle(2021, 'Toyota', 'Camry', 'ABC123', 5000)
# update_vehicle(1, miles=6000)
# delete_vehicle(1)
