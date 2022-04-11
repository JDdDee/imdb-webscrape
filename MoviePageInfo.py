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
import numba
from numba import jit

movieID = 0

imdb_url = 'https://www.imdb.com'
#coda movie url
#url = 'https://www.imdb.com/title/tt10366460/?ref_=adv_li_tt'

#The Lost city movie url
#url = 'https://www.imdb.com/title/tt13320622/?ref_=adv_li_tt'

#our flag means death tv show url
#url = 'https://www.imdb.com/title/tt11000902/?ref_=adv_li_tt'
actorlinks = []
directorlinks = []
writerlinks = []

# test1.p holds movielinks data in a set of size 1162, and pulled links from comedy, scifi, horror and romance
pickle_in = open('moviePagelinks.p', 'rb')
movieLinks = pickle.load(pickle_in)
pickle_in.close()

#url = 'https://www.imdb.com/title/tt11138512/'
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


locationID = 0
locationsdf = pd.DataFrame(columns=['locationID', 'name', 'country'])

def locationsdf_row(locationID, name, country):
    row = {'locationID': locationID, 'name':name, 'country':country}
    return row

movieFilmedAtdf = pd.DataFrame(columns=['locationID', 'mID'])

def movieFilmedAtdf_row(locationID, mID):
    row = {'locationID':locationID, 'mID':mID}
    return row

def convertRuntimeToMinutes(runtime):
    if(runtime):
        test = 0
        test2 = 0
        if(runtime.split('hour')[0] != runtime):
            test = runtime.split('hour')[0]
        if(runtime.split('minute')[0] != runtime):
            if(int(test)>1):
                test2 = (runtime.split('minute')[0]).split('hours')[-1].strip()
            else:
                test2 = (runtime.split('minute')[0]).split('hour')[-1].strip()
        
    return (int(test)*60 + int(test2))

