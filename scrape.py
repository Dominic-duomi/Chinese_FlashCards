# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json

URL = 'https://www.hsk.academy/en/hsk_4'
data = requests.get(URL)

soup = BeautifulSoup(data.text, 'html.parser')
td = [i.text for i in soup.find_all('span', {'class':'theme_label__UH5A4'})]


URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQcTbYaVattB_aOJ7bXHGLcUIH-'\
    'h5B3EJ74uutb52Ah7zXQENSRKDLIzaHZnkrWmQshok13oIsStzAk/pubhtml/sheet?headers%5Cx3'\
    'dfalse&gid=1547926705'
data = requests.get(URL)
data1 = []
soup = BeautifulSoup(data.text, 'html.parser')
waffle = soup.find('table', {'class': 'waffle'})

for i in waffle.find_all('tr', {'style': 'height:20px;'}):
    data1.append(i.find('td').text)

combine = list(set(td + data1[1:]))
combined = {i:float(1) for (i) in combine}


with open('scrape.json','w',encoding='utf-8') as fp:
    json.dump(combined, fp, ensure_ascii=False)

