# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 00:46:37 2022

@author: JD

Description:
    This file is basically what is going to be copy pasted into the getMovieInfo() function in webscrapetesting
    its supposed to scrape all the data/variables we need from a movie page


"""



import pickle
from bs4 import BeautifulSoup
import requests
import pandas as pd

movieID = 0

imdb_url = 'https://www.imdb.com'
#coda movie url
#url = 'https://www.imdb.com/title/tt10366460/?ref_=adv_li_tt'

#The Lost city movie url
#url = 'https://www.imdb.com/title/tt13320622/?ref_=adv_li_tt'

#our flag means death tv show url
#url = 'https://www.imdb.com/title/tt11000902/?ref_=adv_li_tt'
castlinks = []

# test1.p holds movielinks data in a set of size 1162, and pulled links from comedy, scifi, horror and romance
pickle_in = open('moviePagelinks_small.p', 'rb')
movieLinks = pickle.load(pickle_in)
pickle_in.close()

#url = 'https://www.imdb.com/title/tt1570728/'
#movieLinks = [url]

global moviedf
moviedf = pd.DataFrame(columns=['mID','name','releaseDate', 'popularity_score',
                           'popularity_delta','color','runtime','aspectratio','imdb_rating',
                           'grossingUS_CA','grossingUS_CA_OpeningWeekend','grossingWorldwide',
                           ])
def moviedf_row(mid, name, rd, ps, pd, col, runt, asp, rating, us_ca, us_ca_op, world):
    row = {'mID':mid,'name':name,'releaseDate':rd,'popularity_score':ps,
           'popularity_delta':pd,'color':col,'runtime':runt,'aspectratio':asp,'imdb_rating':rating,
           'grossingUS_CA':us_ca,'grossingUS_CA_OpeningWeekend':us_ca_op,'grossingWorldwide':world}
    return row

global companyID
companyID = 0
movieproductioncompanydf = pd.DataFrame(columns=['companyID', 'mID', 'name'])
def movieproductioncompanydf_row(companyID, mID, name):
    row = {'companyID':companyID, 'mID':mID, 'name':name}
    return row

movieKeywordsdf = pd.DataFrame(columns=['keyword', 'mID'])
def movieKeywordsdf_row(keyword,mID):
    row = {'keyword':keyword, 'mID':mID}
    return row

movieGenresdf = pd.DataFrame(columns=['genre', 'mID'])
def movieGenresdf_row(genre,mID):
    row = {'genre':genre, 'mID':mID}
    return row

movieLanguagesdf = pd.DataFrame(columns=['language', 'mID'])
def movieLanguagesdf_row(language,mID):
    row = {'language':language, 'mID':mID}
    return row

global locationID
locationID = 0
locationsdf = pd.DataFrame(columns=['locationID', 'name', 'country'])
def locationsdf_row(locationID, name, country):
    row = {'locationID': locationID, 'name':name, 'country':country}
    return row

movieFilmedAtdf = pd.DataFrame(columns=['locationID', 'mID'])
def movieFilmedAtdf_row(locationID, mID):
    row = {'locationID':locationID, 'mID':mID}
    return row

for url in movieLinks:
    
    soup = BeautifulSoup(requests.get(url).text,'lxml')
    print(url)
    # variables are named to match the names of the attributes of the relation schema
    # budget: there is no budget listing for movies
    movieID = url[27:-1]
    
    #initialize every variable to None
    title = None
    grossingUS_CA = None
    grossingUS_CA_OpeningWeekend = None
    grossingWorldwide = None
    releaseDate = None
    countriesOfOrigin = None
    imdb_rating = None
    popularity_score = None
    popularity_delta = None
    runtime = None
    color = None
    aspectratio = None
    productionCompanies = None
    genres = None
    keywords = None
    languages = None
    filmedAt = None
    directors = None
    writers = None
    
    
    title = soup.find('h1', attrs={'data-testid' : 'hero-title-block__title'}).text #name
    
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
    releaseDatesoup = soup.find('li', attrs={'data-testid' : 'title-details-releasedate'})
    if(releaseDatesoup != None): releaseDate = releaseDatesoup.a.find_next_sibling().text # release dat
    countriesOfOriginsoup = soup.find('li', attrs={'data-testid' : 'title-details-origin'})
    if(countriesOfOriginsoup != None): 
        countriesOfOrigin = countriesOfOriginsoup.find_all('li') # countries of origin
        # temp variables initialized to make countires of origin
        temp2 = ""
        for x in countriesOfOrigin:
            temp2 = temp2 + x.text + ", "
            countries_of_origin = temp2[:-2] # removes the last comma and space

    ratingsoup = soup.find('div', attrs={'data-testid' : 'hero-rating-bar__aggregate-rating__score'})
    if(ratingsoup != None): imdb_rating = ratingsoup.text.split('/')[0] # imdb rating
    
    popularitysoup_s = soup.find('div', attrs={'data-testid' : 'hero-rating-bar__popularity__score'})
    if(popularitysoup_s != None): popularity_score = popularitysoup_s.text #popularity score
    popularitysoup_d = soup.find('div', attrs={'data-testid' : 'hero-rating-bar__popularity__delta'})
    if(popularitysoup_d != None): popularity_delta = popularitysoup_d.text #popularity delta
    
    runtimesoup = soup.find('li', attrs={'data-testid' : 'title-techspec_runtime'})
    if(runtimesoup != None): runtime = runtimesoup.find('div').text #runtime
    
    colorsoup =soup.find('li', attrs={'data-testid' : 'title-techspec_color'})
    if(colorsoup != None): color = colorsoup.find('li').text # color
        
    soundmixsoup = soup.find('li', attrs= {'data-testid' : 'title-techspec_soundmix'})
    if(soundmixsoup != None): soundmix = soundmixsoup.find('div').text # aspectratio
    
    aspectratiosoup = soup.find('li', attrs= {'data-testid' : 'title-techspec_aspectratio'})
    if(aspectratiosoup != None): aspectratio = aspectratiosoup.find('div').text # aspectratio
    
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
    
    
    """ ------------------------------- cast --------------------------------------- """
    top_castlist = soup.find_all('a', attrs={'data-testid' : 'title-cast-item__actor'})
    
    if(top_castlist != None):
        for n in top_castlist:
            castlinks.append((imdb_url + n.get('href'),movieID))
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
    
    prodsoup = soup.find('li', attrs={'data-testid' : 'title-details-companies'})
    if(prodsoup != None):
        prodlist = prodsoup.find('ul').find_all('li') # production companies
        productionCompanies = [x.text for x in prodlist]
    
    genresoup = soup.find('li', attrs={'data-testid' : 'storyline-genres'})
    if(genresoup != None):
        genrelist = genresoup.find_all('li') # genres
        genres = [x.text for x in genrelist] 
    
    # it only takes the 5 keywords displayed on the page, getting the rest will require navigating to another link, which
    # takes a little while computationally
    keywordsoup = soup.find('div', attrs={'data-testid' : 'storyline-plot-keywords'})
    if(keywordsoup != None):
        keywordlist = keywordsoup.find_all('a') # keywords
        keywords = [x.text for x in keywordlist[:-1]] # if you take keywordsoup you get the '5 more keywords...' item, so i took out the last item
    
    langsoup = soup.find('li', attrs={'data-testid' : 'title-details-languages'})
    if(langsoup != None):
        langslist = langsoup.find('ul').find_all('li')
        languages = [x.text for x in langslist]
    
    filmedatsoup = soup.find('li', attrs={'data-testid' : 'title-details-filminglocations'})
    if(filmedatsoup != None):
        filmedatlocations = filmedatsoup.find('ul').find_all('li')
        filmedAt = [x.text for x in filmedatlocations]
    
    importantpeoplesoup = soup.find('div', attrs={'data-testid' : 'title-pc-wide-screen'})
    if(importantpeoplesoup!= None):
        importantpeoplesoup = importantpeoplesoup.find_all('li', attrs={'data-testid': 'title-pc-principal-credit'})
        for x in importantpeoplesoup:
            
            if(x.span != None):
                if(x.span.text == 'Directors' or x.span.text == 'Director'):
                    directorsoup = x.find_all('li', class_ = 'ipc-inline-list__item')
                    if(directorsoup != None):
                        directors = [x.a.text for x in directorsoup]
                if(x.span.text == 'Writers' or x.span.text == 'Writer'):
                    writersoup = x.find_all('li', class_ = 'ipc-inline-list__item')
                    if(writersoup != None):
                        writers = [x.a.text for x in writersoup]
            if(x.a != None):
                if(x.a.text == 'Writers' or x.a.text == 'Writer'):
                    writersoup = x.find_all('li', class_ = 'ipc-inline-list__item')
                    if(writersoup != None):
                        writers = [x.a.text for x in writersoup]

    """
    print(productionCompanies)
    print(genres)
    print(keywords)
    print(languages)
    print(filmedAt)
    print(directors)
    print(writers)
    print()
    """

    
    
    """ ---------------- adding data into the dataframe then exporting that dataframe as a csv --------------"""
    
    
    
    moviedf = moviedf.append(
                    moviedf_row(movieID, title, releaseDate,
                    popularity_score,popularity_delta,color,runtime,
                    aspectratio, imdb_rating, grossingUS_CA,
                    grossingUS_CA_OpeningWeekend, grossingWorldwide), ignore_index=True
                    )
    
    if(productionCompanies!=None):
        for i in productionCompanies:
            #https://stackoverflow.com/questions/30944577/check-if-string-is-in-a-pandas-dataframe
            if(~movieproductioncompanydf['name'].str.contains(i).any()):
                companyID = companyID + 1
                movieproductioncompanydf = movieproductioncompanydf.append(
                        movieproductioncompanydf_row(companyID,movieID, i), ignore_index = True)
    if(keywords!=None):
        for i in keywords:
            movieKeywordsdf = movieKeywordsdf.append(
                        movieKeywordsdf_row(i,movieID), ignore_index = True)
    
    if(genres!=None):
        for i in genres:
            movieGenresdf = movieGenresdf.append(
                        movieGenresdf_row(i,movieID), ignore_index = True)
       
    if(languages!=None):
        for i in languages:
            movieLanguagesdf = movieLanguagesdf.append(
                movieLanguagesdf_row(i,movieID), ignore_index = True)
    
    if(filmedAt!=None):
        for i in filmedAt:
            country = i.split(',')[-1].strip()
            if(country!=i):
                name = i.split(',')[-2].strip()
            else:
                name = i
            
            if(~locationsdf['name'].str.contains(name).any()):
                locationID = locationID + 1
                locationsdf = locationsdf.append(
                        locationsdf_row(locationID,name,country), ignore_index = True)
            
            
    
"end for"

moviedf.to_csv(r'movies.csv', index=False)
movieproductioncompanydf.to_csv(r'movieProductionCompanies.csv', index=False)
movieKeywordsdf.to_csv(r'movieKeywords.csv', index=False)
movieGenresdf.to_csv(r'movieGenres.csv', index=False)
movieLanguagesdf.to_csv(r'movieLanguages.csv', index=False)
locationsdf.to_csv(r'locations.csv', index = False)