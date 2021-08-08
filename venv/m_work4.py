import requests
import time
from lxml import html




def readdata():
    url = 'https://yandex.ru/news/rubric/science'
# для получения мобтлбной версии сайта
    headers = {
        'User-Agent': 'Mozilla/5.0 '
                      '(iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 '
                      '(KHTML, like Gecko)  Version/9.0 Mobile/13B137 Safari/601.1'
    }

    response = requests.get(url, headers=headers)

    # print (response.text)

    dom = html.fromstring(response.text)
    items = dom.xpath('//article[contains(@class, "mg-card")]')


    i = 0
    for item in items:

        i += 1
        print(i)
        name = item.xpath('.//div[@class="mg-card__annotation"]/text()')
        link = item.xpath(
            './/a/@href')
        source = item.xpath('.//span[@class="mg-card-source__source"]/a/text()')


        print(name)
        print(link)
        print(source)







if __name__ == '__main__':
    readdata()
