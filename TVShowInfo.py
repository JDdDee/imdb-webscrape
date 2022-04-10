# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 13:56:17 2022

@author: JD


goal of this file is to visit every tvshow page
"""

import pickle
from bs4 import BeautifulSoup
import requests

imdb_url = 'https://www.imdb.com'
#barry tv show url
url = 'https://www.imdb.com/title/tt5348176/'


soup = BeautifulSoup(requests.get(url).text,'lxml')



pickle_in = open('test2.p', 'rb')
#pickle_in = open('TVShowPagelinks.p', 'rb')
TVShowLinks = pickle.load(pickle_in)
pickle_in.close()

TVShowLinks = [url]

for url in TVShowLinks:
    # variables are named to match the names of the attributes of the relation schema
    # budget: there is no budget listing for movies
    TVShowID = url[27:-1]
    title = soup.find('h1', class_ = 'sc-b73cd867-0 eKrKux').text #name
    
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
    
    season_url = url + 'episodes?season=1'
    soup2 = BeautifulSoup(requests.get(season_url).text,'lxml')
    
    # we have to visit season 1 to get the number of seasons first
    seasonsoup = soup2.find('select', attrs={'id' : 'bySeason'}).find_all('option')
    count = 0
    for x in seasonsoup:
        count = count + 1
    No_Seasons = count
    print(No_Seasons)
    
    # get the info for season 1
    seasonNo = 1
    episodeNo = 0
    episodesoup = soup2.find('div', class_ = 'list detail eplist').find_all('div', class_ = 'info')
    for x in episodesoup:
        episodeNo = episodeNo + 1
        ep_releaseDate = x.find('div', class_ = 'airdate').text.strip() # .strip() method removes all random white spaces in the text
        episode_url = imdb_url + x.find('strong').a.get('href')
        print(episode_url)
        soup3 = BeautifulSoup(requests.get(episode_url).text, 'lxml')
        ep_runtime = soup3.find('li', attrs={'data-testid' : 'title-techspec_runtime'}).find('div').text #runtime
        
    
    # get the info for the rest of the seasons
    for i in range(2,No_Seasons+1):
        season_url = url + 'episodes?season=' + str(i)
        print(season_url)
        soup2 = BeautifulSoup(requests.get(season_url).text,'lxml')
        episodesoup = soup2.find('div', class_ = 'list detail eplist').find_all('div', class_ = 'info')
        for x in episodesoup:
            episodeNo = episodeNo + 1
            ep_releaseDate = x.find('div', class_ = 'airdate').text.strip() # .strip() method removes all random white spaces in the text
            episode_url = imdb_url + x.find('strong').a.get('href')
            print(episode_url)
            soup3 = BeautifulSoup(requests.get(episode_url).text, 'lxml')
            ep_runtime = soup3.find('li', attrs={'data-testid' : 'title-techspec_runtime'}).find('div').text #runtime






