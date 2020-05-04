from datetime import datetime
from telnetlib import EC

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
# import argparse
# parser = argparse.ArgumentParser(description='Videos to images')
# parser.add_argument('type', type=str, help='Input dir for videos')
# parser.add_argument('location', type=str, help='Output dir for image')
# parser.add_argument('country', type=str, help='Output dir for image')
# args = parser.parse_args()
# print(args.type)
# print(args.location)
import os
def getData(businessname,city,country,id):
    chrome_options = Options()

    chrome_options.add_argument("--no-sandbox");
    chrome_options.add_argument("--disable-dev-shm-usage");
    # chrome_options.add_argument('--headless')

    # driver = webdriver.Chrome(options=chrome_options,)
    driver = webdriver.Chrome(options=chrome_options,executable_path='./myapp/scripts/chromedriver')
    begin_time = datetime.now()

    driver.get("https://www.google.com/maps/")

    elem = driver.find_element_by_id("searchboxinput")
    keyword=businessname
    city=city
    country= country
    elem.clear()
    elem.send_keys(keyword+' near '+city+', '+country)
    elem.send_keys(Keys.RETURN)
    d = []
    end_result_count=0
    total=0
    while True:
        sleep(5)
        elem='';
        data_div = driver.find_elements_by_class_name('section-result');
        for data in data_div:
            total=total+1

            # data.find_elements_by_class_name()
            elem = data.find_elements_by_class_name('section-result-title')[0].text
            head_div = data.find_elements_by_class_name('section-result-title')[0].text

            print(head_div)
            rating = 0
            if len(data.find_elements_by_class_name('cards-rating-score')) > 0:
                elem= data.find_elements_by_class_name('cards-rating-score')[0].text
                rating = data.find_elements_by_class_name('cards-rating-score')[0].text
                rating = rating
            reviews = 0
            if len(data.find_elements_by_class_name('section-result-num-ratings')) > 0:
                elem=data.find_elements_by_class_name('section-result-num-ratings')[0].text

                reviews = data.find_elements_by_class_name('section-result-num-ratings')[0].text

            details = data.find_elements_by_class_name('section-result-details')[0].text
            location = data.find_elements_by_class_name('section-result-location')[0].text
            opening_hours = data.find_elements_by_class_name('section-result-opening-hours')[0].text
            phone_number = data.find_elements_by_class_name('section-result-phone-number')[0].text
            weblink=''
            if(data.find_elements_by_class_name('section-result-action-wide')):
                weblink = data.find_elements_by_class_name('section-result-action-wide')[0].get_attribute('href')
            # print(head_div, rating, reviews, details, location, opening_hours, phone_number, weblink)
            d.append((head_div, rating, reviews, details, location,city,country, opening_hours, phone_number, weblink))


        sleep(5)
        try:

            ad = data_div.find_element_by_id('section-no-result-title')
            break;
        except:
            pass;
        try:
            cond = driver.find_element_by_id('n7lv7yjyC35__section-pagination-button-next').is_enabled()
            print(driver.find_element_by_id('n7lv7yjyC35__section-pagination-button-next').is_enabled())
            print(elem)
        except ElementClickInterceptedException:
            print("click intercepted")
            continue;
        except NoSuchElementException:
            print("Element not found",elem  )
            continue
        except WebDriverException:
            print('chrome not found')
            break;
        if cond is False:
            end_result_count=end_result_count+1
            print("Element not found")
            if end_result_count < 1:
                continue
            else:
                break
        else:
            print('clicked')
            btn=driver.find_element_by_id('n7lv7yjyC35__section-pagination-button-next')
            btn.click();
            driver.execute_script("arguments[0].click();", btn)
    dataFrame = pd.DataFrame(d, columns=(
        'Firmenname / COMPANY NAME', 'rating', 'reviews', 'Branche / INDUSTRY','Strasse / Street' ,'Stadt / City','Land / COUNTRY', 'opening_hours', 'phone_number', 'website'))
    dd=dataFrame.sort_values(by=['Firmenname / COMPANY NAME'])
    filename='./'+id+'.csv';
    # dataFrame.to_csv('./myfile.csv')
    dd.to_csv(filename)

    # print(dataFrame.head())
    print(dd.head())
    print(total)
    print(datetime.now() - begin_time)

    print(filename)
    return {'filename':filename,'total':total}

