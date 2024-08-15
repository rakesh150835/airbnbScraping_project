import pandas as pd
import ast
from image_similarity import generateScore
import csv


HF_HOME='C:\\Users\\DELL\\.cache\\huggingface'

file1 = 'airbnb_data.csv'
file2 = 'zillow_data.csv'

abnb_df = pd.read_csv(file1)
zill_df = pd.read_csv(file2)

abnb_df['images'] = abnb_df['images'].apply(ast.literal_eval)
zill_df['images'] = zill_df['images'].apply(ast.literal_eval)


mapped_index = set()


with open('mapped_zill_abnb_data.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(['zill_listing_link', 'abnb_listing_link', 'Property_address', 'Rent_price', '#bedrooms', '#bathrooms', 'Square_footage'])

    # Iterate over csv files
    for index, abnb_row in abnb_df.iterrows():
        image_links_df1 = abnb_row['images']
        

        for zill_index, zill_row in zill_df.iterrows():
            if zill_index in mapped_index:
                continue
            
            image_links_df2 = zill_row['images']
            
            count = 0
            for abnb_image in image_links_df1:
                for zil_image in image_links_df2:

                    if generateScore(abnb_image, zil_image) >= 70:
                        count += 1
                        
                        if count >= 5:
                            mapped_data = [zill_row.get('Listing_link'), abnb_row.get('listing_link'), zill_row.get('Property_address'), zill_row.get('Rent_price'), zill_row.get('#bedrooms'), zill_row.get('#bathrooms'), zill_row.get('Square_footage')]

                            writer.writerow(mapped_data)

                            mapped_index.add(zill_index)
                            
                        break
                
                if count >= 5:
                    break
            if count >= 5:
                break

    

