import pandas as pd
import ast
import csv
from geopy.distance import geodesic
import time
import pandas as pd
import ast
from . image_similarity import generateScore
import csv


# function to handle 'NA' values in csv file
def safe_eval(val):
    if pd.isna(val):
        return val  # or return [] if you prefer to have an empty list for NaNs
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError):
        return val 

# create final mapping file of properties 
mapping_file_headers = ['Zillow_Listing_link', 'airbnb_listing_link', 'Property_address',
                        'Rent_price', '#bedrooms', '#bathrooms', 'Square_footage']
with open('media/mapped_zill_abnb_data.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=mapping_file_headers)
    writer.writeheader()


# check similarity between images of shortlist properties
def map_shortlist_properties():
    file1 = 'abnb_with_same_distance.csv'
    file2 = 'zill_with_same_distance.csv'

    abnb_df = pd.read_csv(file1)
    zill_df = pd.read_csv(file2)

    abnb_df['images'] = abnb_df['images'].apply(safe_eval)
    zill_df['images'] = zill_df['images'].apply(safe_eval)
    

    #mapped_index = set()

    # loop over shortlist airbnb data
    for index, abnb_row in abnb_df.iterrows():
        image_links_abnb = abnb_row['images']
        
        # loop over shortlist zillow data
        for zill_index, zill_row in zill_df.iterrows():
            # if row already mapped we will not traverse it
            #if zill_index in mapped_index:
                #continue
            
            image_links_zill = zill_row['images']
            
            count = 0
            # loop over both airbnb and zillow's images links
            for abnb_image in image_links_abnb:
                for zil_image in image_links_zill:
                
                    if generateScore(abnb_image, zil_image) >= 77: # similarity score
                        count += 1
                        print("----image mapped----")
                        if count >= 2:
                            data = [zill_row.get('Listing_link'), abnb_row.get('listing_link'), zill_row.get('Property_address'),
                                    zill_row.get('Rent_price'), zill_row.get('#bedrooms'), 
                                    zill_row.get('#bathrooms'), zill_row.get('Square_footage')]

                            # if give images of airbnb and zillow mapped then store that property's data 
                            with open('media/mapped_zill_abnb_data.csv', 'a', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(data)

                                # store mapped index so that we don't need to traverse again
                                #mapped_index.add(zill_index)

                            print("---mapped image link---")
                            print("zillow link: ", zill_row['Listing_link'])
                            print("airbnb link: ", abnb_row['listing_link'])
                            
                        break
                
                if count >= 2:
                    break
            if count >= 2:
                break

def map():
    # start shortlisting and then mapping from here
    file1 = 'airbnb_data.csv'
    file2 = 'zillow_data.csv'

    abnb_df = pd.read_csv(file1)
    zill_df = pd.read_csv(file2)

    abnb_df['images'] = abnb_df['images'].apply(safe_eval)
    zill_df['images'] = zill_df['images'].apply(safe_eval)

    # creating file to store properties if distance is less than 20 meter
    zill_headers = ['Property_address', 'airbnb_listing_link', 'Zill_listing_link', 'Rent_price', '#bedrooms', '#bathrooms', 'Square_footage']
    with open('media/shortlist_properties_under_20_meter.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=zill_headers)
        writer.writeheader()


    # shortlisting of properties starts here
    for abnb_index, abnb_row in abnb_df.iterrows():
        lat_abnb = float(abnb_row['latitude']) if not pd.isna(abnb_row['latitude']) else 0.0
        long_abnb = float(abnb_row['longitude']) if not pd.isna(abnb_row['longitude']) else 0.0
        
        abnb_prop = (lat_abnb, long_abnb)
        if abnb_prop == (0.0, 0.0):
            continue
        
        # airbnb's property's data for mapping
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

        num = 0
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
                print("zill index---: ", zill_row.get('Listing_link'))
                print("---------------------")
                
                num += 1 # count how many properties are under particular distance to call maping function

                # zillow's property's data that has distance less than 50 meter with airbnb's property
                zill_data = [zill_row.get('Property_address'), zill_row.get('Listing_link'),
                        zill_row.get('Rent_price'), zill_row.get('#bedrooms'), zill_row.get('#bathrooms'), 
                        zill_row.get('Square_footage'), zill_row.get('images')]

                with open('zill_with_same_distance.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(zill_data)

                # store properties that are under 20 meter distance
                if distance <= 20:
                    zill_data.pop()
                    zill_data.insert(1, abnb_row.get('listing_link'))
                    with open('media/shortlist_properties_under_20_meter.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(zill_data)

        if num >= 1: # call map function only if there is atleast one property under 50 meter distance
            map_shortlist_properties()
            print("called mapped function----")
        
    
    