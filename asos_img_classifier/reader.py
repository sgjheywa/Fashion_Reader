
#### 1 reader.py
# class for crawler that runs through asos website

import requests
from bs4 import BeautifulSoup
import ssl
import urllib.request, urllib.parse, urllib.error
from urllib.parse import urljoin, urlparse
import pandas as pd
import numpy as np
import time
import random
from PIL import Image

from asos import AsosObject

class AsosReader():
    """
    This is the main class to do the web crawling, it is given a set of headers 
    that work for the requests library.
    It is also given a site that would ideally allow for the extension to other 
    site crawling methods.
    """

    def __init__(self, headers, site, training_folder, pages=35):
        # headers are a list of headers for authorisation to access asos website without timeout
        # site is just an indicator for when multiple sites can be used
        # li is just for when the ehaders are being updated and part fo string needs to be removed
        self.headers = headers
        self.site = site
        self.li = 'https://'
        self.unique_id = 1
        self.folder = training_folder
        self.pages = pages

    def set_authority(self, auth):
        # function to update the website in the header, for example if website is asos 
        # auth = www.asos.comf2ACQ
        
        self.headers['authority'] = auth

    def update_headers(self, path):
        # function to update headers everytime a url is accessed, call by
        # grab_from_url
        head = self.li + self.headers['authority']
        path = path.replace(head,'')
        self.headers['path'] = path

    def get_sub_urls(self, fill_url):
        # function to read in url for products from mens new in asos
        # collects urls and returns python list
        # I realised that instead of clicking load more you can speicfy pages
        # still need to update for dynamic page count but figured out
        urls = []
        total_new_pages = self.pages #CHANGE  WITH DYNAMIC data-auto-id=productsProgressBar =x/70
        
        # for each page
        for i in range(total_new_pages):
            #build string    
            new_url = fill_url + str(i)
            # get html text
            response = self.grab_from_url(new_url)

            soup = BeautifulSoup(response.text, 'html.parser')
            # not sure how robust this is, find section with all products
            souptext = soup.find("div", {"data-auto-id" : "productList"})
            for link in souptext.findAll('a'):
                urls.append(link.get('href'))
        return urls

    def grab_from_url(self, url):
        # useful explanation of why straight request.get without header doesnt work
        # https://stackoverflow.com/questions/63428817/python-problem-of-web-scrapping-asos-error
        self.update_headers(url)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        response = requests.get(url, headers=self.headers)
        return response

    def get_asos_details(self, url):
        # from an indiviudal product page get details
        # still needs refinement for exact info
        response = self.grab_from_url(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        souptext = soup.find("div", {"class" : "product-details"})
        return souptext

    def get_asos_title(self, url):
        # from an indiviudal product page get details
        # still needs refinement for exact info
        response = self.grab_from_url(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        souptext = soup.find("div", {"class" : "product-hero"})
        if not souptext:
            souptext = "null"
        else:
            souptext = souptext.select('h1')[0].text.strip()
        return souptext

    def get_asos_image(self, url):
        # get images from page, needs to be finished and refined
        response = self.grab_from_url(url)
        # https://www.thepythoncode.com/article/download-web-page-images-python
        soup = BeautifulSoup(response.content, "html.parser")
        souptext = soup.find("div", {"class" : "product-carousel"})
        if souptext is None:
            return None
        imgurl = souptext.findAll("img")[0].attrs.get("src")
        img = self.get_img_from_url(imgurl)
        return img

    def get_img_from_url(self, imgurl):
        with urllib.request.urlopen(imgurl) as url:
            img = url.read()
        return img

    def get_items(self, urlset, gen_files=False, label=None):
        clothes = []
        print("number of URLs: ", len(urlset))

        for idx,url in enumerate(urlset):
            if (idx%250) == True:
                print("URL: ",idx)
            
            info = self.get_asos_title(url)
            img = self.get_asos_image(url)
            if img is None:
                continue 
            else:
                fname = self.folder + 'training_img_' + str(self.genID())+'.jpg'
                with open(fname, 'wb') as f:
                    f.write(img)
                
                clothes.append(AsosObject(info, img, idx, label, fname))

        return clothes

    def genID(self):
        unid = self.unique_id
        self.unique_id += 1
        return unid
