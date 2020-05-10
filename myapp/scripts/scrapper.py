from django.db import IntegrityError
from myapp.models import Business
from datetime import datetime
from telnetlib import EC
import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

def getData(businessname,city,country,id):

    begin_time = datetime.now()

    keyword=businessname.lower()
    city=city.lower()
    country= country
    d = []
    end_result_count=0
    total=0
    # https://www.yellowpages.com/search?search_terms=salon&geo_location_terms=Berlin

    check_next = True
    url = "https://www.gelbeseiten.de/Suche/"+keyword+"/"+city+"?umkreis=50000"
    while check_next:
        results = requests.get(url)
        print(results.status_code)
        c = results.content
        # from bs4 import BeautifulSoup
        soup = BeautifulSoup(c, features='html.parser')
        samples = soup.findAll("article", {"class": "mod mod-Treffer"})

        for s in samples:
            data = s.findAll('h2')
            name=data[0].get_text().strip()
            type = s.findAll('p', {"class": "d-inline-block mod-Treffer--besteBranche"})
            type=type[0].get_text().strip()
            rating = s.findAll('span', {"class": "mod-Stars__text"})
            if (rating):
                rating=rating[0].get_text().strip()
            desc = s.findAll('div', {"class": "mod-Treffer__freitext"})
            if (desc):
                print(desc[0].get_text().strip())
            address = s.findAll('address', {"class": "mod mod-AdresseKompakt"})

            if (address):
                address = address[0].findAll('p')[0].get_text().split(sep=',')

            phone_number = s.findAll('p', {"class": "mod-AdresseKompakt__phoneNumber"})
            if (phone_number):
                phone_number=phone_number[0].get_text()
            status = s.findAll('div', {"class": "oeffnungszeit_kompakt__zustandsinfo--geschlossen"})
            if (status):
                print(status[0].findAll('span')[0].get_text())
                print(status[0].findAll('span', {"class": 'nobr'})[0].get_text())
            weblink = s.findAll("a", {"class": 'contains-icon-homepage'})
            if (weblink):
                weblink = weblink[0]['href']

            email = s.findAll("a", {"class": 'contains-icon-email gs-btn'})
            print(email)
            if (email):
                email=email[0]['href']
            hours=''
            status = s.findAll('div', {"class": "oeffnungszeit_kompakt__zustandsinfo--geschlossen"})
            if (status):
                # print(status[0].findAll('span')[0].get_text())
                hours=status[0].findAll('span', {"class": 'nobr'})[0].get_text()
            else:
                status = s.findAll('div', {"class": "oeffnungszeit_kompakt__zustandsinfo--geoeffnet"})
                if(status):
                    # print(status[0].findAll('span')[0].get_text())
                    hours=status[0].findAll('span', {"class": 'nobr'})[0].get_text()
            print(hours)
            try:
                business=Business(keyword=keyword,name=name,rating=rating,industry=type,street=" ".join(address[0].split()),postalcode=address[1].split()[0],city=city,country=country,opening_hours=hours,phone_number=phone_number,website=weblink,email=email,)
                business.save()
                print(hours)
                d.append((name, rating, type," ".join(address[0].split()),address[1].split()[0],city,country,hours, phone_number, weblink,email))
                total=total+1
            except IntegrityError as e:
                print('duplicate')
                continue

        next = soup.find("a", {"class", "gs_paginierung__sprungmarke gs_paginierung__sprungmarke--vor btn btn-default"})
        if (next):
            url = next['href']
        else:
            check_next = False
            # result.append(s.text)
            #
            # print(samples)
            # print(c)
    dataFrame = pd.DataFrame(d, columns=(
        'Firmenname / COMPANY NAME', 'rating', 'Branche / INDUSTRY','Strasse / Street',"PostalCode" ,'Stadt / City','Land / COUNTRY','HOURS', 'phone_number', 'website','email'))
    dd=dataFrame.sort_values(by=['Firmenname / COMPANY NAME'])
    filename='./'+id+'.csv';
    # dataFrame.to_csv('./myfile.csv')
    dd.to_csv(filename)

    # print(dataFrame.head())
    print(dd.head())
    # print(total)
    # print(datetime.now() - begin_time)

    print(filename)
    return {'filename':filename,'total':total}

