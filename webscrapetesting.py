# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 19:25:50 2022

@author: JD
"""

from bs4 import BeautifulSoup
import requests


# get the html data from the imdb comedy movie list
imdb_url = 'https://www.imdb.com'
html_text = requests.get('https://www.imdb.com/search/title/?genres=comedy&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3396781f-d87f-4fac-8694-c56ce6f490fe&pf_rd_r=9ARWMHY5YKJ7EFVTNE0V&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr1_i_1').text
soup = BeautifulSoup(html_text, 'lxml')

#movies = soup.find_all('div', class_ = 'lister-list')

# gets the first movie in the list
movie = soup.find('div', class_ = 'lister-item mode-advanced')
# gets the first 'a' head, which includes the link to the movie page containing more details
ahead = movie.find('a')

# extracts the link to the movie page contaning more details from the a head
relative_webaddress = ahead['href']

# construct the moviepage url from the imdb url and the relative webadress
moviepage_url = imdb_url + relative_webaddress
#print(moviepage_url)

# get the html data from the moviepage
movie_html_text = requests.get(moviepage_url).text
movie_soup = BeautifulSoup(movie_html_text, 'lxml')

# get the title of the movie, important people, and directors
title = movie_soup.find('h1', class_ = 'TitleHeader__TitleText-sc-1wu6n3d-0 dxSWFG').text
importantpeople = movie_soup.find('ul', class_ = 'ipc-metadata-list ipc-metadata-list--dividers-all title-pc-list ipc-metadata-list--baseAlt')
directors = importantpeople.find_all('li', class_ = 'ipc-metadata-list__item')

for test in directors:
    print(test.text)

# prints all the attributes that title has
# print(title.attrs)


