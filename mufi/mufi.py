#!/usr/bin/python3

from argparse import ArgumentParser

# Options parsing
parser = ArgumentParser(description="Mufi finds albums by style, genre, date, or mood 🐜")
parser.add_argument("-a", dest="artist", type=str, help="artist", default=None)
parser.add_argument("-d", dest="date", type=str, help="date interval, e.g. 2010-2019", default=None)
parser.add_argument("-g", dest="genre", type=str, help="genres, e.g. rock electronic", default=None)
parser.add_argument("-m", dest="moods", type=str, help="moods, e.g. sad ", default=None)
parser.add_argument("-n", dest="albums_number", type=int, help="number of albums to get (default: 1)", default=1)
parser.add_argument("-r", dest="rating", type=str, help="rating interval (1-5), e.g. \"3.5 5\"", default=None)
parser.add_argument("-t", dest="rectype", type=str, help="recording type", choices=['album', 'studio', 'live', 'single', 'remix', 'va', 'all'], default='all')
parser.add_argument("-s", dest="style", type=str, help="styles, e.g. \"blues rock,indie\"", default=None)
parser.add_argument("-v", dest="verbose", action="count", help="verbose", default=0)

order_group = parser.add_argument_group('sorting/matching arguments')
order_group.add_argument("-o", dest="order", type=str, help="sorting criteria", choices=['album', 'year', 'rating'], default=None)
order_group.add_argument("-x", dest="strict", type=int, help="strictness level for style/genre matching", choices=range(3), default=0)
order_group.add_argument("--and", dest="logic", action="store_true", help="use AND logic (default: OR)", default=False)
order_group.add_argument("--asc", dest="order_asc", action='store_true', help="ascending sort", default=False)

group_random = parser.add_argument_group("randomizer arguments")
group_random.add_argument("-k", dest="sample_num", type=int, help="number of random styles/genres to get", default=1)
group_random.add_argument("--random-album", dest="random_album", action='store_true', help="get random album", default=False)
group_random.add_argument("--random-style", dest="random_style", action='store_true', help="get random style", default=False)
group_random.add_argument("--random-genre", dest="random_genre", action='store_true', help="get random genre", default=False)

options = parser.parse_args()

import random
import re
import time
import sys


# Preprocessing
dates = list(map(int, re.split('\W', options.date))) if options.date else []
strict = options.strict
if strict:
    styles = [list(map(str.strip, re.split('\W', p.strip()))) for p in re.split('[^\w\s]', options.style)] if options.style else None
    genres = [list(map(str.strip, re.split('\W', p.strip()))) for p in re.split('[^\w\s]', options.genre)] if options.genre else None
else:
    styles = re.split('\W', options.style) if options.style else None
    genres = re.split('\W', options.genre) if options.genre else None
logic = 'and' if options.logic else 'or'
moods = re.split('\W', options.moods) if options.moods else None
albums_number = int(options.albums_number)
sample_num = int(options.sample_num)
order = options.order
order_asc = not options.order_asc if order == 'rating' else options.order_asc
rating = list(map(float, re.split('\s', options.rating))) if options.rating else []
rectypes = {'album': 'recordingtype:mainalbum',
            'live': 'recordingtype:live',
            'studio': 'recordingtype!:live',
            'single': 'recordingtype:single',
            'remix': 'recordingtype:remix',
            'va': 'recordingtype:variousartists',
            }
verbose = options.verbose

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

# Webdriver init
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True
base_url = 'https://www.allmusic.com/advanced-search/'

drv = webdriver.Chrome(options=chrome_options)
drv.implicitly_wait(10)
drv.get(base_url)


def __get_genre_or_style(drv, patterns=None, what='style', strict=False, rand=False, rand_num=1):

    elems = drv.find_elements_by_xpath("//li[@class='" + what + "']")
    results = []
    find = all if strict else any
        
    if elems:
        if patterns:
            for el in elems:
                li_text = el.get_attribute('data-text-filter')
                if strict == 2:
                    select = any([len(re.findall("|".join(pat), li_text, re.IGNORECASE)) >= len(pat) and len(pat) == len(re.split('\W', li_text)) for pat in patterns])
                elif strict == 1:
                    select = any([len(re.findall("|".join(pat), el.get_attribute('data-text-filter'), re.IGNORECASE)) >= len(pat) for pat in patterns])
                else:
                    select = len(re.findall("|".join(patterns), el.get_attribute('data-text-filter'), re.IGNORECASE)) >= len(patterns)
                
                if select:
                    name = el.find_element_by_tag_name('input').get_attribute('value')
                    eid = el.find_element_by_tag_name('input').get_attribute('id')
                    item = {'name': name, 'id': eid}
                    results.append(item)
            results = random.sample(result, rand_num) if rand else results
        elif not patterns and rand:
            chosen_elems = random.sample(elems, rand_num)
            for el in chosen_elems:
                name = el.find_element_by_tag_name('input').get_attribute('value')
                eid = el.find_element_by_tag_name('input').get_attribute('id')
                item = {'name': name, 'id': eid}
                results.append(item)
        return results
    return None


def select_genre_or_style(drv, patterns, logic, what='style', strict=False, rand=False, rand_num=1):
    
    lst = __get_genre_or_style(drv, patterns, what, strict, rand, rand_num)
    if lst:
        result = 'Selected ' + what + 's: ' + (" " + logic.upper() + " ").join([l['name'] for l in lst])

        ids = [l['id'] for l in lst]
        script = '%s.forEach(function(e, i){document.getElementById(e).click();});' % ids
        drv.execute_script(script)
    else:
        result = what.capitalize() + ' not found'

    return drv, result

