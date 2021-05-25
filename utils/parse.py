import asyncio
import requests

from bs4 import BeautifulSoup
from aiohttp.client import ClientSession


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()

async def fetch_with_sem(url, session, sem):
    async with sem:
        return await fetch(url, session) 


def get_authors(url, main_page='https://slova.org.ru'):
    website_url = requests.get(url, verify=False).text
    soup = BeautifulSoup(website_url, 'html.parser')
    
    author_list = []
    for letter_box in soup.find_all('div', class_='letter_box'):
        for link in letter_box.find_all('a'):
            link = link.get('href')
            # Link to an author page is appended to a main page since 
            # all author page links are relative.
            author_list.append(main_page + f"/{link.split('/')[-2]}/")
    return author_list


# Links with poems extracting
def get_poem_links(web_page, main_page='https://slova.org.ru'):
    '''A function that parses the author's page to get links to poems'''
    soup = BeautifulSoup(web_page, 'html.parser')
    
    # First element is taken since there is only one letter_box
    # on a page with poem.
    # Link to poem is appended to a main page since 
    # poem links on the author page are relative.
    links = soup.find_all('div', class_='letter_box')[0]
    links_list = [
        main_page + link.get('href') for link in links.find_all('a')
    ]
    return links_list

async def fetch_and_parse_links(url, session, main_page='https://slova.org.ru'):
    web_page = await fetch(url, session)
    sample = get_poem_links(web_page, main_page=main_page)
    return sample

async def scrape_poem_links(url_list, main_page='https://slova.org.ru'):
    async with ClientSession() as session:
        return await asyncio.gather(
            *(
                fetch_and_parse_links(url, session, main_page=main_page) 
                for url in url_list
            )
        )


# Poem extracting
def get_sample_data(web_page):
    '''A function that extracts text and header from a poem page'''
    soup = BeautifulSoup(web_page,'html.parser')
    soup.em.decompose()
    data = {}
    title = soup.find_all('title')
    text = soup.find_all('pre')
    
    # None value is added to dict so as not to break the dict
    # structure when title or text not found
    if not (text):
        data['text'] = None
    else:
        data['text'] = text[0].text
    
    if not (title):
        data['title'] =  None
    else:
        data['title'] = title[0].text     
    return data

async def fetch_and_parse_poems(url, session, sem):
    web_page = await fetch_with_sem(url, session, sem)
    sample = get_sample_data(web_page)
    return sample

async def scrape_poems(url_list, sem_value=200):
    sem = asyncio.Semaphore(sem_value)
    async with ClientSession() as session:
        return await asyncio.gather(
            *(fetch_and_parse_poems(url, session, sem) for url in url_list)
        )
