# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 00:46:37 2022

@author: JD
"""

from bs4 import BeautifulSoup
import requests

movieID = 0

imdb_url = 'https://www.imdb.com'
#coda movie url
#url = 'https://www.imdb.com/title/tt10366460/?ref_=adv_li_tt'

#The Lost city movie url
url = 'https://www.imdb.com/title/tt13320622/?ref_=adv_li_tt'

#our flag means death tv show url
#url = 'https://www.imdb.com/title/tt11000902/?ref_=adv_li_tt'


soup = BeautifulSoup(requests.get(url).text,'lxml')

# variables are named to match the names of the attributes of the relation schema
# budget: there is no budget listing for movies
movieID = url[27:37]
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
#aspectratio = soup.find('li', attrs= {'data-testid' : 'title-techspec_aspectratio'}).find('div').text # aspectratio


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
#print(aspectratio)



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
""" ------------------------------- end cast ------------------------------------"""

prodCompanieslist = soup.find('li', attrs={'data-testid' : 'title-details-companies'}).find('ul').find_all('li') # production company
temp2 = ""
for x in prodCompanieslist:
    temp2 = temp2 + x.text + ', '
productionCompanies = temp2[:-2]
print(productionCompanies)

genresoup = soup.find('li', attrs={'data-testid' : 'storyline-genres'}).find_all('li')
genres = []
for x in genresoup:
    genres.append(x.text)
print(genres)

#print(releaseDate)
#grossing = soup.find_all('span', class_ = 'ipc-metadata-list-item__list-content-item')
#for x in grossing:
#    print(x.text)

#for tag in releaseDate.find_all(True):
#    print(tag.name)


#print(grossing)
