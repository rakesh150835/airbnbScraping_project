import pandas as pd
import ast
import csv
from geopy.distance import geodesic
import time
from mapping_abnb_zill import mapping_func

def safe_eval(val):
    if pd.isna(val):
        return val  # or return [] if you prefer to have an empty list for NaNs
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError):
        return val 
    
file1 = 'airbnb_data_Scottsdale_latlong.csv'
file2 = 'zillow_data_Scottsdale_latlong.csv'

abnb_df = pd.read_csv(file1)
zill_df = pd.read_csv(file2)

#abnb_df['images'] = abnb_df['images'].apply(ast.literal_eval)
#zill_df['images'] = zill_df['images'].apply(ast.literal_eval)

abnb_df['images'] = abnb_df['images'].apply(safe_eval)
zill_df['images'] = zill_df['images'].apply(safe_eval)

mapped_index = set()

for abnb_index, abnb_row in abnb_df.iterrows():
    lat_abnb = float(abnb_row['latitude']) if not pd.isna(abnb_row['latitude']) else 0.0
    long_abnb = float(abnb_row['longitude']) if not pd.isna(abnb_row['longitude']) else 0.0
    
    abnb_prop = (lat_abnb, long_abnb)
    if abnb_prop == (0.0, 0.0):
        continue

    # write particular property of airbnb to csv for mapping
    abnb_headers = ['property_address', 'listing_link', 'bedrooms', 'bathroms', 'square_footage', 'price', 'listing_description', 'images']
    abnb_data = {'property_address': abnb_row.get('property_address'), 'listing_link': abnb_row.get('listing_link'),
                 'bedrooms': abnb_row.get('bedrooms'), 'bathroms': abnb_row.get('bathroms'), 'square_footage': abnb_row.get('square_footage'), 
                 'price': abnb_row.get('price'), 'listing_description': abnb_row.get('listing_description'), 'images': abnb_row.get('images')}
    
    with open('abnb_with_same_distance.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=abnb_headers)
        writer.writeheader()
        writer.writerow(abnb_data)

    # write headers for zillow's properties
    zill_headers = ['Property_address', 'Listing_link', 'Rent_price', '#bedrooms', '#bathrooms', 'Square_footage', 'images']
    with open('zill_with_same_distance.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=zill_headers)
        writer.writeheader()

    count = 0
    # start looping over zillow csv files
    for zill_index, zill_row in zill_df.iterrows():
        lat_zill = float(zill_row['latitude']) if not pd.isna(zill_row['latitude']) else 0.0
        long_zill = float(zill_row['longitude']) if not pd.isna(zill_row['longitude']) else 0.0

        zill_prop = (lat_zill, long_zill)

        if zill_prop != (0.0, 0.0):
            distance = geodesic(abnb_prop, zill_prop).meters
        else:
            continue
        
        if distance < 50: # if distance between airbnb and zillow property is less than 100 we will map their images for similarity
            print("distance--: ", distance)
            print("airbnb link---: ", abnb_row.get('listing_link'))
            print()
            print("zill index---: ", zill_row.get('Listing_link'))
            print()
            print("---------------------")
            
            count += 1
            # zillow's property's data that has distance less than 100 meter with airbnb's property
            zill_data = [zill_row.get('Property_address'), zill_row.get('Listing_link'),
                    zill_row.get('Rent_price'), zill_row.get('#bedrooms'), zill_row.get('#bathrooms'), 
                    zill_row.get('Square_footage'), zill_row.get('images')]

            with open('zill_with_same_distance.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(zill_data)

    if count >= 1:
        mapping_func()
        print("called mapped function----")
        
    
    