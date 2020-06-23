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
import re



def clean_text(obj):
    if type(obj).__name__ == 'NavigableString':
        o = obj
    else:
        o = obj.text 
        
    return o.strip()    







url_list = [('Star Trek', 'http://www.chakoteya.net/StarTrek/episodes.htm'),
            ('Deep Space Nine', 'http://www.chakoteya.net/DS9/episodes.htm'),
            ('Voyager', 'http://www.chakoteya.net/Voyager/episode_listing.htm'),
            ('Enterprise', 'http://www.chakoteya.net/Enterprise/episodes.htm')]


u = url_list[2]    #temp

# cycle through the series URLs and get the list of episode URLs
df_scripts = None

for u in url_list[2:3]:
    series_name = u[0]
    url_prefix = re.search('(.*\/)(.*)', u[1])[1]   
    
    # get the contents of the episode listing page    
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
    e = 0
    while e < len(elements):       
        print('processing element ' + str(e))
        print(str(elements[e])[0:100])
        if str(elements[e])[0:3].strip() == '<h2':
            print('element ' + str(e) + ' is a header')
            # get the season name from the header
            season = elements[e].text.strip()            
            
            # get the season episode list from the next element in the table
            df = pd.read_html(str(elements[e+1]))[0]
            
            #rename cols using first row
            cols = [c.strip().lower().replace(' ', '_') for c in df.iloc[0]]
            df = df[1:]
            df.columns = cols
            
            # add series and season
            df['series_name'] = series_name
            df['season'] = season
            
            # get the URLs for each episode and add them to the main dataframe
            links = pd.Series([str(s) for s in elements[e+1].find_all('a')])
            links = links.str.extract(r'<a href="(?P<link>\d+\.htm)">(?P<episode_name>.*?)</a>')
            links['link'] = url_prefix + links['link']
            
            df = df.merge(links, how='left', on='episode_name') 
 
            # union the new data to the main dataframe
            df_scripts = pd.concat([df_scripts, df])

            # skip the next element (the table)
            e += 2
            continue

    else:    # not a season header
        e += 1
        
        
# cycle through the episode links and parse the transcripts into blocks        
link = df_scripts['link'].iloc[0]

for link in df_scripts['link']:              
    # get the html contents for the episode transcript
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'lxml')

    script_lines = pd.DataFrame( {'row_text' : [clean_text(c) for c in soup.td.contents]} )

    # if \r\n is followed by open parenthesis or capital letters followed by :, 
    # then replace with a line break, \n. Otherwise, replace with a space.
    script_lines['row_text'] = script_lines['row_text'].str.replace('\r\n(?=(\(|[A-Z]+\:))', '\n', regex=True)
    script_lines['row_text'] = script_lines['row_text'].str.replace('\r\n', ' ', regex=True)
    
    # split individual lines into lists
    script_lines['row_text'] = [r.split('\n') for r in script_lines['row_text']] 
    
    # break the lists into separate rows
    script_lines = script_lines.explode('row_text')   

    # remove rows that are just whitespace 
    script_lines = script_lines[script_lines['row_text'].str.strip() != '']
    
    # label the rows
    script_lines['row_type'] = np.where(script_lines['row_text'].str[0] == '[', 'scene location', 
                                 np.where(script_lines['row_text'].str[0] == '(', 'description', 
                                   np.where(script_lines['row_text'].str, '', '')))   #, 

            
    script_lines.head()
  
    # copy down scene location
    
    # parse speaker from lines
    
    # add link for joining
    
    # end columns: line, speaker, scene location, link (for joining)
    # other types of lines (e.g. description of action) will have speaker = null
  
    # union to main lines dataset
    
    
    
# merge with main dataset
  
    
  
    

    script_lines['link'] = link

script_lines['row_text'].iloc[300]




            
    

        
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