# https://www.yellowpages.com/search?search_terms=salon&geo_location_terms=Berlin
import requests
result=[]
results = requests.get("https://adressmonster.de/branchenliste#alph_A")
print( results.status_code)
c = results.content
from bs4 import BeautifulSoup
soup = BeautifulSoup(c,features='html.parser')
samples = soup.findAll("div",{"class":"headline"})

for s in samples:
    # ht=BeautifulSoup(s,'lxml')
    print(s.text)
    result.append(s.text)


print(result)