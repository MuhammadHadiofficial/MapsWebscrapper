from django.db import IntegrityError
from myapp.models import Business
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
from multiprocessing import Pool

from urllib3.exceptions import MaxRetryError

sys.setrecursionlimit(250000000)


def getDetails(url):
    city = url['city']
    keyword = url['keyword']
    print(url)
    try:

        country = 'Germany'
        phone_number = '-'
        weblink = '-'
        email = '-'
        hours = '-'
        address = '-'
        street = '-'
        street_number = '-'
        postal = '-'
        area = '-'
        name = '-'
        rating = '-'
        type = '-'
        street_rec = '-'
        results = requests.get(url['url'], timeout=20)
        details = results.content
        detailpage = BeautifulSoup(details, features='html.parser')
        rating = detailpage.find('div', {'class', 'mod-Bewertungen__gesamt-note'})
        if (rating):
            rating = rating.get_text().strip()
        else:
            rating = '-'
        type = detailpage.find('div', {'class', 'mod mod-BranchenUndStichworte'})
        if (type):
            type = " ".join(type.get_text().strip().split(','))
        else:
            type = '-'

        name = detailpage.find('h1', {'class', 'mod-TeilnehmerKopf__name'})
        if (name):
            name = " ".join(name.get_text().strip().split(','))

            # print(name)
        else:
            name = '-'
        street = detailpage.findAll('address', {'class': 'mod-TeilnehmerKopf__adresse'})

        if (street):
            try:
                if (street[0].find('span', {"property": "postalCode"})):
                    postal = street[0].find('span', {"property": "postalCode"}).get_text().strip()
                else:
                    postal = '-'
                # print(street[0].find('span', {"property": "streetAddress"}))
                # print(street[0].find('span', {"property": "postalCode"}))
                # print(street[0].find('span', {"property": "postalCode"}))
            except IndexError:
                postal = '-'
            except AttributeError:
                postal = '-'

            streetdata = street[0].findAll('span', {'class', 'mod-TeilnehmerKopf__adresse-daten'})
            streetpartial = None
            if (streetdata):
                street = streetdata[0].get_text().split()
                #
                # if( street[len(street) - 1:][0].strip().isalpha() and ( street[len(street) - 1:][0].strip().find('-')!=-1 or street[len(street) - 1:][0].strip().find('.')!=-1)):
                #     # print(street[len(street) - 1:][0].strip()+"true")

                street_number = street[len(street) - 1:][0].strip()
                if (street[len(street) - 1:][0].strip().isalpha()):
                    # print(street[len(street) - 1:][0].strip()+"true")
                    streetpartial = street[len(street) - 1:][0].strip()
                    street_number = '-'

                street_rec = "".join(street[0:len(street) - 1]).strip()
                if (streetpartial):
                    street_rec = street_rec + " " + streetpartial
                # print(street_rec)
        address = detailpage.findAll('span', {'class', 'mod-TeilnehmerKopf__adresse-daten--noborder'})

        try:
            area = address[0].get_text().strip()
        except IndexError:
            area = '-'
        phone_number = detailpage.find("span", {"data-role": 'telefonnummer'})
        if (phone_number):
            phone_number = phone_number.get_text().strip()
        else:
            phone_number = '-'
        email = detailpage.find("a", {"property": 'email'})
        if (email):
            email = email.get_text().strip()
        else:
            email = '-'
        weblink = detailpage.find("a", {"property": 'url'})
        if (weblink):
            weblink = weblink.get_text().strip()
        else:
            weblink = '-'
        return (
        name, rating, type, street_rec, street_number, postal, area, city, country, phone_number, weblink, email)

        print("record ends")
    except requests.exceptions.ReadTimeout:
        print('timeout')
        return None
    except requests.exceptions.ConnectionError:
        return None
    return None


def getData(businessname, city, country, id, radius):
    keyword = businessname.lower()
    city = city.lower()
    country = country
    d = []
    total = 0
    check_next = True

    if (int(radius) == 0):
        url = "https://www.gelbeseiten.de/Suche/" + keyword + "/" + city
    else:
        url = "https://www.gelbeseiten.de/Suche/" + keyword + "/" + city.strip() + "?umkreis=" + str(int(radius) * 1000)

    while check_next:

        try:
            results = requests.get(url)
            print(url)
        except requests.exceptions.ConnectionError:
            # sleep(2)
            print('jell')
            continue
        except MaxRetryError:
            # sleep(2)
            print('jell')
            continue
        c = results.content
        # from bs4 import BeautifulSoup
        soup = BeautifulSoup(c, features='html.parser')
        samples = soup.findAll("article", {"class": "mod mod-Treffer"})
        url = []
        for s in samples:
            try:
                detail = s.findAll("a", {"class": 'gs-btn'})[0].attrs
                url.append({'city': city, 'keyword': keyword, 'url': detail['href']})
            except IndexError:
                continue
        p = Pool(20)
        a = p.map(getDetails, url)
        p.terminate()
        p.join()
        print("next Iteration")
        for row in a:
            # print(row)
            if (row):
                total = total + 1

                try:
                    # (name, rating, type, street_rec, street_number, postal, area, city, country, phone_number, weblink,
                    #  email)

                    business = Business(keyword=keyword, name=row[0], rating=row[1], industry=row[2], street=row[3],
                                        street_number=row[4], postalcode=row[5], area=row[6], city=row[7],
                                        country=row[8], opening_hours='-', phone_number=row[9],
                                        website=row[10], email=row[11], )
                    business.save()
                    print(row)

                except IntegrityError as e:
                    print('duplicate')
                    # print(rating, type, street, street_number, postal, area, city, country, hours, phone_number,
                    #       weblink, email)
                    print(row)
                    return None
                d.append(row)

        next = soup.find("a", {"class", "gs_paginierung__sprungmarke gs_paginierung__sprungmarke--vor btn btn-default"})
        if (next):
            url = next['href']

            print(url)
        else:
            check_next = False
    dataFrame = pd.DataFrame(d, columns=(
        'Firmenname / COMPANY NAME', 'rating', 'Branche / INDUSTRY', 'Strasse / Street', 'Strasse no', "PostalCode",
        "Area", 'Stadt / City', 'Land / COUNTRY', 'phone_number', 'website', 'email'))
    dd = dataFrame.sort_values(by=['Firmenname / COMPANY NAME'])
    filename = './' + str(id) + '.csv';
    dd = dd.reset_index(drop=True)
    dd.to_csv(filename)

    rating_count = dataFrame[dataFrame['rating'] != '-'].count()[0]
    phone_count = dataFrame[dataFrame['phone_number'] != '-'].count()[0]
    email_count = dataFrame[dataFrame['email'] != '-'].count()[0]
    website_count = dataFrame[dataFrame['website'] != '-'].count()[0]
    name_count = dataFrame[dataFrame['Firmenname / COMPANY NAME'] != '-'].count()[0]

    postalCode_count = dataFrame[dataFrame['PostalCode'] != '-'].count()[0]
    print(total)
    print(filename)
    if (total > 0):
        dd.to_csv(filename)

    return {'filename': filename, 'total': total, 'rating_count': str(rating_count),
            'phone_count': str(phone_count), 'email_count': str(email_count), 'website_count': str(website_count),
            'name_count': str(name_count), 'postalCode_count': str(postalCode_count)}
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
