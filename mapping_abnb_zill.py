import pandas as pd
import ast
from image_similarity import generateScore
import csv


HF_HOME='C:\\Users\\DELL\\.cache\\huggingface'

file1 = 'zillow_data.csv'
file2 = 'zillow_data.csv'

abnb_df = pd.read_csv(file1)
zill_df = pd.read_csv(file2)

abnb_df['images'] = abnb_df['images'].apply(ast.literal_eval)
zill_df['images'] = zill_df['images'].apply(ast.literal_eval)


mapped_index = set()
no_of_img = 0

for index, abnb_row in abnb_df.iterrows():
    image_links_df1 = abnb_row['images']
    
    if no_of_img >= 100:
        break

    for zill_index, zill_row in zill_df.iterrows():
        if zill_index in mapped_index:
            continue
        
        image_links_df2 = zill_row['images']
        
        count = 0
        for abnb_image in image_links_df1:
            for zil_image in image_links_df2:
                no_of_img += 1
                
                print("No of images: ", no_of_img)

                if no_of_img >= 100:
                    break

                if generateScore(abnb_image, zil_image) >= 70:
                    count += 1
                    
                    if count >= 5:
                        mapped_data = [zill_row.get('Listing_link'), abnb_row.get('Listing_link'), zill_row.get('Property_address'), zill_row.get('Rent_price'), zill_row.get('#bedrooms'), zill_row.get('#bathrooms'), zill_row.get('Square_footage')]

                        # change anbnb listing link
                        print(mapped_data)
                        with open('mapped_zill_abnb_data.csv', mode='a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(mapped_data)

                        mapped_index.add(zill_index)
                        
                    break
            
            if count >= 5 or no_of_img >= 100:
                break
        if count >= 5 or no_of_img >= 100:
            break



