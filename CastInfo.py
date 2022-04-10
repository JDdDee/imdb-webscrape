# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 14:06:30 2022

@author: JD

goal of this file is to visit every tvshow page and movie page then build a cast list with the appropriate info, and export it into a csv
"""

import pickle
from bs4 import BeautifulSoup
import requests

pickle_in = open('moviePagelinks.p', 'rb')
movieLinks = pickle.load(pickle_in)
pickle_in.close()

pickle_in = open('TVShowPagelinks.p', 'rb')
TVShowLinks = pickle.load(pickle_in)
pickle_in.close()

imdb_url = 'https://www.imdb.com'
#The Lost city movie url
url = 'https://www.imdb.com/title/tt13320622/?ref_=adv_li_tt'

soup = BeautifulSoup(requests.get(url).text,'lxml')


""" ------------------------------- cast --------------------------------------- """
top_castlist = soup.find_all('a', attrs={'data-testid' : 'title-cast-item__actor'})

castlinks = []
for n in top_castlist:
    castlinks.append(imdb_url + n.get('href'))
#print(castlinks)

"""
for n in top_castlist:
    cast_url = imdb_url + n.get('href')
    #print(cast_url)
    castname = n.text
    castid = n.get('href')[6:15]
    soup2 = BeautifulSoup(requests.get(cast_url).text,'lxml')
    temp = soup2.find('div', attrs={'id':'name-born-info'})
    if(temp != None):
        dob = temp.time['datetime']
        born_in = temp.find_all('a')[2].text
    else:
        dob = None
        born_in = None
    print(castid)
    print(castname)
    print(dob)
    print(born_in)
""" 
""" ---------------------------------------------------------------------"""
