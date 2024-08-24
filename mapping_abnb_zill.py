import pandas as pd
import ast
from image_similarity import generateScore
import csv



def safe_eval(val):
    if pd.isna(val):
        return val  # or return [] if you prefer to have an empty list for NaNs
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError):
        return val 
    

def mapping_func():
    file1 = 'abnb_with_same_distance.csv'
    file2 = 'zill_with_same_distance.csv'

    abnb_df = pd.read_csv(file1)
    zill_df = pd.read_csv(file2)

    #abnb_df['images'] = abnb_df['images'].apply(ast.literal_eval)
    #zill_df['images'] = zill_df['images'].apply(ast.literal_eval)

    abnb_df['images'] = abnb_df['images'].apply(safe_eval)
    zill_df['images'] = zill_df['images'].apply(safe_eval)


    #mapped_index = set()

    # loop over airbnb data
    for index, abnb_row in abnb_df.iterrows():
        image_links_abnb = abnb_row['images']
        
        for zill_index, zill_row in zill_df.iterrows():
            # if row already mapped we will not traverse it
            #if zill_index in mapped_index:
                #continue
            
            image_links_zill = zill_row['images']
            
            count = 0
            # loop over both airbnb and zillow's images links
            for abnb_image in image_links_abnb:
                for zil_image in image_links_zill:
                
                    if generateScore(abnb_image, zil_image) >= 85: # similarity score
                        count += 1
                        print("----image mapped----")
                        if count >= 2:
                            data = [zill_row.get('Listing_link'), abnb_row.get('listing_link'), zill_row.get('Property_address'),
                                    zill_row.get('Rent_price'), zill_row.get('#bedrooms'), 
                                    zill_row.get('#bathrooms'), zill_row.get('Square_footage')]

                            # if give images of airbnb and zillow mapped then store that property's data 
                            with open('mapped_zill_abnb_ScottsDale_data.csv', 'a', newline='') as file:
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
