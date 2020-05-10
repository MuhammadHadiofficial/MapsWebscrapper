# https://www.yellowpages.com/search?search_terms=salon&geo_location_terms=Berlin
import requests
from bs4 import BeautifulSoup
result=[]
# industry=input("indiustry")
# city=input("city")
check_next=True
url="https://www.gelbeseiten.de/Suche/Textilwaren/Berlin?umkreis=50000"
while check_next:
    results = requests.get(url)
    print( results.status_code)
    c = results.content
    # from bs4 import BeautifulSoup
    soup = BeautifulSoup(c,features='html.parser')
    samples = soup.findAll("article",{"class":"mod mod-Treffer"})

    for s in samples:
        data=s.findAll('h2')
        # print(data[0].get_text().strip())
        type=s.findAll('p',{"class":"d-inline-block mod-Treffer--besteBranche"})
        # print(type[0].get_text().strip())
        rating = s.findAll('span', {"class": "mod-Stars__text"})
        # if (rating):
            # print(rating[0].get_text().strip())
        desc = s.findAll('div', {"class": "mod-Treffer__freitext"})
        # if (desc):
            # print(desc[0].get_text().strip())
        address = s.findAll('address', {"class": "mod mod-AdresseKompakt"})
        if (address):
            address=address[0].findAll('p')[0].get_text().split(sep=',')
            # print(" ".join(address[0].split()))
            print(address[1].split()[0])
        phone = s.findAll('p', {"class": "mod-AdresseKompakt__phoneNumber"})
        # if (phone):
            # print(phone[0].get_text())
        status= s.findAll('div', {"class": "oeffnungszeit_kompakt__zustandsinfo--geschlossen"})
        # if (status):
            # print(status[0].findAll('span')[0].get_text())
            # print(status[0].findAll('span',{"class":'nobr'})[0].get_text())
        # status= s.findAll('div', {"class": "oeffnungszeit_kompakt__zustandsinfo--geoeffnet"})
        # if (status):
            # print(status[0].findAll('span')[0].get_text())
            # print(status[0].findAll('span',{"class":'nobr'})[0].get_text())
        weblink=s.findAll("a",{"class":'contains-icon-homepage'})
        if(weblink):
            weblink=weblink[0]['href']
            # print(weblink)
        email=s.findAll("a",{"class":'contains-icon-email gs-btn'})
        # print(email)
        # if(email):
            # print(email[0]['href'])
    next=soup.find("a",{"class","gs_paginierung__sprungmarke gs_paginierung__sprungmarke--vor btn btn-default"})
    if(next):
        url=next['href']
    else:
        check_next=False
    # result.append(s.text)
    #
    # print(samples)
    # print(c)