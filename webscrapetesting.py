# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 19:25:50 2022

@author: JD
"""

# tutorial i used : https://www.youtube.com/watch?v=XVv6mJpFOb0&
# you may need to install beautifulsoup and lxml to properly compile this. He goes over how to install in that video

""" 
TO DO:
    condense stuff into methods/functions better. rn i just coded everything into main and its kind of messy - Jared
"""

from bs4 import BeautifulSoup
import requests



# get the html data from the imdb comedy movie list
imdb_url = 'https://www.imdb.com'
html_text = requests.get('https://www.imdb.com/search/title/?genres=comedy&start=1&explore=title_type,genres&ref_=adv_nxt').text
soup = BeautifulSoup(html_text, 'lxml')

# given an abitrary page in the listing of movies, get the next page
def getNextPageURL(url):
    soup = BeautifulSoup(requests.get(url).text,'lxml')
    nextlink = imdb_url + soup.find('a', class_ ='lister-page-next next-page').get('href')
    return str(nextlink)
"end def"

# get movie links
def getMovieLinks():
    # this url is the one for comedy movies, if you want 1000 movies of a different genre, just swap this url
    url = 'https://www.imdb.com/search/title/?genres=comedy&start=1&explore=title_type,genres&ref_=adv_nxt'
    
    movieLinkList = []
    for i in range(0,10): # this range number can be modified to get a designated amt of links
        soup = BeautifulSoup(requests.get(url).text, 'lxml')
        moviecards = soup.find_all('h3', class_ = 'lister-item-header')
        for m in moviecards:
            movieLinkList.append(imdb_url + m.a.get('href'))
        url = getNextPageURL(url)
    "end for"

    return movieLinkList

"end def"

# given the link to a moviepage, get all the info that we may want.
# link to the google doc with schemas : https://docs.google.com/document/d/1u5GSzlVB__nNwAN6gUZsgE6nMR-T4LVavB8agKqINrY/edit
# will likely be very very long
def getMovieInfo(moviePageUrl):
    soup = BeautifulSoup(requests.get(moviePageUrl).text, 'lxml')
    
    temp = []
    # budget: there is no budget listing for movies
    title = soup.find('h1', class_ = 'sc-b73cd867-0 eKrKux').text #Name
    grossingWorldwide = soup.find('li', class_ = "ipc-metadata-list__item sc-3c7ce701-2 eYXppQ").find('span').find_next_sibling().text # grossing worldwide
    # had to use attrs={key : value} for this because the key had a hyphen in it and python doesnt like that
    releaseDate = soup.find('li', attrs={'data-testid' : 'title-details-releasedate'}).a.find_next_sibling().text

    return temp
"end def"

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
#title = movie_soup.find('h1', class_ = 'TitleHeader__TitleText-sc-1wu6n3d-0 dxSWFG').text
importantpeople = movie_soup.find('ul', class_ = 'ipc-metadata-list ipc-metadata-list--dividers-all title-pc-list ipc-metadata-list--baseAlt')
directors = importantpeople.find_all('li', class_ = 'ipc-metadata-list__item')

# prints all the important people that contributed to the movie
for test in directors:
    print(test.text)




