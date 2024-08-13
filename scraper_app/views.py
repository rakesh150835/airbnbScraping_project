from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraper_app.zilscraper.spiders.zillow_all import ZillowAllSpider
from scraper_app.zilscraper.spiders.zillow_furnished import run_spider_furnished
from django.contrib import messages
from . airbnb_scrape import scrape_airbnb
from scraper_app.spiders.zillow_furnished import ZillowFurnishedSpider

# def run_spider_all(city):
#     settings = get_project_settings()
#     process = CrawlerProcess(settings)

#     # Output file name
#     file_name = city.replace(" ", "_").replace(",", "") + "-all.csv"

#     # Set the FEEDS setting to store data in a CSV file
#     settings.set('FEEDS', {
#         file_name: {
#             'format': 'csv',
#             'overwrite': True
#         },
#     })

#     # Start the spider with the given city
#     process.crawl(ZillowAllSpider, city=city)
#     process.start()
# def run_spider_furnished(city):
#     settings = get_project_settings()
#     process = CrawlerProcess(settings)

#     # Output file name
#     file_name = city.replace(" ", "_").replace(",", "") + "-furnished.csv"

#     # Set the FEEDS setting to store data in a CSV file
#     settings.set('FEEDS', {
#         file_name: {
#             'format': 'csv',
#             'overwrite': True
#         },
#     })

#     # Start the spider with the given city
#     process.crawl(ZillowFurnishedSpider, city=city)
#     process.start()

def scraping(request):
    if request.method == 'POST':
        state = request.POST.get('state')
        city = request.POST.get('city', None)
        if city:
            full_city = city+' '+state
        else:
            full_city = state
        
        #settings = get_project_settings()
        process = CrawlerProcess(settings={
            'FEEDS', {
            file_name: {
                'format': 'csv',
                'overwrite': True
            },
        }
        })

        # Output file name
        file_name = full_city.replace(" ", "_").replace(",", "") + "-furnished.csv"

        # Set the FEEDS setting to store data in a CSV file
        # settings.set('FEEDS', {
        #     file_name: {
        #         'format': 'csv',
        #         'overwrite': True
        #     },
        # })

        # Start the spider with the given city
        process.crawl(ZillowFurnishedSpider, city=full_city)
        process.start()
        #run_spider_furnished(full_city)
        #scrape_airbnb(full_city)
        #run_spider_all(full_city)
        # try:
        #     messages.success(request, 'Scraping completed successfully!')
        # except Exception as e:
        #     messages.error(request, f'Scraping failed: {e}')
        return JsonResponse({'status':True,'message':'Success'})
    return render(request, 'scraper_app/index.html')