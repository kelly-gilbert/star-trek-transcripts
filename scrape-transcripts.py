# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 21:09:09 2020

@author: Kelly
"""

import requests
from bs4 import BeautifulSoup

url_list = [('Star Trek', 'http://www.chakoteya.net/StarTrek/episodes.htm'),
            ('Deep Space Nine', 'http://www.chakoteya.net/DS9/episodes.htm'),
            ('Voyager', 'http://www.chakoteya.net/Voyager/episode_listing.htm'),
            ('Enterprise', 'http://www.chakoteya.net/Enterprise/episodes.htm')]

u = url_list[2]


# cycle through the URLs
df_scripts = None
for u in url_list:
    series_name = u[0]
    
    r = requests.get(u[1], headers={'User-Agent': 'Custom'})

    if r.status_code != 200:    # not successful
        print('Error ' + str(r.status_code) + ': ' + url_list[i])
        continue
    
    
    soup = BeautifulSoup(r.text, 'lxml')
        
    # find the first cell of the outer table, and create a list of its
    # contents (excluding elements that are only whitespace)
    outer_cell = soup.find('table').find('td')
    elements = [e for e in outer_cell.children if str(e).strip() != '']

    # cycle through the elements, recording h2/table pairs
    for e in range(0, len(elements)):       
        
        if str(elements[e])[0:4] == '<h2>':
            season = elements[e].text.strip()            
            df = read_html(str(elements[e+1]))[0]
            df['season'] = season
            df['series_name'] = series_name
            
            # get the URLs for each episode
            str(elements[e+1])
            
            # cycle through the URLs and get the script text
            
            
            # union the new data to the main dataframe

        # skip the next element (the table)
        e = e + 2
            
    

        
         = list(outer_table.children)
        len(c) 
        c[5]
        len(children)
        
        type(children[3])
        
        
        
        c2 = [x for x in c if x != '\n']
        outer_table2 = list(outer_table.children)[1]
 
type(c)

        
        # find the outer table
        outer = soup.find('table')
        
        
        df = read_html(str(outer))
        df        
        

        # get the season header
        season = outer.find('h2').text.strip()
        
        
        
        
        t = soup.find('table').find('table')
        t
        str(t)
        type(t)
        t.dtype()      


        df = read_html(str(t))
        df
        len(df)
        
        album.text.strip()
        try:
            album = album.find_all('a')[1].get('title')[9:]
        except:
            album = 'Unknown'
        song_dict['album'] = album
        
        # get the lyrics
        try:
            lyrics = soup.find(class_='lyricbox')
            lyrics = chr(10).join(lyrics.stripped_strings)
        except:
            lyrics = ''
        song_dict['lyrics'] = lyrics
        
        return song_dict
        

from pandas import read_html

df = read_html('http://www.chakoteya.net/Voyager/episode_listing.htm', match='Season')
df
df[1]




df[0].iloc[0]

len(df)
df[7].columns

new_header = df[0].iloc[0] 

df = df[1:] 

df.columns = new_header