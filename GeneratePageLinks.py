# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 11:24:02 2022

@author: JD
"""

from bs4 import BeautifulSoup
import pickle
import requests

html_text = requests.get('https://www.imdb.com/search/title/?genres=comedy&start=1&explore=title_type,genres&ref_=adv_nxt').text
soup = BeautifulSoup(html_text, 'lxml')

imdb_url = 'https://www.imdb.com'
movietitleset = set()
TVtitleset = set()

def getNextPageURL(url):
    soup = BeautifulSoup(requests.get(url).text,'lxml')
    nextlink = imdb_url + soup.find('a', class_ ='lister-page-next next-page').get('href')
    return str(nextlink)
"end def"

def genTitleLinks(url):
    # this url is the one for comedy movies, if you want 1000 movies of a different genre, just swap this url
    url = url

    for i in range(0,100): # this range number can be modified to get a designated amt of links
        soup = BeautifulSoup(requests.get(url).text, 'lxml')
        
        
        moviecards = soup.find_all('div', class_ = 'lister-item-content')
        
        for m in moviecards:
            cert = m.find('span', class_ = 'certificate')
            if(cert != None):
                if(cert.text.find('TV') != -1): # if the card is a tv item
                    
                    TVtitleset.add(imdb_url + m.a.get('href'))
                else:
                    movietitleset.add(imdb_url + m.a.get('href'))
            else:
                movietitleset.add(imdb_url + m.a.get('href'))
                
        "end for"    
            
        url = getNextPageURL(url)
    "end for"

    #return movieLinkList, TVLinkList

"end def"


"""
links based definition
# get movie links
def genTitleLinks():
    # this url is the one for comedy movies, if you want 1000 movies of a different genre, just swap this url
    url = 'https://www.imdb.com/search/title/?genres=comedy&start=1&explore=title_type,genres&ref_=adv_nxt'
    
    movieLinks = []
    TVLinks = []
    for i in range(0,5): # this range number can be modified to get a designated amt of links
        soup = BeautifulSoup(requests.get(url).text, 'lxml')
        
        
        moviecards = soup.find_all('div', class_ = 'lister-item-content')
        
        for m in moviecards:
            cert = m.find('span', class_ = 'certificate')
            if(cert != None):
                if(cert.text.find('TV') != -1): # if the card is a tv item
                    
                    TVLinks.append(imdb_url + m.a.get('href'))
                else:
                    movieLinks.append(imdb_url + m.a.get('href'))
            else:
                movieLinks.append(imdb_url + m.a.get('href'))
                
        "end for"    
            
        url = getNextPageURL(url)
    "end for"
    
    with open('moviePagelinks.p', 'wb') as handle:
        pickle.dump(movieLinks, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    with open('TVShowPagelinks.p', 'wb') as handle2:
        pickle.dump(TVLinks, handle2, protocol=pickle.HIGHEST_PROTOCOL)

    #return movieLinkList, TVLinkList

"end def"
"""

def visitAllGenres():
    
    
    genrePage_urls = []
    
    comedyPage_url = 'https://www.imdb.com/search/title/?genres=comedy&start=1&explore=title_type,genres&ref_=adv_nxt'
    scifiPage_url = 'https://www.imdb.com/search/title/?genres=sci-fi&start=1&explore=title_type,genres&ref_=adv_nxt'
    horrorPage_url = 'https://www.imdb.com/search/title/?genres=horror&start=1&explore=title_type,genres&ref_=adv_nxt'
    romancePage_url = 'https://www.imdb.com/search/title/?genres=romance&start=1&explore=title_type,genres&ref_=adv_nxt'
    actionPage_url = 'https://www.imdb.com/search/title/?genres=action&start=1&explore=title_type,genres&ref_=adv_nxt'
    thrillerPage_url = 'https://www.imdb.com/search/title/?genres=thriller&start=1&explore=title_type,genres&ref_=adv_nxt'
    dramaPage_url = 'https://www.imdb.com/search/title/?genres=drama&start=1&explore=title_type,genres&ref_=adv_nxt'
    mysteryPage_url = 'https://www.imdb.com/search/title/?genres=mystery&start=1&explore=title_type,genres&ref_=adv_nxt'
    crimePage_url = 'https://www.imdb.com/search/title/?genres=crime&start=1&explore=title_type,genres&ref_=adv_nxt'
    animationPage_url = 'https://www.imdb.com/search/title/?genres=animation&start=1&explore=title_type,genres&ref_=adv_nxt'
    adventurePage_url = 'https://www.imdb.com/search/title/?genres=adventure&start=1&explore=title_type,genres&ref_=adv_nxt'
    fantasyPage_url = 'https://www.imdb.com/search/title/?genres=fantasy&start=1&explore=title_type,genres&ref_=adv_nxt'
    
    #genrePage_urlstest = [comedyPage_url, scifiPage_url, horrorPage_url, romancePage_url]
    
    genrePage_urls = [comedyPage_url, scifiPage_url, horrorPage_url, 
                      romancePage_url, actionPage_url, thrillerPage_url,
                      dramaPage_url, mysteryPage_url, crimePage_url, 
                      animationPage_url, adventurePage_url, fantasyPage_url]
    
    for p in genrePage_urls:
        genTitleLinks(p)
    
    
    with open('moviePagelinks.p', 'wb') as handle:
        pickle.dump(movietitleset, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('TVShowPagelinks.p', 'wb') as handle:
        pickle.dump(TVtitleset, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
"end def"



visitAllGenres()
