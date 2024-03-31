import streamlit as st
import pandas as pd
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from auto_data import *


# Create SQLite database engine
engine = create_engine('sqlite:///vehicles.db', echo=True)

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
        df = pd.DataFrame([(v.id, v.year, v.make, v.model, v.vin_number, v.miles) for v in vehicles],
                          columns=['ID', 'Year', 'Make', 'Model', 'VIN Number', 'Miles'])
        st.dataframe(df)
    else:
        st.write('No vehicles found.')


# Streamlit app
def main():
    st.set_page_config(page_title='Vehicle Management System', page_icon=':car:')
    st.title('Vehicle Management System')

    # Sidebar menu
    menu_selection = st.sidebar.radio('Menu', ['Enter New Vehicle Data', 'View Data'])
    current_year = datetime.datetime.now().year
    if menu_selection == 'Enter New Vehicle Data':
        st.subheader('Enter New Vehicle Data')
        year = st.number_input('Year', min_value=1900, max_value=9999, value=current_year)
        make = st.text_input('Make')
        model = st.text_input('Model')
        vin_number = st.text_input('VIN Number')
        miles = st.number_input('Miles', min_value=0)

        if st.button('Add Vehicle'):
            add_vehicle(year, make, model, vin_number, miles)
            st.success('Vehicle added successfully.')

    elif menu_selection == 'View Data':

        option = st.selectbox('Select Extra Options',('View All','Search','Edit','Delete'))

        if option == 'View All':
            st.subheader('View Vehicle Data')
            display_vehicle_data(fetch_all_vehicle_data())

        elif option == 'Search':
            
            vehicle_id = st.number_input('Vehicle ID')
            year = st.number_input('Year')
            make = st.text_input('Make')
            model = st.text_input('Model')
            vin_number = st.text_input('VIN Number')
            miles = st.number_input('Miles')
            search_result = st.button('Search Database')
            swt = 0
            #switch button state 
            if search_result:
                swt = 1
            if swt == 1:
                search = search_vehicle(vehicle_id,year,make,model,vin_number,miles)
                if search:
                    st.success('Vehicles found: '+str(len(search)))
                    display_vehicle_data(search)
                else:
                    st.warning('No results found based on parameters')
                swt = 0


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
