#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python file that gathers the function used in parser.py
"""
from bs4 import BeautifulSoup as bs
import re
import unicodedata

import pandas as pd


def dividi_parole(string):
    for i in range(1, len(string) - 1):
        if string[i - 1].islower() and string[i].isupper() and not string[i-2:i] == "Mc":
            string = string[0:i] + ", " + string[i:len(string)]
        elif string[i - 1] == '.' and string[i].isupper():
            string = string[0:i] + ", " + string[i:len(string)]
    return string

def html_to_dict(file_name):
    film_dict = {}
    with open(file_name, 'rb') as html:
        soup = bs(html, 'html.parser')

    if 'This disambiguation page' in soup.text:
        pass  # this is a disambiguation page, not film page
    else:
        # Title Page
        page_title = soup.title.text
        page_title = re.sub(r' - Wikipedia', '', page_title)
        film_dict.update({"Title": page_title})

        # Paragraphers (Intro and Plot)
        p = soup.find_all("p")

        if len(p) >= 1:
            intro = p[0].text
            intro = re.sub(r'\n', '', intro)
            intro = re.sub(r'\[\d*\]', '', intro)
            film_dict.update({"Intro": intro})
        if len(p) >= 2:
            plot = p[1].text
            plot = re.sub(r'\n', '', plot)
            plot = re.sub(r'\[\d*\]', '', plot)
            film_dict.update({"Plot": plot})

        # URL
        urls = soup.find("link", {"rel": "canonical", 'href': True})
        film_dict.update({"Wikipedia Url": urls.get('href')})

        # Film Infobox
        infobox = soup.find_all("table", {"class": "infobox vevent"})

        if infobox:
            infobox = infobox[0]

            tr = infobox.find_all('tr')

            for i in range(len(tr)):
                tr[i] = re.sub(r'\[\d*\]', '', tr[i].text)
                tr[i] = tr[i].replace("  ", ", ")
                tr[i] = tr[i].replace("\n", ", ")
                tr[i] = unicodedata.normalize("NFKD", tr[i])

                if 'Directed by' in tr[i][:11]:
                    film_dict.update({"Directed by": tr[i][11:].strip(', ')})
                elif 'Produced by' in tr[i][:11]:
                    film_dict.update({"Produced by": dividi_parole(tr[i][11:].strip(', '))})
                elif 'Written by' in tr[i][:10]:
                    film_dict.update({"Written by": dividi_parole(tr[i][10:].strip(', '))})
                elif 'Starring' in tr[i][:8]:
                    film_dict.update({"Starring": dividi_parole(tr[i][8:].strip(', '))})
                elif 'Narrated by' in tr[i][:11]:
                    film_dict.update({"Narrated by": dividi_parole(tr[i][11:].strip(', '))})
                elif 'Music by' in tr[i][:8]:
                    film_dict.update({"Music by": dividi_parole(tr[i][8:].strip(', '))})
                elif 'Screenplay by' in tr[i][:13]:
                    film_dict.update({"Screenplay by": dividi_parole(tr[i][13:].strip(', '))})
                elif 'Story by' in tr[i][:8]:
                    film_dict.update({"Story by": dividi_parole(tr[i][8:].strip(', '))})
                elif 'Cinematography' in tr[i][:14]:
                    film_dict.update({"Cinematography": dividi_parole(tr[i][14:].strip(', '))})
                elif 'Edited by' in tr[i][:9]:
                    film_dict.update({"Edited by": dividi_parole(tr[i][9:].strip(', '))})
                elif 'Productioncompany' in tr[i][:17]:
                    film_dict.update({"Production Company": dividi_parole(tr[i][17:].strip(', '))})
                elif 'Distributed by' in tr[i][:14]:
                    film_dict.update({"Distributed by": dividi_parole(tr[i][14:].strip(', '))})
                elif 'Release date' in tr[i][:12]:
                    film_dict.update({"Release date": dividi_parole(tr[i][12:].strip(', '))})
                elif 'Running time' in tr[i][:12]:
                    film_dict.update({"Running time": dividi_parole(tr[i][12:].strip(', '))})
                elif 'Country' in tr[i][:7]:
                    film_dict.update({"Country": dividi_parole(tr[i][7:].strip(', '))})
                elif 'Language' in tr[i][:8]:
                    film_dict.update({"Language": dividi_parole(tr[i][8:].strip(', '))})
                elif 'Budget' in tr[i][:6]:
                    film_dict.update({"Budget": tr[i][6:].strip(', ')})
                elif 'Box office' in tr[i][:10]:
                    film_dict.update({"Box office": tr[i][10:].strip(', ')})
                else:
                    pass
    return film_dict


#print(html_to_dict('Wikipedia/article_199.html'))

def save_tsv_dataframe(list_info_film):
    dataframe = pd.DataFrame(list_info_film)
    n_file = input("Number of movies file (1, 2, 3): ")
    name_file = 'Wikipedia/movie' + n_file + '.tsv'
    dataframe.to_csv(name_file, sep='\t', index=False)
