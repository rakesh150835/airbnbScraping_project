import pandas as pd
import ast
from . image_similarity import generateScore
def map():
    file1 = 'airbnb_data.csv'
    file2 = 'zillow_data.csv'

    abnb_df = pd.read_csv(file1)
    zill_df = pd.read_csv(file2)

    abnb_df['images'] = abnb_df['images'].apply(ast.literal_eval)
    zill_df['images'] = zill_df['images'].apply(ast.literal_eval)


    zill_link = []
    anbn_link = []
    address = []
    zill_rent_price = []
    bedrooms = []
    bathroms = []
    square_footage = []

    mapped_index = set()
    #no_of_img = 0

    # loopin over airbnb images
    for index, abnb_row in abnb_df.iterrows():
        # list of image links of particular property
        image_links_df1 = abnb_row['images']
        
        # looping over zilliow images
        for zill_index, zill_row in zill_df.iterrows():
            if zill_index in mapped_index:
                continue
            
            image_links_df2 = zill_row['images']
            
            count = 0
            for abnb_image in image_links_df1:
                for zil_image in image_links_df2:
                    #no_of_img += 1

                    

                    #print("no of images: ", no_of_img)
                    if generateScore(abnb_image, zil_image) >= 70:
                        count += 1
                        
                        if count >= 5:
                            zill_link.append(zill_row['Listing_link'])
                            anbn_link.append(abnb_row['listing_link'])
                            address.append(zill_row.get('Property_address'))
                            zill_rent_price.append(zill_row.get('Rent_price'))
                            bedrooms.append(zill_row.get('#bedrooms'))
                            bathroms.append(zill_row.get('#bathrooms'))
                            square_footage.append(zill_row.get('Square_footage'))

                            mapped_index.add(zill_index)
                            
                            break
                
                if count >= 5 :
                    break
            if count >= 5 :
                break



    mapped_data = {
            'Zillow rental link': zill_link, 'Airbnb Listing link':        anbn_link, "Address": address, 'Zillow Rent price' : zill_rent_price, 'bedrooms': bedrooms, 
            'bathroms' : bathroms, 'Square footage': square_footage, 
        }

    # to add 'NA' value if data not found 
    max_length = 0
    for values in mapped_data.values():
        max_length = max(max_length, len(values))

    for key, values in mapped_data.items():
        if len(values) < max_length:
            values.extend(['NA']*(max_length - len(values)))

    # create dataframe to save data in csv file
    df = pd.DataFrame(mapped_data)
    df.to_csv('media/mapped_zill_abnb_data.csv', index=False)

    print("airbnb_mapped_liks: ", zill_link)
    print("zill_mapped_image: ", anbn_link)