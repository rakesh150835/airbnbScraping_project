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

'''def run_spider_all(full_city):
    file_name = full_city.replace(" ", "_").replace(",", "") + "-all.csv"
    process = CrawlerProcess(settings={
        'FEEDS': {
            file_name: {
                'format': 'csv',
                'overwrite': True,
            },
        },
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
        "CONCURRENT_REQUESTS": 1,  # Example: adjust as needed
        "ROBOTSTXT_OBEY": False,    # Disable obeying robots.txt
    })

    process.crawl(ZillowAllSpider, city=full_city)
    process.start()

def run_spider_furnished(full_city):
    file_name = full_city.replace(" ", "_").replace(",", "") + "-furnished.csv"
    process = CrawlerProcess(settings={
        'FEEDS': {
            file_name: {
                'format': 'csv',
                'overwrite': True,
            },
        },
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
    })

    process.crawl(ZillowFurnishedSpider, city=full_city)
    process.start()


def scraping(request):
    if request.method == 'POST':
        state = request.POST.get('state')
        city = request.POST.get('city', None)
        if city:
            full_city = city+' '+state
        else:
            full_city = state
        run_spider_all(full_city)
        run_spider_furnished(full_city)
        return JsonResponse({'status':True,'message':'Success'})
    return render(request, 'scraper_app/index.html')'''
# def run_spider_all(full_city):
#     file_name = full_city.replace(" ", "_").replace(",", "") + "-all.csv"
#     # Separate CrawlerProcess instance for ZillowAllSpider
#     process = CrawlerProcess(settings={
#         'FEEDS': {
#             file_name: {
#                 'format': 'csv',
#                 'overwrite': True,
#             },
#         },
#         "DEFAULT_REQUEST_HEADERS": {
#             'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#             'accept-language': 'en-US,en;q=0.9',
#             'cache-control': 'no-cache',
#             'pragma': 'no-cache',
#             'priority': 'u=0, i',
#             'referer': 'https://www.zillow.com/',
#             'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
#             'sec-ch-ua-mobile': '?0',
#             'sec-ch-ua-platform': '"Windows"',
#             'sec-fetch-dest': 'document',
#             'sec-fetch-mode': 'navigate',
#             'sec-fetch-site': 'same-origin',
#             'sec-fetch-user': '?1',
#             'upgrade-insecure-requests': '1',
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
#         },
#         "CONCURRENT_REQUESTS": 1,
#         "ROBOTSTXT_OBEY": False,
#     })

#     process.crawl(ZillowAllSpider, city=full_city)
#     process.start()

# def run_spider_furnished(full_city):
#     file_name = full_city.replace(" ", "_").replace(",", "") + "-furnished.csv"
#     # Separate CrawlerProcess instance for ZillowFurnishedSpider
#     process = CrawlerProcess(settings={
#         'FEEDS': {
#             file_name: {
#                 'format': 'csv',
#                 'overwrite': True,
#             },
#         },
#         "DEFAULT_REQUEST_HEADERS": {
#             'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#             'accept-language': 'en-US,en;q=0.9',
#             'cache-control': 'no-cache',
#             'pragma': 'no-cache',
#             'priority': 'u=0, i',
#             'referer': 'https://www.zillow.com/',
#             'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
#             'sec-ch-ua-mobile': '?0',
#             'sec-ch-ua-platform': '"Windows"',
#             'sec-fetch-dest': 'document',
#             'sec-fetch-mode': 'navigate',
#             'sec-fetch-site': 'same-origin',
#             'sec-fetch-user': '?1',
#             'upgrade-insecure-requests': '1',
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
#         },
#         "CONCURRENT_REQUESTS": 1,
#         "ROBOTSTXT_OBEY": False,
#     })

#     process.crawl(ZillowFurnishedSpider, city=full_city)
#     process.start()
def run_spiders(full_city):
    file_name_all = full_city.replace(" ", "_").replace(",", "") + "-all.csv"
    file_name_furnished = full_city.replace(" ", "_").replace(",", "") + "-furnished.csv"

    configure_logging()
    runner = CrawlerRunner(settings={
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
    })

    @inlineCallbacks
    def crawl():
        yield runner.crawl(ZillowAllSpider, city=full_city, custom_settings={
            'FEEDS': {
                file_name_all: {
                    'format': 'csv',
                    'overwrite': True,
                }
            }
        })

        # Run ZillowFurnishedSpider and save results to file_name_furnished
        yield runner.crawl(ZillowFurnishedSpider, city=full_city, custom_settings={
            'FEEDS': {
                file_name_furnished: {
                    'format': 'csv',
                    'overwrite': True,
                }
            }
        })
        reactor.stop()

    crawl()
    reactor.run()
def scraping(request):
    if request.method == 'POST':
        state = request.POST.get('state')
        city = request.POST.get('city', None)
        if city:
            full_city = city + ' ' + state
        else:
            full_city = state
        run_spiders(full_city)
        return JsonResponse({'status': True, 'message': 'Success'})

    return render(request, 'scraper_app/index.html')
