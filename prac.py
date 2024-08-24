import gobnb

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

print(image_links)
