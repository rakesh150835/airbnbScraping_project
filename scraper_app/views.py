from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from scrapy.crawler import CrawlerProcess
from django.contrib import messages
from . airbnb_scrape import scrape_airbnb
from scraper_app.spiders.zillow_furnished import ZillowFurnishedSpider
from scraper_app.spiders.zillow_all import ZillowAllSpider
from scrapy.utils.log import configure_logging
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
import os
from django.conf import settings
from . mapping import map
from django.views.decorators.csrf import csrf_exempt
import zipfile
from django.conf import settings
from io import BytesIO
import time



def delete_csv_files(directory):
    for file_name in os.listdir(directory):
        if file_name.endswith('.csv'):
            file_path = os.path.join(directory, file_name)
            os.remove(file_path)

@csrf_exempt
def run_spiders(request):
    if request.method == 'POST':
        state = request.POST.get('state')
        city = request.POST.get('city', None)
        if city:
            full_city = city + ' ' + state
        else:
            full_city = state
        media_dir = os.path.join(settings.MEDIA_ROOT)
        root_dir = os.path.join(settings.BASE_DIR)
        # delete_csv_files(media_dir)  #REMOVE THE COMMENT IN PRODUCTION
        # delete_csv_files(root_dir) #REMOVE THE COMMENT IN PRODUCTION
        
        file_name_all = "zillow_data.csv"
        file_name_furnished = 'media/'+full_city.replace(" ", "_").replace(",", "") + "-furnished.csv"

        configure_logging()

        @inlineCallbacks
        def crawl():
            # Run ZillowFurnishedSpider
            runner_furnished = CrawlerRunner(settings={
                "DEFAULT_REQUEST_HEADERS": {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'no-cache',
                    'pragma': 'no-cache',
                    'priority': 'u=0, i',
                    'referer': 'https://www.zillow.com/',
                    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                },
                "CONCURRENT_REQUESTS": 1,
                "ROBOTSTXT_OBEY": False,
                'FEEDS': {
                    file_name_furnished: {
                        'format': 'csv',
                        'overwrite': True,
                    }
                }
            })
            yield runner_furnished.crawl(ZillowFurnishedSpider, city=full_city)

            # Run ZillowAllSpider
            runner_all = CrawlerRunner(settings={
                "DEFAULT_REQUEST_HEADERS": {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'no-cache',
                    'pragma': 'no-cache',
                    'priority': 'u=0, i',
                    'referer': 'https://www.zillow.com/',
                    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                },
                "CONCURRENT_REQUESTS": 1,
                "ROBOTSTXT_OBEY": False,
                'FEEDS': {
                    file_name_all: {
                        'format': 'csv',
                        'overwrite': True,
                    }
                }
            })
            yield runner_all.crawl(ZillowAllSpider, city=full_city)

            reactor.stop()

        crawl()
        reactor.run()
        return JsonResponse({
            'status':True,
            'full_city': full_city
        })
        

@csrf_exempt
def airbnb(request):
    if request.method == 'POST':
        # Extract data from the request
        full_city = request.POST.get('full_city')
        city = full_city.lower().replace(" ", "-").replace(",", "")
        try:
            scrape_airbnb(city)
            return JsonResponse({
                    'status':True,
                    'message':'Airbnb scarping Completed!'   
                })
        except:
            return JsonResponse({
                    'status':False,
                    'message': 'Something Went Wrong In Airbnb Scraping!'
                })    

@csrf_exempt
def data_mapping(request):
    if request.method == 'POST':
        #full_city = request.POST.get('full_city')
        try:
            map() 
            mapping_result = f"Data mapping completed!"
            return JsonResponse({'status': True, 'message': mapping_result})
        except :
            return JsonResponse({'status': False, 'message': 'Something Went Wrong In Mapping!'})

def download_media_zip(request):
    # Create a BytesIO buffer to hold the zip file in memory
    buffer = BytesIO()

    # Create a ZipFile object with the buffer as the file
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        # Walk through the media directory
        for root, dirs, files in os.walk(settings.MEDIA_ROOT):
            for file_name in files:
                # Create the full file path
                file_path = os.path.join(root, file_name)

                # Add the file to the zip file, maintaining the directory structure
                zip_file.write(file_path, os.path.relpath(file_path, settings.MEDIA_ROOT))

    # Prepare the buffer for reading by seeking to the beginning
    buffer.seek(0)

    # Create an HTTP response with the zip file
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=media_files.zip'

    return response

def scraping(request):
    # if request.method == 'POST':
    #     state = request.POST.get('state')
    #     city = request.POST.get('city', None)
    #     if city:
    #         full_city = city + ' ' + state
    #     else:
    #         full_city = state
    #     media_dir = os.path.join(settings.MEDIA_ROOT)
    #     root_dir = os.path.join(settings.BASE_DIR)
        #delete_csv_files(media_dir)
        #delete_csv_files(root_dir)

        # run_spiders(full_city)
        # scrape_airbnb(full_city)
        # map()
        # return JsonResponse({'status': True, 'message': 'Success'})

    return render(request, 'scraper_app/index.html')
