import requests,re
from bs4 import BeautifulSoup
def get_cou():
  l=[]
  u='https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes'
  c=requests.get(u, headers = {'User-Agent': 'ala'}).text
  soup = BeautifulSoup(c,"html.parser")
  p=soup.find_all('table',class_="wikitable sortable")
  for x in p:
   for y in x.find_all('tr'):
    try:
     l.append( str(y.find_all('td')[-1]).split('<a href="/wiki/.')[1].split('"')[0])
    except:
     pass
   break
  print(len(l))
  print(str(l))
get_cou()