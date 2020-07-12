# -*- coding: utf-8 -*-
"""
scrape-transcripts.py

Scrapes Star Trek episode transcripts from chakoteya.net

Author: Kelly Gilbert
Created: 2020-06-13
Requirements: 
    - pandas 0.25 or higher
"""

from bs4 import BeautifulSoup
from csv import QUOTE_ALL
import numpy as np
from os import chdir
import pandas as pd
import re
import requests



def clean_text(obj):
    if type(obj).__name__ == 'NavigableString':
        o = obj
    else:
        # replace line breaks with characters
        for br in obj.find_all(['br', 'p']):
            br.replace_with(br.text + '\n\n')
        o = obj.text 
        
    return o.strip()    



#------------------------------------------------------------------------------
# Setup
#------------------------------------------------------------------------------
    
# set the working directory
chdir('C:\\projects\\star-trek-transcripts\\')

# urls to scrape
urls = [('Star Trek', 'http://www.chakoteya.net/StarTrek/episodes.htm'),
            ('Deep Space Nine', 'http://www.chakoteya.net/DS9/episodes.htm'),
            ('Voyager', 'http://www.chakoteya.net/Voyager/episode_listing.htm'),
            ('Enterprise', 'http://www.chakoteya.net/Enterprise/episodes.htm')]



#------------------------------------------------------------------------------
# Get the list of episodes and export to csv
#------------------------------------------------------------------------------

# cycle through the series URLs and get the list of episode URLs
df_episodes = None    # initialize the episodes dataframe
for u in urls[2:3]:
    series_name = u[0]
    url_prefix = re.search('(.*\/)(.*)', u[1])[1]   
    
    # get the contents of the episode listing page    
    r = requests.get(u[1], headers={'User-Agent': 'Custom'})

    if r.status_code != 200:    # not successful
        print('Error ' + str(r.status_code) + ': ' + urls[u])
        continue
    
    soup = BeautifulSoup(r.text, 'lxml')
        
    # find the first cell of the outer table, and create a list of its
    # contents (excluding elements that are only whitespace)
    outer_cell = soup.find('table').find('td')
    elements = [e for e in outer_cell.children if str(e).strip() != '']

    # the page is made up of an outer table, containing season headers and season tables.
    # cycle through the elements of the HTML table, recording header/table pairs   

    # elements = elements in the main table of the page
    # df_season = temp dataframe containing the episode list for one season
    # df_episodes = the final dataframe that contains the list of episodes
    df_episodes = None
    e = 0
    while e < len(elements):       
        if str(elements[e])[0:3].strip() == '<h2':
            # get the season name from the header
            season = elements[e].text.strip()            
            
            # get the season episode list from the next element in the table
            df_season = pd.read_html(str(elements[e+1]))[0]
            
            #rename cols using first row
            cols = [c.strip().lower().replace(' ', '_') for c in df_season.iloc[0]]
            df_season = df_season[1:]
            df_season.columns = cols
            
            # clean episode name
            df_season['episode_name'].str.replace('\s+', ' ', regex=True)
            
            # add series and season
            df_season['series_name'] = series_name
            df_season['season'] = season
            
            
            # get the URLs for each episode and add them to the main dataframe
            df_links = pd.Series([str(s) for s in elements[e+1].find_all('a')])
            
            # clean up extra linebreaks and split into episode name and link
            df_links = df_links.str.replace('\s+', ' ', regex=True)
            df_links = df_links.str.extract(r'<a href="(?P<link>\d+\.htm.*?)">(?P<episode_name>.*?)</a>')
            df_links['link'] = url_prefix + df_links['link']
            
            # join back to season episode list on episode name
            df_season_links = df_season.merge(df_links, how='outer', on='episode_name') 
 
            # union the season to the main episode list
            df_episodes = pd.concat([df_episodes, df_season_links])

            # skip the next element (the table)
            e += 2
            continue

        else:    # not a season header - go to the next element
            e += 1
 

# export the episode list/URLs to csv
df_episodes.to_csv('.\\star-trek-esisode-list.csv', index=False, quoting=QUOTE_ALL)



#------------------------------------------------------------------------------
# Get and parse the individual transcripts
#------------------------------------------------------------------------------

# cycle through the episode links and parse the transcripts into lines        
#   df_episodes is the main listing of episodes with links to each transcript
#   df_scripts is the main dataframe of parsed scripts
#   df_curr is the current script being parsed
#   df_curr_rows is the current script, with lines parsed into separate rows

df_episodes = pd.read_csv('.\\star-trek-esisode-list.csv')

