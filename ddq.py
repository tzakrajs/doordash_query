#!/usr/bin/env python
import hashlib
import json
import re
import requests
import sys
import unicodedata
from unidecode import unidecode

LATITUDE = 37.371941
LONGITUDE = -121.886283

BASE_URL = 'https://www.doordash.com'
CACHE_FILE_PREFIX = 'ddq.cache'

JUNK_WORDS = ['of', 'a', 'in', 'and', 'with', 'on', 'or', 'our', 'the', 'w'
              '&', 'your', 'over', 'de', 'to', 'w/', 'for', 'an', 'any',
              'is', 'it', 'its', 'per', '&']

def get_hash(seeds):
    hash = hashlib.md5()
    [hash.update(str(x)) for x in seeds]
    return hash.hexdigest()

def cache_file_name(hash):
    cache_file_name = '{0}.{1}'.format(CACHE_FILE_PREFIX, hash)
    return cache_file_name

def get_uri(uri):
    try:
        cached_response = get_cache(uri)
    except IOError:
        cached_response = None
    if cached_response:
        return cached_response
    response = requests.get('{0}/{1}'.format(BASE_URL, uri))
    response_text = response.text
    build_cache(response_text, uri)
    return response_text

def get_cache(*args):
    hash = get_hash(args)
    cache_file = open(cache_file_name(hash), 'r+')
    obj = json.loads(cache_file.read())
    cache_file.close()
    return obj

def build_cache(content, *args):
    hash = get_hash(args)
    cache_file = open(cache_file_name(hash), 'w')
    cache_file.write(json.dumps(content))
    cache_file.close()

def convert_to_dicts(parent, new_parent=None):
    """Takes a recursive list of dicts and returns recursive dict of dicts
       only changes a list into a dict, when its children dicts have id keys
    """
    new_parent = {}
    if isinstance(parent, list) and len(parent) > 0:
        if isinstance(parent[0], dict) and parent[0].get('id'):
            # assume all children dicts have an id key
            for child in parent:
                new_parent[child['id']] = convert_to_dicts(child)
    elif isinstance(parent, dict) and len(parent.keys()) > 0:
        for child_key, child_value in parent.iteritems():
            new_parent[child_key] = convert_to_dicts(child_value)
    elif not isinstance(parent, list) and not isinstance(parent, dict):
        return parent
    return new_parent

def get_restaurants(latitude=LATITUDE, longitude=LONGITUDE):
    """Takes float latitude, float longitude, returns list of restaurants"""
    try:
        restaurants = get_cache('restaurants,{0},{1}'.format(latitude,
                                                             longitude))
    except IOError:
        restaurants = None
    if restaurants:
        return restaurants
    uri = 'api/v2/restaurant/?lat={0}&lng={1}'.format(latitude, longitude)
    response_text = get_uri(uri)
    restaurants = convert_to_dicts(json.loads(response_text))
    # now populate the menus
    for restaurant_id, restaurant in restaurants.iteritems():
        restaurant['menus'] = get_menus(restaurant)
    build_cache(restaurants, 'restaurants,{0},{1}'.format(latitude,
                                                          longitude))
    return restaurants

def extract_menu_json(menu_html):
    menu_json = re.search('var restaurantMenu = JSON.parse\("(.*)"\);',
                          menu_html)
    if menu_json:
        menu_json_unicode = menu_json.group(1)
        #quotes
        menu_json_unicode = menu_json_unicode.replace('\u0022', '"')
        #backslash
        menu_json_unicode = menu_json_unicode.replace('\u005C', '\\')
        #hyphen/minus
        menu_json_unicode = menu_json_unicode.replace('\u002D', '-')
        return json.loads(menu_json_unicode)

def get_menus(restaurant):
    """Takes dict of restaurant attributes, returns dict with menus"""
    slug = restaurant['slug']
    id = restaurant['id']
    menus = restaurant['menus']
    for menu_id, menu in menus.iteritems():
        uri = 'store/{0}-{1}/{2}/'.format(slug, id, menu_id)
        menu_items = extract_menu_json(get_uri(uri))
        menu.update(menu_items)
    return convert_to_dicts(menus)

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def extract_food_words(item):
    words = u'{0} {1}'.format(item['description'], item['name'])
    words = strip_accents(words)
    words = unidecode(words)
    regex = re.compile('[\'\.\,\'"]')
    words = regex.sub('', words)
    regex = re.compile('[\-/]')
    words = regex.sub(' ', words)
    return words.lower().split()

def populate_food_word_index(food_word_index, restaurant):
    restaurant_id = restaurant['id']
    for menu_id, menu in restaurant['menus'].iteritems():
        for category_id, category in menu['menu_categories'].iteritems():
            for item_id, item in category['items'].iteritems():
                identifier = (restaurant_id, menu_id, category_id, item_id)
                words = extract_food_words(item)
                for word in words:
                    if word in JUNK_WORDS:
                        continue
                    if not food_word_index.get(word):
                        food_word_index[word] = set()
                    food_word_index[word].add(identifier)
    return food_word_index

if __name__ == "__main__":
    search_terms = sys.argv[1:]
    food_word_index = {}
    restaurants = get_restaurants(LATITUDE, LONGITUDE)
    for restaurant_id, restaurant in restaurants.iteritems():
        food_word_index = populate_food_word_index(food_word_index, restaurant)
    word_popularity = []
    for word, instances in food_word_index.iteritems():
        word_popularity.append((word, len(instances)))
    word_popularity.sort(key=lambda x:x[1], reverse=True)
    for word, count in word_popularity:
        print u"{0}: {1}".format(word, count)
    search_results = []
    for term in search_terms:
        instances = food_word_index[term]
        for instance in instances:
            restaurant_id, menu_id, category_id, item_id = instance
            restaurant = restaurants[str(restaurant_id)]
            menu = restaurant['menus'][str(menu_id)]
            category = menu['menu_categories'][str(category_id)]
            item = category['items'][str(item_id)]
            price = str(item['price'])
            price = '${0}.{1}'.format(price[:-2], price[-2:])
            slug = restaurant['slug']
            doordash_url = '{0}/store/{1}-{2}/{3}/'.format(BASE_URL,slug, 
                                                           restaurant_id, menu_id)
            result = {'name': item['name'],
                      'description': item['description'],
                      'price': price,
                      'restaurant_name': restaurant['name'],
                      'menu_name': menu['name'],
                      'category_name': category['title'],
                      'doordash_url': doordash_url}
            search_results.append(result)
        search_results.sort(key=lambda x:x['restaurant_name'])
        print "=================================="
        print "Results: {0}".format(len(search_results))
        print "=================================="
        for search_result in search_results:
            print u"Name: {0}".format(search_result['name'])
            print u"Description: {0}".format(search_result['description'])
            print u"Price: {0}".format(search_result['price'])
            print u"Restaurant: {0}".format(search_result['menu_name'])
            print u"Category: {0}".format(search_result['category_name'])
            print u"URL: {0}".format(search_result['doordash_url'])
            print "=================================="
