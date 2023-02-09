from pprint import pprint
import requests
from bs4 import BeautifulSoup
import json

KEYWORDS = ["Django", "Flask"]

def json_write(list):
    with open('hh.json', 'w', encoding="utf-8") as file:
        json.dump(list, file, indent=4)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
response = requests.get("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2", headers=headers)
hh_main = response.text

soup = BeautifulSoup(hh_main, features='lxml')
main_content = soup.find('div', id='a11y-main-content')
contents = main_content.find_all('div', class_='vacancy-serp-item__layout')

vacancy_list=[]
for conten in contents:
    description = conten.find('div', class_='g-user-content').text
    link_desc = conten.find('a', class_='serp-item__title')
    title_v = link_desc.text
    link_v = link_desc['href']
    salary_val = conten.find('span', class_='bloko-header-section-3')
    if salary_val:
        salary = salary_val.text
    else:
        salary = ''
    company = conten.find('div', class_='vacancy-serp-item__meta-info-company').text
    adress = conten.select('div [data-qa="vacancy-serp__vacancy-address"]')
    city =adress[0].text.split()[0].replace(',','')
    for word in KEYWORDS:
        if word.lower() in title_v.lower() or word.lower() in description.lower():
            vacancy_row= {'title_v': title_v,
                           'company': company,
                           'salary': salary,
                           'link_v': link_v}
            vacancy_list.append(vacancy_row)

pprint(vacancy_list)

json_write(vacancy_list)


