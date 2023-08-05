import requests,re
from bs4 import BeautifulSoup
u='https://check-host.net/ip-info?host=205.185.114.231'
c=requests.get(u,headers = {'User-Agent': "ala ala"}).text
soup= BeautifulSoup(c,'html.parser')
la=soup.find_all('a')
l=[]
for i in la:
 if "#ip_info-dbip" in str(i):
  l.append(remove_html_tags(str(i)).strip().replace('\n',' '))
 if "#ip_info-ip2location" in str(i):
  l.append(remove_html_tags(str(i)).strip().replace('\n',' '))
 if "#ip_info-geolite2" in str(i):
  l.append(remove_html_tags(str(i)).strip().replace('\n',' '))
p=soup.find_all('table')
o=0
di={}
for x in p:
 try:
  do={}
  y=x.find_all('tr')
  for w in y:
   a=w.find_all('td')
   try:
    c=str(a[0]).split('<td>')[1].split('</td>')[0].strip()
    d=str(a[1]).split('<td>')[1].split('</td>')[0].strip()
    d=remove_html_tags(d).strip().replace('\n',' ')
    do.update({c:d})
   except:
    pass
  di.update({l[o]:do})
  o+=1
 except:
  pass
for x in di:
 print (x)
 print('')
 for y in di[x]:
  print(y+": "+di[x][y])
 print('')