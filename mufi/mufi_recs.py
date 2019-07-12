#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from random import sample, shuffle
import os
import re
import sys

# Login data paths
paths = list(map(os.path.expanduser, ['~/.lastfm', '~/.config/mufi/.lastfm']))

# Terminal colors
class term:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def login(drv, user, password):
    login_field = drv.find_element_by_id('id_username')
    if login_field:
        login_field.send_keys(user)

        pass_field = drv.find_element_by_id('id_password')
        pass_field.send_keys(password)
        pass_field.send_keys(Keys.ENTER)
    return drv

def get_login_data(paths):
    for path in paths:
        if os.path.exists(path) and os.path.isfile(path):
            with open(path) as file:
                user, password = file.read().split()
            return user, password
    return None

def nav_artists(drv):
    drv.get('https://www.last.fm/home/artists')
    return drv

def nav_albums(drv):
    drv.get('https://www.last.fm/home/albums')
    return drv


def get_recom_artists(drv):
    artists_elems = drv.find_elements_by_class_name('recs-feed-item--artist')
    if artists_elems:
        results = []
        for artist_elem in artists_elems:
            artist_name = artist_elem.find_element_by_xpath('.//h3[@class="recs-feed-title"]').text
            listeners = artist_elem.find_element_by_xpath('.//p[@class="recs-feed-description"]').text.replace(',', ' ').strip()
            listeners = re.sub(r'\D', '', listeners)
            listeners = int(listeners) if listeners else ''
            context = artist_elem.find_element_by_xpath('.//div[@class="context"]').text.strip()
            artist = {'name': artist_name, 'listeners': listeners, 'context': context}

            results.append(artist)
        return results
    return None

def get_recom_albums(drv):
    albums_elems = drv.find_elements_by_class_name('recs-feed-inner-wrap')
    if albums_elems:
        results = []
        for album_elem in albums_elems:
            album_name = album_elem.find_element_by_xpath('.//h3[@class="recs-feed-title"]').text
            artist_name = album_elem.find_element_by_xpath('.//p[@class="recs-feed-description"]/a').text
            listeners_text = album_elem.find_element_by_xpath('.//p[@class="recs-feed-description"]').text
            listeners_matches = re.search(r'\d+ listeners', re.sub(r'[^\w\s]', '', listeners_text))
            listeners = int(re.sub(r'\D', '', listeners_matches[0])) if listeners_matches else ''

            context = album_elem.find_element_by_xpath('.//div[@class="context"]').text.strip()
            artist = {'artist': artist_name, 'album': album_name, 'context': context, 'listeners': listeners}

            results.append(artist)
        return results
    return None



def sort(lst, key, rev, num):
    if key == 'none':
        s = lst
    if key == 'random':
        shuffle(lst)
        s = lst
    else:
        s = sorted(lst, key=lambda x: x[key], reverse=rev)
    
    return s[:num] if num else s

def print_artists(lst, context=True, comfy=False, verbose=0):
    for i, artist in enumerate(lst):
        
        listeners = (' (%d listeners)' % artist['listeners']) if artist['listeners'] else ''

        if verbose == 1:
            print(artist['name'], listeners, sep='')
        elif verbose == 2:
            print(term.BOLD, artist['name'], term.END, listeners, sep='')
        elif verbose >= 3:
            print('[%d] ' % (i+1), term.BOLD, artist['name'], term.END, listeners, sep='')
        else:
            print(artist['name'])
       
        if context:
            spaces = ' ' * (len('[%d] ' % (i+1)) + 1)
            print(spaces + artist['context'])
        if comfy:
            print('')

def print_albums(lst, context=True, comfy=False, verbose=0):
    for i, item in enumerate(lst):
        
        listeners = (' (%d listeners)' % item['listeners']) if item['listeners'] else ''

        if verbose >= 2:
            print('[%d] ' % (i+1), term.BOLD, item['artist'], term.END, ' - ', item['album'], listeners, sep='')
        elif verbose == 1:
            print(term.BOLD, item['artist'], term.END, ' - ', item['album'], listeners, sep='')
        else:
            print(item['artist'], '-', item['album'],)
       
        if context:
            print(item['context'])
        if comfy:
            print('')

def init_drv(headless=True, wait=15):

    options = webdriver.ChromeOptions()
    options.headless = headless
    login_url = 'https://secure.last.fm/login'

    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(wait)
    drv.get(login_url)
    return drv

#if __name__ == '__main__':
def main():

    from argparse import ArgumentParser

    # Options parsing
    parser = ArgumentParser(description='Mufi fetches your recommendations from last.fm 🐜 ')
    parser.add_argument("-a", dest="artists", action="store_true", help="recommended artists (default)", default=False)
    parser.add_argument("-l", dest="albums", action="store_true", help="recommended albums", default=False)
    parser.add_argument("-n", dest="number", type=int, help="results number", default=0)
    parser.add_argument("-o", dest="orderby", type=str, help="sort by: none, random (default), name, listeners", default='random')
    parser.add_argument("-s", dest="context", action='store_true', help="show similar/context", default=False)
    parser.add_argument("-v", dest="verbose", action='count', help="verbose", default=0)
    options = parser.parse_args()

    artists = True if not any([options.artists, options.albums]) else options.artists
    albums = options.albums
    number = int(options.number)
    orderby = options.orderby
    context = options.context
    verbose = options.verbose

    drv = init_drv()
    
    login_data = get_login_data(paths)
    if not login_data:
        print('No login data found. Please say `echo login password > ~/.lastfm` in terminal. You can also use `~/.config/mufi/.lastfm` file to store your login data')
        sys.exit(1)

    user, password = login_data
    login(drv, user, password)

    if artists:
        nav_artists(drv)
        artists = sort(get_recom_artists(drv), key=orderby, rev=True, num=number)
        print_artists(artists, context=context, verbose=verbose)
    else:
        nav_albums(drv)
        albums = sort(get_recom_albums(drv), key=orderby, rev=True, num=number)
        print_albums(albums, context=context, verbose=verbose)

    drv.quit()