# from django.db import IntegrityError
# from myapp.models import Business
# from datetime import datetime
# from telnetlib import EC
#
# import pandas as pd
# from selenium import webdriver
# from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, WebDriverException
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from time import sleep
# # import argparse
# # parser = argparse.ArgumentParser(description='Videos to images')
# # parser.add_argument('type', type=str, help='Input dir for videos')
# # parser.add_argument('location', type=str, help='Output dir for image')
# # parser.add_argument('country', type=str, help='Output dir for image')
# # args = parser.parse_args()
# # print(args.type)
# # print(args.location)
# import os
# def getData(businessname,city,country,id):
#     chrome_options = Options()
#
#     chrome_options.add_argument("--no-sandbox");
#     chrome_options.add_argument("--disable-dev-shm-usage");
#     # chrome_options.add_argument('--headless')
#
#     # driver = webdriver.Chrome(options=chrome_options,)
#     driver = webdriver.Chrome(options=chrome_options,executable_path='./myapp/scripts/chromedriver')
#     begin_time = datetime.now()
#
#     driver.get("https://www.google.com/maps/")
#
#     elem = driver.find_element_by_id("searchboxinput")
#     keyword=businessname
#     city=city
#     country= country
#     elem.clear()
#     elem.send_keys(keyword+' near '+city+', '+country)
#     elem.send_keys(Keys.RETURN)
#     d = []
#     end_result_count=0
#     total=0
#     while True:
#         sleep(5)
#         elem='';
#         data_div = driver.find_elements_by_class_name('section-result');
#         for data in data_div:
#             total=total+1
#             # data.find_elements_by_class_name()
#             elem = data.find_elements_by_class_name('section-result-title')[0].text
#             head_div = data.find_elements_by_class_name('section-result-title')[0].text
#
#             print(head_div)
#             rating = 0
#             if len(data.find_elements_by_class_name('cards-rating-score')) > 0:
#                 elem= data.find_elements_by_class_name('cards-rating-score')[0].text
#                 rating = data.find_elements_by_class_name('cards-rating-score')[0].text
#                 rating = rating
#             reviews = 0
#             if len(data.find_elements_by_class_name('section-result-num-ratings')) > 0:
#                 elem=data.find_elements_by_class_name('section-result-num-ratings')[0].text
#
#                 reviews = data.find_elements_by_class_name('section-result-num-ratings')[0].text
#
#             details = data.find_elements_by_class_name('section-result-details')[0].text
#             location = data.find_elements_by_class_name('section-result-location')[0].text
#             opening_hours = data.find_elements_by_class_name('section-result-opening-hours')[0].text
#             phone_number = data.find_elements_by_class_name('section-result-phone-number')[0].text
#             weblink=''
#             if(data.find_elements_by_class_name('section-result-action-wide')):
#                 weblink = data.find_elements_by_class_name('section-result-action-wide')[0].get_attribute('href')
#             # print(head_div, rating, reviews, details, location, opening_hours, phone_number, weblink)
#             try:
#                 business=Business(keyword=businessname,name=head_div,rating=rating,reviews=reviews,industry=details,street=location,city=city,country=country,opening_hours=opening_hours,phone_number=phone_number,website=weblink)
#                 business.save()
#                 d.append((head_div, rating, reviews, details, location,city,country, opening_hours, phone_number, weblink))
#
#             except IntegrityError as e:
#                 print('duplicate')
#                 continue
#         sleep(5)
#         try:
#             ad = data_div.find_element_by_id('section-no-result-title')
#             break;
#         except:
#             pass;
#         cond=False;
#         try:
#             cond = driver.find_element_by_id('n7lv7yjyC35__section-pagination-button-next').is_enabled()
#             print(driver.find_element_by_id('n7lv7yjyC35__section-pagination-button-next').is_enabled())
#             print(elem)
#         except ElementClickInterceptedException:
#             print("click intercepted")
#             continue;
#         except NoSuchElementException:
#             print("Element not found",elem  )
#             end_result_count=end_result_count+1
#             print("Element not found",end_result_count)
#             if end_result_count > 3:
#                 print(end_result_count)
#                 break
#
#         except WebDriverException:
#             print('chrome not found')
#             break;
#         if cond is False:
#             end_result_count=end_result_count+1
#             print("Element not found",end_result_count)
#             if end_result_count > 3:
#                 print(end_result_count)
#                 break
#         else:
#             end_result_count=0
#             print('clicked')
#             btn=driver.find_element_by_id('n7lv7yjyC35__section-pagination-button-next')
#
#             driver.execute_script("arguments[0].click();", btn)
#     dataFrame = pd.DataFrame(d, columns=(
#         'Firmenname / COMPANY NAME', 'rating', 'reviews', 'Branche / INDUSTRY','Strasse / Street' ,'Stadt / City','Land / COUNTRY', 'opening_hours', 'phone_number', 'website'))
#     dd=dataFrame.sort_values(by=['Firmenname / COMPANY NAME'])
#     filename='./'+id+'.csv';
#     # dataFrame.to_csv('./myfile.csv')
#     dd.to_csv(filename)
#
#     # print(dataFrame.head())
#     print(dd.head())
#     print(total)
#     print(datetime.now() - begin_time)
#
#     print(filename)
#     return {'filename':filename,'total':total}
#
