import json
from time import sleep
from bs4 import BeautifulSoup as bs
import requests
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 '
                  '(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }


def getsalary( word):
    word = word.replace(" ", "")
    word = word.replace('руб.', "")
    findindex = word.find('от', 0)
    if findindex == 0:
        word = word.replace('от', "")
        minsalary = float(word.strip())
        maxsalary = 0.0
        currency = 0.0
        return minsalary, maxsalary, currency
    findindex = word.find('от', 0)
    if findindex == 0:
        word = word.replace('до', "")
        maxsalary = float(word.strip())
        minsalary = 0.0
        currency = 0.0
        return minsalary, maxsalary, currency
    findindex = word.find('–')
    if findindex > -1:
        words = word.split('–')
        minsalary = float(str(words[0]).strip())
        maxsalary = float(str(words[1]).strip())
        currency = (minsalary + maxsalary) / 2
        return minsalary, maxsalary, currency

    return None, None, None




rsc = 200
i = 0
data =[]
while rsc < 300:
    url =f'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=bigdata&page= {i}'
    response = requests.get(url, headers=headers)
    rsc = response.status_code
    print(f'Страница с номером {i} существует')
    i += 1
    soup = bs(response.text, 'html.parser')
    vacancys = soup.findAll("div", {"class": "vacancy-serp-item"})
    if len(vacancys) == 0:
        rsc = 300

    for vacancy in vacancys:
        vacancyurl = vacancy.findAll("a", {"data-qa": "vacancy-serp__vacancy-title"})[0]["href"]
        position = vacancy.findAll("a", {"data-qa": "vacancy-serp__vacancy-title"})[0].text
        salary = vacancy.findAll("div", {"class": "vacancy-serp-item__sidebar"})[0].text
        companyname = vacancy.findAll("a", {"data-qa": "vacancy-serp__vacancy-employer"})[0].text
        placecompany = vacancy.findAll("span", {"data-qa": "vacancy-serp__vacancy-address"})[0].text
        minsalary, maxsalary, currency = getsalary(salary)
        print (vacancyurl, position, salary, companyname, placecompany)
        print(type(salary))
        print(minsalary, maxsalary, currency)
        data.append([
            ['companyname ', companyname],
            ['position ', position],
            ['minsalary ', minsalary],
            ['maxsalary ', maxsalary],
            ['currency ', currency],
            ['vacancyurl ', vacancyurl],
            ['placecompany ', placecompany]
            ]
            )
    sleep(0.5)
with open( "vacancys.csv", "w", newline="", encoding= 'utf8') as file:
    writer = csv.writer(file,  delimiter=';')
    writer.writerows(data)






