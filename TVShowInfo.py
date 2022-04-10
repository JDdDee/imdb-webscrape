# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 13:56:17 2022

@author: JD
"""

import pickle
from bs4 import BeautifulSoup
import requests

#our flag means death tv show url
url = 'https://www.imdb.com/title/tt11000902/?ref_=adv_li_tt'


soup = BeautifulSoup(requests.get(url).text,'lxml')


pickle_in = open('test2.p', 'rb')
#pickle_in = open('TVShowPagelinks.p', 'rb')
TVShowLinks = pickle.load(pickle_in)
pickle_in.close()

# variables are named to match the names of the attributes of the relation schema
# budget: there is no budget listing for movies
TVShowID = url[27:37]
title = soup.find('h1', class_ = 'sc-b73cd867-0 eKrKux').text #name

temp = soup.find('div', attrs={'data-testid' : 'title-boxoffice-section'}) # grossing info
grossingUS_CA = None
grossingUS_CA_OpeningWeekend = None
grossingWorldwide = None
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



print(TVShowID)
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

prodsoup = soup.find('li', attrs={'data-testid' : 'title-details-companies'}).find('ul').find_all('li') # production companies
productionCompanies = [x.text for x in prodsoup]
print(productionCompanies)

genresoup = soup.find('li', attrs={'data-testid' : 'storyline-genres'}).find_all('li') # genres
genres = [x.text for x in genresoup]
print(genres)

# it only takes the 5 keywords displayed on the page, getting the rest will require navigating to another link, which
# takes a little while computationally
keywordsoup = soup.find('div', attrs={'data-testid' : 'storyline-plot-keywords'}).find_all('a') # keywords
keywords = [x.text for x in keywordsoup[:-1]] # if you take keywordsoup you get the '5 more keywords...' item, so i took out the last item
print(keywords)

langsoup = soup.find('li', attrs={'data-testid' : 'title-details-languages'}).find('ul').find_all('li')
languages = [x.text for x in langsoup]
print(languages)

filmedatlocations = soup.find('li', attrs={'data-testid' : 'title-details-filminglocations'}).find('ul').find_all('li')
filmedAt = [x.text for x in filmedatlocations]
print(filmedAt)

importantpeople = soup.find('div', class_ = 'sc-fa02f843-0 fjLeDR')
directorsoup = importantpeople.find('li').find_all('li', class_ = 'ipc-inline-list__item')
writersoup = importantpeople.find('li').find_next_sibling().find_all('li', class_ = 'ipc-inline-list__item')

directors = [x.text for x in directorsoup]
writers = [x.a.text for x in writersoup]
print(directors)
print(writers)