def __get_moods(drv, moods=None):

    elems = drv.find_elements_by_xpath("//input[@name='mood']")

    if elems:
        results = []
        for el in elems:
            select = len(re.findall("|".join(moods), el.get_attribute('value'), re.IGNORECASE)) > 0
            
            if select:
                name = el.get_attribute('value')
                eid = el.get_attribute('id')
                item = {'name': name, 'id': eid}
                results.append(item)
        return results
    return None


def select_moods(drv, moods):
    
    lst = __get_moods(drv, moods)

    if lst:
        ids = [l['id'] for l in lst]
        script = '%s.forEach(function(e, i){document.getElementById(e).click();});' % ids
        drv.execute_script(script)

    result = 'Selected moods: ' + ', '.join([l['name'] for l in lst]) if lst else 'Moods not found'
    return drv, result


def select_date(drv, dates):
    start, end = min(dates), max(dates)

    script = '''document.getElementsByClassName('start-year')[0].value = %s;
                document.getElementsByClassName('end-year')[0].value = %s;''' % (start, end)
    drv.execute_script(script)
    return drv


def select_logic(drv, logic):

    class_name = logic + '-logic'
    drv.find_element_by_class_name(class_name)
    script = "document.getElementsByClassName('%s')[0].click();" % class_name
    drv.execute_script(script)
    return drv


def select_rating(drv, vals):
    rating = {1.: 'editorialrating:1',
          1.5: 'editorialrating:2',
          2.: 'editorialrating:3',
          2.5: 'editorialrating:4',
          3.: 'editorialrating:5',
          3.5: 'editorialrating:6',
          4.: 'editorialrating:7',
          4.5: 'editorialrating:8',
          5.: 'editorialrating:9'}
    
    minr, maxr = min(vals), max(vals)

    ids = [v for k, v in rating.items() if k >= minr and k <= maxr]
    script = '%s.forEach(function(e, i){document.getElementById(e).click();});' % ids
    drv.execute_script(script)

    return drv


def set_sorting(drv, order=None, order_asc=False):
    if order:

        results = drv.find_element_by_class_name("desktop-results")
        if not results:
            return drv

        script = "document.getElementsByClassName('{}')[0].children[0].click();".format(order)
        drv.execute_script(script)

        if not order_asc:
            script = "document.getElementsByClassName('{}')[0].children[0].click();".format(order)
            drv.find_element_by_class_name("desktop-results")
            #el = wait.WebDriverWait(drv, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "desktop-results")))
            drv.execute_script(script)
            
    return drv


def get_albums(drv, num=1, rand=False):
    albums_elems = drv.find_element_by_class_name("desktop-results").find_elements_by_tag_name('tr')
    albums = []
    if albums_elems:
        chosen_elems = random.sample(albums_elems[1:], min(num, len(albums_elems))) if rand else albums_elems[1:min(num+1, len(albums_elems))]

        for el in chosen_elems:
            title_el = el.find_element_by_class_name("title")
            url = title_el.find_element_by_tag_name("a").get_attribute('href')
            title = title_el.text
            date_el = el.find_element_by_class_name("year").text.strip()
            date = int(date_el) if date_el else ''
            artist = el.find_element_by_class_name("artist").text
            rating = el.find_element_by_xpath("td[@class='rating']/div").get_attribute('class')
            match = re.findall('(\d+)$', rating)
            stars = int(match[0]) if match else 0
            stars = int(stars / 2 + 0.5) if stars > 1 else stars
            album = {'url': url, 'rating': stars, 'artist': artist, 'date': date, 'title': title}
            albums.append(album)
        return albums
    return None


def print_albums(albums, verbose=0):
    if verbose > 1:
        print('')

    if albums:
        for i, album in enumerate(albums):
            date = '(%s)' % album['date'] if album['date'] else ''
            
            if verbose:
                print('[%d] ' % (i+1), term.BOLD, album['artist'], term.END, ' - ', album['title'], ' ' + date, ' ' + '⋆' * album['rating'], sep='')
            else:
                print(album['artist'], '-', album['title'], date, '⋆' * album['rating'])

    else:
        if verbose:
            print('Sorry, nothing found')
        sys.exit(1)


# RUNNING
if styles or options.random_style:
    drv, result = select_genre_or_style(drv, styles, logic, 'style', strict=strict, rand=options.random_style, rand_num=sample_num)
    if verbose > 1:
        print(result)

if genres or options.random_genre:
    drv, result = select_genre_or_style(drv, genres, logic, 'genre', strict=strict, rand=options.random_genre, rand_num=sample_num)

    if verbose > 1:
        print(result)

if moods:
    drv, result = select_moods(drv, moods)
    if verbose > 1:
        print(result)

if dates:
    if verbose > 1:
        print('Selected entries between {} and {}'.format(min(dates), max(dates)))
    drv = select_date(drv, dates)

if logic:
    drv = select_logic(drv, logic)

if rating:
    if verbose > 1:
        print('Selected {}-{} rating'.format(min(rating), max(rating)))
    drv = select_rating(drv, rating)

if order:
    if verbose > 1:
        print('Ordered by %s' % order)
    drv = set_sorting(drv, order, order_asc)

if options.random_album:
    if verbose > 1:
        print('Getting ' + str(albums_number) + ' random ' + ('albums' if albums_number > 1 else 'album'))

print_albums(get_albums(drv, albums_number, options.random_album), verbose=verbose)
drv.quit()
