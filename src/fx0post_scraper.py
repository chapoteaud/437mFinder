import requests as req
from bs4 import BeautifulSoup
import re

def fx0post_scraper(fx0, url, item):
    # use regex to find 437M in thread titles
    wheels_437M = re.compile(item)

    # f30 post scrappers
    fx0post_scrapper  = req.get(url)
    fx0post_data = BeautifulSoup(fx0post_scrapper.text, 'lxml')

    # Find any posts with 437M in the title
    fx0post_data_links = fx0post_data.find_all('a', string=wheels_437M)

    # Alert if there any sellers in either forum
    seller_urls = []
    
    no_sellers = f'No sellers on {fx0} at this time'

    if fx0post_data_links:
        email_fx0 = f'There are {len(fx0post_data_links)} sellers for 437M wheels! on {fx0} post'
        for sellers in fx0post_data_links:
            seller_urls_dict = {}

            # Build hyperlink to post from data
            href = sellers.get('href')
            # title = f'Thread: {sellers.get_text()}'
            # link = f'Link: https://{fx0}.bimmerpost.com/forums/{href}'
            # seller_urls.append(f'{title} | {link}')
            #             
            seller_urls_dict['title'] = sellers.get_text()
            seller_urls_dict['link'] = f'https://{fx0}.bimmerpost.com/forums/{href}'

            seller_urls.append(seller_urls_dict)
            


    
    # Shoot an email of data that was found
    if not seller_urls:
        return no_sellers
    
    return seller_urls



if __name__ == '__main__':
    fx0post_scraper()
