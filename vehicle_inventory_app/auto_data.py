from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

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
    image_path = Column(String)
# Create table in the database
Base.metadata.create_all(engine)

# Function to add a new vehicle record
def add_vehicle(year, make, model, vin_number, miles, image_path=None):
    Session = sessionmaker(bind=engine)
    session = Session()
    vehicle = Vehicle(year=year, make=make, model=model, vin_number=vin_number, miles=miles,image_path=image_path)
    session.add(vehicle)
    session.commit()
    session.close()
    

# Function to update an existing vehicle record
def update_vehicle(vehicle_id, year=None, make=None, model=None, vin_number=None, miles=None,image_path=None, delete_image=False):
    Session = sessionmaker(bind=engine)
    session = Session()
    vehicle = session.query(Vehicle).filter_by(id=vehicle_id).first()
    
    if vehicle:
        # Update vehicle fields
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

        # Handle image updates
        if delete_image:  # If delete_image flag is set
            current_image_path = f"images/{vehicle.id}.jpg"
            if os.path.exists(current_image_path):  # Check if the image file exists
                os.remove(current_image_path)  # Delete the file
            vehicle.image_path = None  # Update database to reflect no image

        elif image_path:
            vehicle.image_path = image_path  # Update with the new image path

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
