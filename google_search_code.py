import csv
import time
from serpapi import GoogleSearch
from datetime import datetime, timedelta
import gobnb
from image_similarity import generateScore


# client SerpAPI key
#SERPAPI_KEY = "782a74addaa027329ee50918a806476f7f21aea50e10c4f0d424d6db1f7ee518"

#personal SerpAPI key
SERPAPI_KEY = "c9058c0614bd0d61f21305be68720e3d9cd40b3f08d935eac819a309074cfc37"

# Max searches per hour
MAX_SEARCHES_PER_HOUR = 5900
# Max images per property (updated to 20)
MAX_IMAGES_PER_PROPERTY = 20

def get_images_links(self, room_url):
        currency="USD"
        check_in = ""
        check_out = ""
        data = gobnb.Get_from_room_url(room_url,currency,check_in,check_out,"")

        # get images links 
        images = data.get('images', [])

        image_links = []
        print(f"num of images: {len(images)}")
        for image in images:
            if image.get('url', None) != None:
                image_links.append(image.get('url'))

        return image_links
    
    
# Function to search for Zillow image URL and get all Airbnb links if available
def search_image_on_google(zill_image_url, retry_attempts=3):
    params = {
        "engine": "google_reverse_image",
        "image_url": 'https://photos.zillowstatic.com/fp/70f4a0d99547b625e09f6b573edcbf18-cc_ft_384.webp',
        "api_key": SERPAPI_KEY
    }

    attempt = 0
    airbnb_links = []  # List to collect all Airbnb links

    while attempt < retry_attempts:
        try:
            # Perform the reverse image search using SerpAPI
            search = GoogleSearch(params)
            results = search.get_dict()

            # Try exact match results first
            if 'image_results' in results:
                search_results = results['image_results'][:20]  # Get top 20 results
                for result in search_results:
                    link = result.get('link')
                    if "airbnb.com" in link:
                        if '/rooms/' in link:
                            # get airbnb's images of a property
                            images_links = get_images_links(link)
                            for abnb_image in images_links:
                                if generateScore(zill_image_url, abnb_image) >= 90:
                                    print(f"Found Airbnb link (Exact Match): {link}")
                                    airbnb_links.append(link)  # Add Airbnb link to the list


            # Try related images next
            if 'related_images' in results:
                related_results = results['related_images'][:20]  # Get top 20 related images
                for result in related_results:
                    link = result.get('link')
                    if "airbnb.com" in link:
                        if '/rooms/' in link:
                            # get airbnb's images of a property
                            images_links = get_images_links(link)
                            for abnb_image in images_links:
                                if generateScore(zill_image_url, abnb_image) >= 90:
                                    print(f"Found Airbnb link (Related Images): {link}")
                                    airbnb_links.append(link)  # Add Airbnb link to the list

            # Try inline images last
            if 'inline_images' in results:
                inline_results = results['inline_images'][:20]  # Get top 20 inline images
                for result in inline_results:
                    link = result.get('link')
                    if "airbnb.com" in link:
                        if '/rooms/' in link:
                            # get airbnb's images of a property
                            images_links = get_images_links(link)
                            for abnb_image in images_links:
                                similarity_score = generateScore(zill_image_url, abnb_image)
                                if similarity_score >= 90:
                                    print(f"Found Airbnb link (Inline Images): {link}")
                                    airbnb_links.append(link)  # Add Airbnb link to the list

            # If no match is found, return "No Match Found"
            if not airbnb_links:
                return "No Match Found"

            # Return all Airbnb links separated by commas
            return ', '.join(airbnb_links)

        except Exception as e:
            print(f"Error during search for {zill_image_url}: {e}")
            attempt += 1
            if attempt < retry_attempts:
                print(f"Retrying... Attempt {attempt + 1}")
                time.sleep(2)  # Wait before retrying
            else:
                return "Error"

