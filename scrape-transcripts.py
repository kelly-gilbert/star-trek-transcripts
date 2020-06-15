# -*- coding: utf-8 -*-
"""
scrape-transcripts.py

Scrapes Star Trek episode transcripts from chakoteya.net

Author: Kelly Gilbert
Created: 2020-06-13
Requirements: 
    - pandas 0.25 or higher
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

url_list = [('Star Trek', 'http://www.chakoteya.net/StarTrek/episodes.htm'),
            ('Deep Space Nine', 'http://www.chakoteya.net/DS9/episodes.htm'),
            ('Voyager', 'http://www.chakoteya.net/Voyager/episode_listing.htm'),
            ('Enterprise', 'http://www.chakoteya.net/Enterprise/episodes.htm')]

u = url_list[2]    #temp


# cycle through the series URLs
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

    # the page is made up of an outer table, containing season headers and season tables.
    # cycle through the elements of the HTML table, recording header/table pairs
    e = 1   # temp

    for e in range(0, len(elements)):       
                
        if str(elements[e])[0:4] == '<h2>':
            season = elements[e].text.strip()            
            df = pd.read_html(str(elements[e+1]))[0]
            
            #rename cols using first row
            cols = [c.strip().lower().replace(' ', '_') for c in df.iloc[0]]
            df = df[1:]
            df.columns = cols
            
            # add series and season
            df['series_name'] = series_name
            df['season'] = season
            
            # get the URLs for each episode
            links = pd.Series([str(s) for s in elements[e+1].find_all('a')])
            links = links.str.extract(r'<a href="(?P<link>\d+\.htm)">(?P<episode_name>.*?)</a>')
            
            # cycle through the URLs and get the script text
            
            r2 = requests.get('http://www.chakoteya.net/Voyager/119.htm')
            soup = BeautifulSoup(r2.text, 'lxml')
            
            c = pd.DataFrame([c for c in list(soup.td.contents) if str(c).strip() != ''])
            
            
            pd. __version__
            
            
            len(c)      
            
            c['row_text'] = [t.text.strip() for t in c[0]]
            
            # if \r\n is followed by open parenthesis or a capital letter, then
            # replace it with a line break, \n. Otherwise, replace with a space.
            c['row_text'] = c['row_text'].str.replace('\r\n(?=(\(|[A-Z]+\:))', '\n', regex=True)
            c['row_text'] = c['row_text'].str.replace('\r\n', ' ', regex=True)
            c['row_text'] = [r.split('\n') for r in c['row_text']]
            
            # break the lines into separate rows
            c.explode('row_text')
            
            c['row_type'] = np.where(c['row_text'].str[0] == '[', 'scene start', 
                              np.where(c['row_text'].str[0] == '(', 'action', 'other'))
            
            c['row_text2'] = c['row_text'].str.replace('(?<=\s)\r\n', 'xxxx', regex=True)
            c['row_text2'].iloc[1]

            c['row_text'].iloc[1]
 
             \r\n followed by capital or ( --> replace with \n
             \r\n otherwise --> replace with space


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