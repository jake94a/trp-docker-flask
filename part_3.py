"""
Rewrite the following:

def scrape_sites(sites):
	results = []

	for site in sites:
		r = requests.get(site)
		results.append(r.content)

	return results
 """

import requests
import asyncio

sites = [
    "http://www.google.com",
    "http://www.github.com",
    "http://www.youtube.com",
    "http://www.facebook.com",
    "http://www.yahoo.com",
]

# list comprehension
def scrape_sites(sites):
    """
    Use the `requests` library to hit each site in the sites list
    Store the content of each site in a dictionary

    If we want to scrape for something specific, such as JS, then we could scrape only <script> tags
    or <meta> if we want site metadata

    Notes:
    - I like this solution for its simplicity, but it can be difficult to understand at first glace
    """
    return [{site: requests.get(site).content} for site in sites]


# basic
def scrape_sites(sites):
    """
    Use the `requests` library to hit each site in the sites list
    Store the content of each site in a dictionary

    If we want to scrape for something specific, such as JS, then we could scrape only <script> tags
    or <meta> if we want site metadata

    Notes:
    - I like this solution for its verbosity
    - This isn't really a re-written solution, however, only having one more broken-out step
    """
    scraped_info = []

    for site in sites:
        req = requests.get(site)
        site_content = req.content
        scraped_info.append(site_content)

    return scraped_info


# asyncio
async def scrape_site(site):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, requests.get, site)
    return response.content


async def scrape_sites(sites_list):
    scraped_info = [{site: await scrape_site(site)} for site in sites_list]
    print(scraped_info)
    return scraped_info


asyncio.run(scrape_sites(sites))