# Function to process Zillow image URLs and write results to CSV instantly
def process_zillow_images(zillow_csv):
    airbnb_matches = set()  # Set to store unique Airbnb links
    search_count = 0  # Track the number of searches in the hour
    start_time = datetime.now()  # Track the start time for the hour

    # Generate output CSV file with timestamp in the name
    output_csv = f"output_results_{start_time.strftime('%Y%m%d_%H%M%S')}_time.csv"

    # Count the total number of images to track global image processing progress
    total_images = 0
    with open(zillow_csv, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            total_images += len(row['images'].split(','))

    # Now process the images
    current_image_count = 0  # Tracks progress for images processed
    with open(zillow_csv, 'r') as infile:
        reader = csv.DictReader(infile)
        
        # Prepare the output CSV file in append mode so it's updated after each row is processed
        with open(output_csv, 'a', newline='') as outfile:
            fieldnames = ['Zillow_Address', 'Zillow_Link', 'Image_URL', 'Airbnb_Links', 'Rent_Price', 'Description', 'Has_Pool', 'Timestamp']  # Added 'Description' and 'Has_Pool'
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)

            # Check if the CSV is empty or already has a header
            if outfile.tell() == 0:
                writer.writeheader()

            # Get the total number of rows for tracking progress
            total_rows = sum(1 for _ in reader)
            infile.seek(0)  # Reset reader to the start of the file
            next(reader)  # Skip header row
            
            # Process each Zillow image URL list
            for idx, row in enumerate(reader, start=1):
                zillow_image_urls = row['images'].split(',')  # Split by comma to get individual image URLs
                address = row['Property_address']  # Assuming you have an 'address' column
                zillow_link = row['Listing_link']  # Assuming you have a 'zillow_link' column
                rent = row['Rent_price']  # Assuming you have a 'Rent_price' column
                #description = row['Description']  # Assuming you have a 'description' column
                #has_pool = "Yes" if 'pool' in description.lower() else "No"  # Determine if the property has a pool based on the description

                row_images_count = len(zillow_image_urls)

                # Skip rows with less than 2 images
                if row_images_count < 2:
                    print(f"Skipping row {idx} because it has fewer than 2 images.")
                    continue

                print(f"Working on Zillow row {idx} of {total_rows}")

                for img_idx, image_url in enumerate(zillow_image_urls[:MAX_IMAGES_PER_PROPERTY], start=1):  # Limit to first 20 images
                    image_url = image_url.strip()

                    # Update the current image count
                    current_image_count += 1

                    # Print progress in the format: Working on Zillow row X of Y | image U of V
                    print(f"Working on Zillow row {idx} of {total_rows} | image {current_image_count} of {total_images}")

                    # Check if we need to pause for rate limiting
                    search_count += 1
                    if search_count >= MAX_SEARCHES_PER_HOUR:
                        elapsed_time = datetime.now() - start_time
                        if elapsed_time < timedelta(hours=1):
                            sleep_time = (timedelta(hours=1) - elapsed_time).total_seconds()
                            print(f"Reached {MAX_SEARCHES_PER_HOUR} searches, sleeping for {sleep_time / 60:.2f} minutes...")
                            time.sleep(sleep_time)
                        # Reset for the next hour
                        search_count = 0
                        start_time = datetime.now()

                    # Perform the reverse image search for each image in the list
                    airbnb_links = search_image_on_google(image_url)

                    # Add all images to the CSV, whether a match is found or not, along with the current timestamp
                    writer.writerow({
                        'Zillow_Address': address,
                        'Zillow_Link': zillow_link,
                        'Image_URL': image_url,
                        'Airbnb_Links': airbnb_links,
                        'Rent_Price': rent,
                        #'Description': description,
                        #'Has_Pool': has_pool,
                        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })

                    print(f"Updated CSV for image {img_idx} of row {idx}.")

                    # If a match is found, move to the next property
                    if airbnb_links != "No Match Found":
                        airbnb_matches.add(airbnb_links)  # Add Airbnb links to set for unique count
                        break

    # Print the unique Airbnb match count at the end
    print(f"\n{len(airbnb_matches)} unique Airbnb matches found.")

# Execute the script
if __name__ == "__main__":
    zillow_csv = "zillow_data_Scottsdale_latlong.csv"  # Input Zillow CSV with image URLs

    # Process Zillow images and find Airbnb links, updating CSV after every image
    process_zillow_images(zillow_csv)
