# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 19:25:50 2022

@author: JD
"""

# tutorial i used : https://www.youtube.com/watch?v=XVv6mJpFOb0&
# you may need to install beautifulsoup and lxml to properly compile this. He goes over how to install in that video

""" 
TO DO:
    
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
# output of this function will most likely be a dataframe with columns (movieid, movietitle, grossing, releasedate, rating, etc.)
def getMovieInfo(moviePageUrl):
    soup = BeautifulSoup(requests.get(moviePageUrl).text, 'lxml')
    
    # variables are named to match the names of the attributes of the relation schema
    
    movieID = moviePageUrl[27:37]
    title = soup.find('h1', class_ = 'sc-b73cd867-0 eKrKux').text #name
    
    temp = soup.find('div', attrs={'data-testid' : 'title-boxoffice-section'}) # grossing info
    if(temp != None):
        grossingUS_CA = temp.find('li', attrs={'data-testid' : 'title-boxoffice-grossdomestic'})
        if(grossingUS_CA !=None):
            grossingUS_CA = grossingUS_CA.find('li').text
        grossingUS_CA_OpeningWeekend = temp.find('li', attrs={'data-testid' : 'title-boxoffice-openingweekenddomestic'})
        if(grossingUS_CA_OpeningWeekend != None):
            grossingUS_CA_OpeningWeekend = grossingUS_CA_OpeningWeekend.find('li').text
        grossingWorldwide = temp.find('li', attrs={'data-testid' : 'title-boxoffice-cumulativeworldwidegross'})
        if(grossingWorldwide != None):
            grossingWorldwide = grossingWorldwide.find('li').text
    
    # had to use attrs={key : value} because the key had a hypen in it and python doesnt like that
    #note on release date can do a .split('(')[0] to remove the place
    releaseDate = soup.find('li', attrs={'data-testid' : 'title-details-releasedate'}).a.find_next_sibling().text # release date
    countriesOfOrigin = soup.find('li', attrs={'data-testid' : 'title-details-origin'}).find_all('li') # countries of origin
    # temp variables initialized to make countires of origin
    temp2 = ""
    for x in countriesOfOrigin:
        temp2 = temp2 + x.text + ", "
    countries_of_origin = temp2[:-2] # removes the last comma and space
    imdb_rating = soup.find('div', class_ = 'sc-7ab21ed2-2 kYEdvH').text.split('/')[0] # imdb rating
    popularity_score = soup.find('div', attrs={'data-testid' : 'hero-rating-bar__popularity__score'}).text #popularity score
    popularity_delta = soup.find('div', attrs={'data-testid' : 'hero-rating-bar__popularity__delta'}).text #popularity delta
    runtime = soup.find('li', attrs={'data-testid' : 'title-techspec_runtime'}).find('div').text #runtime
    color = soup.find('li', attrs={'data-testid' : 'title-techspec_color'}).find('li').text # color
    aspectratio = soup.find('li', attrs= {'data-testid' : 'title-techspec_aspectratio'}).find('div').text # aspectratio
    
    """
    print(movieID)
    print(title)
    print(grossingUS_CA)
    print(grossingUS_CA_OpeningWeekend)
    print(grossingWorldwide)
    print(releaseDate)
    print(countries_of_origin)
    print(imdb_rating)
    print(popularity_score)
    print(popularity_delta)
    print(runtime)
    print(color)
    print(aspectratio)
    """
    
    
    top_castlist = soup.find_all('a', attrs={'data-testid' : 'title-cast-item__actor'})
    castlinks = []
    for n in top_castlist:
        castlinks.append(imdb_url + n.get('href'))
    
    
    
    
"end def"


# test that the movielinks function is working
links = getMovieLinks()
print(links)
    

#getMovieInfo('https://www.imdb.com/title/tt13320622/?ref_=adv_li_tt')

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

# get title of the movie, important people, and directors
title = movie_soup.find('h1', class_ = 'TitleHeader__TitleText-sc-1wu6n3d-0 dxSWFG')
importantpeople = movie_soup.find('ul', class_ = 'ipc-metadata-list ipc-metadata-list--dividers-all title-pc-list ipc-metadata-list--baseAlt')
directors = importantpeople.find_all('li', class_ = 'ipc-metadata-list__item')

#for test in directors:
#    print(test.text)

# prints all the attributes that title has
# print(title.attrs)