for url in movieLinks:
    
    soup = BeautifulSoup(requests.get(url).text,'lxml')
    print(url)
    # variables are named to match the names of the attributes of the relation schema
    # budget: there is no budget listing for movies
    movieID = url[29:-1]
    
    #initialize every variable to None
    title, grossingUS_CA, grossingUS_CA_OpeningWeekend, grossingWorldwide, releaseDate, countriesOfOrigin, imdb_rating, popularity_score, popularity_delta, runtime, color, aspectratio, productionCompanies, genres, keywords, languages, filmedAt, directors, writers = None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None
    
    """
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
    """
    
    titlesoup = soup.find('h1', attrs={'data-testid' : 'hero-title-block__title'})
    if(titlesoup):
        title = titlesoup.text #name
    
    temp = soup.find('div', attrs={'data-testid' : 'title-boxoffice-section'}) # grossing info

    if(temp):
        grossingUS_CA = temp.find('li', attrs={'data-testid' : 'title-boxoffice-grossdomestic'})
        if(grossingUS_CA):
            grossingUS_CA = grossingUS_CA.find('li').text.split('$')[-1]
        grossingUS_CA_OpeningWeekend = temp.find('li', attrs={'data-testid' : 'title-boxoffice-openingweekenddomestic'})
        if(grossingUS_CA_OpeningWeekend):
            grossingUS_CA_OpeningWeekend = grossingUS_CA_OpeningWeekend.find('li').text.split('$')[-1]
        grossingWorldwide = temp.find('li', attrs={'data-testid' : 'title-boxoffice-cumulativeworldwidegross'})
        if(grossingWorldwide):
            grossingWorldwide = grossingWorldwide.find('li').text.split('$')[-1]
    
    # had to use attrs={key : value} because the key had a hypen in it and python doesnt like that
    releaseDatesoup = soup.find('li', attrs={'data-testid' : 'title-details-releasedate'})
    if(releaseDatesoup): releaseDate = releaseDatesoup.a.find_next_sibling().text.split('(')[0][:-1] # release date
    countriesOfOriginsoup = soup.find('li', attrs={'data-testid' : 'title-details-origin'})
    if(countriesOfOriginsoup): 
        countriesOfOrigin = countriesOfOriginsoup.find_all('li') # countries of origin
        # temp variables initialized to make countires of origin
        temp2 = ""
        for x in countriesOfOrigin:
            temp2 = temp2 + x.text + ", "
            countries_of_origin = temp2[:-2] # removes the last comma and space

    ratingsoup = soup.find('div', attrs={'data-testid' : 'hero-rating-bar__aggregate-rating__score'})
    if(ratingsoup): imdb_rating = ratingsoup.text.split('/')[0] # imdb rating
    
    popularitysoup_s = soup.find('div', attrs={'data-testid' : 'hero-rating-bar__popularity__score'})
    if(popularitysoup_s): popularity_score = popularitysoup_s.text #popularity score
    popularitysoup_d = soup.find('div', attrs={'data-testid' : 'hero-rating-bar__popularity__delta'})
    if(popularitysoup_d): popularity_delta = popularitysoup_d.text #popularity delta
    
    runtimesoup = soup.find('li', attrs={'data-testid' : 'title-techspec_runtime'})
    if(runtimesoup): 
        runtimestring = runtimesoup.find('div').text #runtime
        runtime = convertRuntimeToMinutes(runtimestring)
    
    colorsoup =soup.find('li', attrs={'data-testid' : 'title-techspec_color'})
    if(colorsoup): color = colorsoup.find('li').text # color
        
    soundmixsoup = soup.find('li', attrs= {'data-testid' : 'title-techspec_soundmix'})
    if(soundmixsoup): soundmix = soundmixsoup.find('div').text # aspectratio
    
    aspectratiosoup = soup.find('li', attrs= {'data-testid' : 'title-techspec_aspectratio'})
    if(aspectratiosoup):
        aspectratio = aspectratiosoup.find('div').text.replace(" ","") # aspectratio
    
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
    
    if(top_castlist):
        for n in top_castlist:
            actorlinks.append((imdb_url + n.get('href'),movieID))
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
    if(prodsoup):
        prodlist = prodsoup.find('ul').find_all('li') # production companies
        productionCompanies = [x.text for x in prodlist]
    
    genresoup = soup.find('li', attrs={'data-testid' : 'storyline-genres'})
    if(genresoup):
        genrelist = genresoup.find_all('li') # genres
        genres = [x.text for x in genrelist] 
    
    # it only takes the 5 keywords displayed on the page, getting the rest will require navigating to another link, which
    # takes a little while computationally
    keywordsoup = soup.find('div', attrs={'data-testid' : 'storyline-plot-keywords'})
    if(keywordsoup):
        keywordlist = keywordsoup.find_all('a') # keywords
        keywords = [x.text for x in keywordlist[:-1]] # if you take keywordsoup you get the '5 more keywords...' item, so i took out the last item
    
    langsoup = soup.find('li', attrs={'data-testid' : 'title-details-languages'})
    if(langsoup):
        langslist = langsoup.find('ul').find_all('li')
        languages = [x.text for x in langslist]
    
    filmedatsoup = soup.find('li', attrs={'data-testid' : 'title-details-filminglocations'})
    if(filmedatsoup):
        filmedatlocations = filmedatsoup.find('ul').find_all('li')
        filmedAt = [x.text for x in filmedatlocations]
    
    importantpeoplesoup = soup.find('div', attrs={'data-testid' : 'title-pc-wide-screen'})
    if(importantpeoplesoup):
        importantpeoplesoup = importantpeoplesoup.find_all('li', attrs={'data-testid': 'title-pc-principal-credit'})
        for x in importantpeoplesoup:
            
            if(x.span):
                if(x.span.text == 'Directors' or x.span.text == 'Director'):
                    directorsoup = x.find_all('li', class_ = 'ipc-inline-list__item')
                    if(directorsoup):
                        directorlinks.append([x.a.get('href') for x in directorsoup])
                if(x.span.text == 'Writers' or x.span.text == 'Writer'):
                    writersoup = x.find_all('li', class_ = 'ipc-inline-list__item')
                    if(writersoup):
                        writerlinks.append([x.a.get('href') for x in writersoup])
            if(x.a):
                if(x.a.text == 'Writers' or x.a.text == 'Writer'):
                    writersoup = x.find_all('li', class_ = 'ipc-inline-list__item')
                    if(writersoup):
                        writerlinks.append([x.a.get('href') for x in writersoup])

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
    
    if(productionCompanies):
        for i in productionCompanies:
            #https://stackoverflow.com/questions/30944577/check-if-string-is-in-a-pandas-dataframe
            if(~movieproductioncompanydf['name'].str.contains(i).any()):
                companyID = companyID + 1
                movieproductioncompanydf = movieproductioncompanydf.append(
                        movieproductioncompanydf_row(companyID,movieID, i), ignore_index = True)
    if(keywords):
        for i in keywords:
            movieKeywordsdf = movieKeywordsdf.append(
                        movieKeywordsdf_row(i,movieID), ignore_index = True)
    
    if(genres):
        for i in genres:
            movieGenresdf = movieGenresdf.append(
                        movieGenresdf_row(i,movieID), ignore_index = True)
       
    if(languages):
        for i in languages:
            movieLanguagesdf = movieLanguagesdf.append(
                movieLanguagesdf_row(i,movieID), ignore_index = True)
    
    if(filmedAt):
        for i in filmedAt:
            country = i.split(',')[-1].strip()
            if(country!=i):
                name = i.split(',')[-2].strip()
            else:
                name = i
            

            #if(~locationsdf['name'].str.contains(name).any()):
            if((locationsdf[locationsdf['name'] == name]).empty):
                locationID = locationID + 1
                locationsdf = locationsdf.append(
                        locationsdf_row(locationID,name,country), ignore_index = True)
            
            #print(name + ' ' + country)
    
            locID = (locationsdf [ (locationsdf['name']  == name)])['locationID'].iloc[0]
            movieFilmedAtdf = movieFilmedAtdf.append(
                        movieFilmedAtdf_row(locID,movieID), ignore_index = True)
    else:
        movieFilmedAtdf = movieFilmedAtdf.append(
                        movieFilmedAtdf_row(None,movieID), ignore_index = True)
    
    moviedf.to_csv(r'csvs/movies.csv', index = False)
    movieproductioncompanydf.to_csv(r'csvs/movieProductionCompanies.csv', index = False)
    movieKeywordsdf.to_csv(r'csvs/movieKeywords.csv', index = False)
    movieGenresdf.to_csv(r'csvs/movieGenres.csv', index = False)
    movieLanguagesdf.to_csv(r'csvs/movieLanguages.csv', index = False)
    locationsdf.to_csv(r'csvs/locations.csv', index = False)
    movieFilmedAtdf.to_csv(r'csvs/moviesFilmedAt.csv', index = False)
    
    with open('actorlinks.p', 'wb') as handle:
        pickle.dump(actorlinks, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    with open('directorlinks.p', 'wb') as handle:
        pickle.dump(directorlinks, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    with open('writerlinks.p', 'wb') as handle:
        pickle.dump(writerlinks, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
"end for"


