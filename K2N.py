'''
Created on 30th Apr.,2017
@author: Harry Zhang
'''

#the ending page will not be downloaded, it ends one before the end. It wil download the starting page
STARTING_PAGE = 7
ENDING_PAGE = 8
#this url can be changed, possibly for other pages like the Japan one
url = "https://k2nblog.com/category/single-album/k-pop/page/"
#don't be abusing the system people
WAIT_TIME = 2


import urllib.request
import urllib
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import re
import requests
from selenium import webdriver
import time
import socket



timeout = 20
socket.setdefaulttimeout(timeout)

# url2 = "https://k2nblog.com/varsity-1st-single-album-round-one-mp3/"
# url3 = """https://k2nblog.com/redirect.html?u=aHR0cHM6Ly9tZWRpYWZpcmUuY29tLz9kMTV2MWs1MnA1NWU5a2U=" target="_blank"""
# url4 = "http://www.mediafire.com/file/d15v1k52p55e9ke/VARSITY+-+VARSITY+1st+Single+Album+-+ROUND+ONE+%5Bwww.k2nblog.com%5D.7z"
# url5 = "http://download2230.mediafireuserdownload.com/d8xxrsdgccqg/d15v1k52p55e9ke/VARSITY+-+VARSITY+1st+Single+Album+-+ROUND+ONE+%5Bwww.k2nblog.com%5D.7z"

http = httplib2.Http()

def getlink(html):
    return re.findall(r'"(.+)"', html)[0]
     
def namify(link):
    link = re.findall(r'/(.+)', link)[0]
    link = re.findall(r'/(.+)', link)[0]
    name = re.findall(r"/(.+)/", link)[0]
    name = name.replace("-", " ")
    return name.upper()+".7z"
    
def get_song_url(lowerbound, upperbound):
    count = 0
    for i in range(lowerbound, upperbound):
        pageurl = url+str(i)+"/"
        status, response = http.request(pageurl)
        for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
            if "Read more" in link:
                time.sleep(WAIT_TIME)
                linkcount = 2
                count += 1
                print("*"*10+"COUNT: "+str(count)+"*"*10)                
                link = link.encode('utf-8')
                link = getlink(str(link))
                filename = namify(link)
                templink = link
                print("FILENAME: "+filename[:-3])
                while(1):
                    try:
                        if linkcount > 9:
                            break
                        link = get_adfly(templink, linkcount)
                        link = get_k2n_link(link)
                        link = get_mediafire(link)
                        print(" "*20+"Download link: "+str(link))
                        if "mediafire" in link.lower():
                            print(" "*5+"DOWNLOADING...")
                            link = get_dl_link(link)
                            download_file(link, filename)
                            print("FINISHED!")
                            break
                        else:
                           linkcount += 1
                           print(" "*5+"Trying next link")
                           continue 
                    except:
                        print("Error with downloading, trying another link")
                        linkcount += 1
                        
                
def get_adfly(url, linkcount):
    status, response = http.request(url)
    count = 0
    for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
        link = str(link.encode('utf-8'))
        if "ADF.LY" in link:
            count += 1
            if count == linkcount:
                return getlink(str(link))
            
def get_k2n_link(url):
    for i in range(0, 4):
        url = re.findall(r'/(.+)', url)[0]
    return url

def get_mediafire(url):
    driver = webdriver.Chrome()
    driver.get(url)
    original_url = driver.current_url
    print(" "*20+"k2n URL: " + original_url)
    count = 0
    while(1):
        count += 1
        if count > 4:
            redirected = driver.current_url
            driver.quit()
            return redirected
        time.sleep(5)
        print(" "*20+"Waiting for redirect...")
        print(" "*20+ "Current url: "+driver.current_url)
        if driver.current_url != original_url:
            redirected = driver.current_url
            driver.quit()
            return redirected
        
def get_dl_link(url):
    status, response = http.request(url)
    for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
        link = str(link.encode('utf-8'))
        if "YahooDownloadClick" in link:
            print(" "*20+"Size of file: "+re.findall(r'>\((.+MB)\)', link)[0])
            return re.findall(r'href="(.+)" on', link)[0]


def download_file(url, filename):
    response = urllib.request.urlopen(url)
    data = response.read()

    file_ = open(filename, 'wb')
    file_.write(data)
    file_.close()


get_song_url(STARTING_PAGE,ENDING_PAGE)