df_scripts = None
prev_link = '|||'
for link in df_episodes['link']:  
            
    # ignore continuations
    if prev_link in link:
        continue
    
    # get the html contents for the episode transcript
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'lxml')
  
    # parse the contents into a dataframe
    df_curr = pd.DataFrame( {'row_text' : [clean_text(c) for c in soup.td.contents]} )

    # if \r\n is followed by open parenthesis or capital letters followed by :, 
    # then replace with a line break, \n. 
    # Otherwise, replace \r\n with a space.
    # Replace tabs (\t) with empty string
    df_curr['row_text'] = df_curr['row_text'].str.replace('\t', '', regex=True)
    df_curr['row_text'] = df_curr['row_text'].str.replace('\r\n(?=(\(|[A-ZÀ-Ý\w\s\[\]\(\)]+\:))', '\n', regex=True)
    df_curr['row_text'] = df_curr['row_text'].str.replace('\r\n', ' ', regex=True)

    
    # split individual lines into lists
    df_curr['row_text'] = [r.split('\n') for r in df_curr['row_text']] 
    
    # break the lists into separate rows
    df_curr = df_curr.explode('row_text')   
    
    # remove rows that are just whitespace and strip the remaining rows
    df_curr['row_text'] = df_curr['row_text'].str.strip()
    df_curr = df_curr[df_curr['row_text'] != '']
    
    # extract the speaker from the line
    df_curr_rows = df_curr['row_text'].str.extract(r'(?P<speaker>[A-ZÀ-Ý\w\s\[\]\(\)]+(?=\: ))?\:? *(?P<line>.*)')
   
    
    # label the row types
    df_curr_rows['row_type'] = np.where(df_curr_rows['speaker'].isna() == False, 'line',
                                np.where(df_curr_rows['line'].str[0] == '[', 'scene description', 
                                 np.where(df_curr_rows['line'].str[0] == '(', 'description', 'other'))) 

    # move the scene description into its own column and copy down
    df_curr_rows['scene_description'] = np.where(df_curr_rows['row_type']=='scene description', 
                                                df_curr_rows['line'], np.nan)
    
    df_curr_rows['scene_description'].ffill(inplace=True)
    df_curr_rows = df_curr_rows[df_curr_rows['row_type'] != 'scene description']

    # add link for joining
    df_curr_rows['link'] = link
      
    # concatenate with previous script data
    df_scripts = pd.concat([df_scripts, df_curr_rows])
    
    prev_link = link
    


#------------------------------------------------------------------------------
# Clean up parsing issues
#------------------------------------------------------------------------------

# if speaker is [OC] only or "and...", then get the line from the previous row 
# and append it to the speaker name
# next, delete the previous row
missing_speaker = df_scripts[df_scripts['speaker'].str.match('\[.*\]$', na=False) 
                             | df_scripts['speaker'].str.match('^and .*', na=False)]

for s in missing_speaker.index:
    df_scripts.loc[s]['speaker'] = str(df_scripts.loc[s-1]['line']) + ' ' \
                                   + str(df_scripts.loc[s]['speaker'])
    df_scripts.drop(index=[s-1], inplace=True)
    
    
# assume all "Captain's log..." entries are JANEWAY speaking
captains_log = df_scripts[df_scripts['line'].str.match('Captain\'s log.*', 
                                                       na=False) 
                          & df_scripts['speaker'].isna()]
for c in captains_log.index:
    df_scripts.loc[c]['speaker'] = 'JANEWAY'


# fix speaker names with a stray p
df_scripts['speaker'] = df_scripts['speaker'].str.replace('^p', '', regex=True)    


# fix incorrectly parsed scene descriptons 
habitat = df_scripts[df_scripts['speaker'] == '(Habitat']
for h in habitat.index:
    df_scripts.loc[h]['line'] = str(df_scripts.loc[h]['speaker']) + ': ' \
                                    + str(df_scripts.loc[h]['line'])
    df_scripts.loc[h]['speaker'] = np.nan
    df_scripts.loc[h]['row_type'] = 'description'


# fix speaker names with a stray (
df_scripts['speaker'] = df_scripts['speaker'].str.replace('^\(', '', regex=True)    



#------------------------------------------------------------------------------
# Output to csv
#------------------------------------------------------------------------------

# after all scripts have been parsed, merge with episode list
df_final = df_episodes.merge(df_scripts, how='left', on='link')
      
# output to csv
df_final.to_csv('.\\star-trek-transcripts_parsed.csv', index=False, 
                quoting=QUOTE_ALL)