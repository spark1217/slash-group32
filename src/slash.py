"""
Copyright (C) 2021 SE Slash - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: secheaper@gmail.com

"""

import argparse
import scraper
import formatter
import email_utils
from tabulate import tabulate
import browser
import time
import threading
import concurrent.futures
from multiprocessing.dummy import Pool as ThreadPool
import itertools


def main(search_item, num_item, sort_item, order_item, email):
    order_des = False
    sort = 're'
    if order_item == "Descending":
        order_des = True

    if sort_item == "price":
        sort = 'pr'
    elif sort_item == "rating":
        sort = 'ra'

    finalistList = []

    # List of stores to scrape
    stores = ['amazon', 'walmart', 'target', 'costco', 'ebay']
    # Create a thread for each store
    pool = ThreadPool(len(stores))
    # Scrape each store using the search item
    results = pool.starmap(
        scraper.searchStore,
        zip(stores, itertools.repeat(search_item), itertools.repeat(True)))
    # Appends results to final list of products
    for x in range(0, len(results)):
        finalistList.append(results[x][:num_item])
    print(results)
    mergedResults = email_utils.alternateMerge(finalistList)
    results = formatter.sortList(mergedResults, sort, order_des)

    print()
    print()
    print(tabulate(results, headers="keys", tablefmt="github"))
    print(
        "\nTrying to send email notification to the customers if there are any...\n"
    )
    email_utils.write_data(results, True, email)
    print("Done :)")
    print()
    print()

    return results
