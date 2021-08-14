import os
import time 
import asyncio

import pandas as pd

from utils import parse


def main(start_page):
    RES_DATA_DIR = 'datasets'
    DATASET_NAME = 'poems_data_scrapped.csv'

    print('Extracting authors list...')
    authors_list = parse.get_authors(start_page)
    print(f'Authors list extracted, length of list : {len(authors_list)}')

    print('Exracting list of poems links...')
    start_time = time.perf_counter()
    loop = asyncio.get_event_loop()
    poem_link_list = []
    for res in loop.run_until_complete(parse.scrape_poem_links(authors_list)):
        poem_link_list.extend(res)
    loop.close
    print('List of poems links extracted,' + 
          f'number of poem links: {len(poem_link_list)}')
    print(f'Elapsed time {time.perf_counter() - start_time} seconds')

    print('Poems data extracting...')
    start_time = time.perf_counter()
    loop = asyncio.get_event_loop()
    poem_data_list = loop.run_until_complete(parse.scrape_poems(poem_link_list))
    print('Poems data extracted')
    print(f'Elapsed time {time.perf_counter() - start_time} seconds')

    res = pd.DataFrame(poem_data_list)
    
    print(f'Dataset saving...')
    if not os.path.exists(RES_DATA_DIR):
        os.makedirs(RES_DATA_DIR)
    
    res_dataset_path = os.path.join(RES_DATA_DIR, DATASET_NAME)
    res.to_csv(res_dataset_path, index=False)
    print(f'Dataset saved in {res_dataset_path} directory')


if __name__ == '__main__':
    main('https://slova.org.ru/')
