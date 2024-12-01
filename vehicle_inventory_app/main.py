import streamlit as st
import pandas as pd
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from auto_data import *
import os




# Create SQLite database engine
engine = create_engine('sqlite:///vehicles.db', echo=True)
# Create path for images
if not os.path.exists("images"):
    os.makedirs("images")

# Function to fetch vehicle data from the database
def fetch_all_vehicle_data():
    Session = sessionmaker(bind=engine)
    session = Session()
    vehicles = session.query(Vehicle).all()
    session.close()
    return vehicles

# Function to display vehicle data
def display_vehicle_data(fetch):
    # vehicles = fetch_vehicle_data()
    vehicles = fetch
    if vehicles:
        # Display the vehicle data in a table with "View" buttons
        for vehicle in vehicles:
            col1, col2 = st.columns([3, 1])  # Adjust column proportions for data and button
            with col1:
                st.write(f"**ID:** {vehicle.id}, **Year:** {vehicle.year}, **Make:** {vehicle.make}, "
                        f"**Model:** {vehicle.model}, **VIN:** {vehicle.vin_number}, **Miles:** {vehicle.miles}")
            with col2:
                
                toggle_key = f"toggle_image_{vehicle.id}"

                # Initialize the toggle state in session_state if not present
                if toggle_key not in st.session_state:
                    st.session_state[toggle_key] = False

                # Create a "View" button for the vehicle
                if st.button(f"View Image for Vehicle ID {vehicle.id}", key=f"view_{vehicle.id}"):
                    # Toggle the state
                    st.session_state[toggle_key] = not st.session_state[toggle_key]

                # Check if the image should be displayed
                if st.session_state[toggle_key]:
                    image_path = get_image_path(vehicle.id)
                    if image_path:
                        st.image(image_path, caption=f"Image for Vehicle ID {vehicle.id}", use_container_width=True)
                    else:
                        st.warning(f"No image available for Vehicle ID {vehicle.id}")
    else:
        st.write('No vehicles found.')
    

# Function to fetch the image path for a vehicle
def get_image_path(vehicle_id):
    image_path = f"images/{vehicle_id}.jpg"  # Assuming images are stored as <vehicle_id>.jpg
    return image_path if os.path.exists(image_path) else None


# Streamlit app
def main():
    st.set_page_config(page_title='Vehicle Management System', page_icon=':car:')
    st.title('Vehicle Management System')

    menu_selection = st.sidebar.radio('Menu', ['Enter New Vehicle Data', 'View Data'])
    current_year = datetime.datetime.now().year

    if menu_selection == 'Enter New Vehicle Data':
        st.subheader('Enter New Vehicle Data')
        year = st.number_input('Year', min_value=1900, max_value=9999, value=current_year)
        make = st.text_input('Make')
        model = st.text_input('Model')
        vin_number = st.text_input('VIN Number')
        miles = st.number_input('Miles', min_value=0)
        image_file = st.file_uploader("Upload Vehicle Image (Optional)", type=["jpg", "jpeg", "png"])

        if st.button('Add Vehicle'):
            # Add vehicle to the database first
            add_vehicle(year, make, model, vin_number, miles)

            # Fetch the last inserted vehicle ID
            Session = sessionmaker(bind=engine)
            session = Session()
            last_vehicle = session.query(Vehicle).order_by(Vehicle.id.desc()).first()
            session.close()

            if image_file:
                # Save the uploaded image with the vehicle ID
                image_path = f"images/{last_vehicle.id}.jpg"
                with open(image_path, "wb") as f:
                    f.write(image_file.read())
            
            st.success(f'Vehicle added successfully. ID: {last_vehicle.id}')

    
    elif menu_selection == 'View Data':

        option = st.selectbox('Select Extra Options',('View All','Search','Edit','Delete'))

        if option == 'View All':
            st.subheader('View Vehicle Data')
            display_vehicle_data(fetch_all_vehicle_data())


        elif option == 'Search':
            # Search criteria inputs
            vehicle_id = st.number_input('Vehicle ID', value=0)
            year = st.number_input('Year', value=0)
            make = st.text_input('Make')
            model = st.text_input('Model')
            vin_number = st.text_input('VIN Number')
            miles = st.number_input('Miles', value=0)
            
            # Use session state to preserve search results
            if "search_results" not in st.session_state:
                st.session_state["search_results"] = []

            if st.button('Search Database'):
                search = search_vehicle(
                    vehicle_id=vehicle_id if vehicle_id else None,
                    year=year if year else None,
                    make=make if make else None,
                    model=model if model else None,
                    vin_number=vin_number if vin_number else None,
                    miles=miles if miles else None
                )
                if search:
                    st.session_state["search_results"] = search
                    st.success(f"Vehicles found: {len(search)}")
                else:
                    st.session_state["search_results"] = []
                    st.warning('No results found based on parameters')

            # Display search results
            if st.session_state["search_results"]:
                display_vehicle_data(st.session_state["search_results"])



        elif option == 'Edit':
            vehicle_id = st.text_input('Enter Vehicle ID')       
                    
            vehicle = select_vehicle(int(vehicle_id)) if vehicle_id else None

            # Display vehicle attributes in input fields
            if vehicle:
                
                st.subheader('Current Vehicle Data')
                st.write(f'ID: {vehicle.id}')
                year = st.text_input('Year', value=str(vehicle.year))
                make = st.text_input('Make', value=vehicle.make)
                model = st.text_input('Model', value=vehicle.model)
                vin_number = st.text_input('VIN Number', value=vehicle.vin_number)
                miles = st.text_input('Miles', value=str(vehicle.miles))

                confirm_update = st.button('Confirm Update')

                if confirm_update:

                    update_vehicle(int(vehicle_id), year, make, model, vin_number, miles)
                    st.success('Vehicle updated successfully.')
                    # st.experimental_rerun()
            else:
                st.warning('Vehicle not found. Please enter a valid Vehicle ID.')
                    
                    
        elif option == 'Delete':
            vehicle_id_del = st.text_input('Enter Vehicle ID')
            vehicle = select_vehicle(int(vehicle_id_del)) if vehicle_id_del else None
            if vehicle:
                confirm_deletion = st.button('Confirm Deletion')
                if confirm_deletion:
                    delete_vehicle(int(vehicle_id_del))
                    st.success('Vehicle deleted successfully.')
                    # st.experimental_rerun()
            else:
                st.warning('Vehicle not found. Please enter a valid Vehicle ID.')
#run main
if __name__ == '__main__':
    main()
