from bs4 import BeautifulSoup
import requests
import json

url = "http://www.ip33.com/area_code.html"
response = requests.get(url, timeout=5)
content = BeautifulSoup(response.content, "html.parser")
data = list()

for province in content.findAll('div', attrs={"class": "ip"}):
    for county in province.find('ul').findAll('li', recursive=False):
        for region in county.findAll('li'):
            dataObject = {
                "Province Name": "".join(filter(lambda x: not (str.isdigit(x)), province.find('h4').text)),
                "Province Code": "".join(filter(str.isdigit, province.find('h4').text)),
                "County Name": "".join(filter(lambda x: not (str.isdigit(x)), county.find('h5').text)),
                "County Code": "".join(filter(str.isdigit, county.find('h5').text)),
                "Region Name": "".join(filter(lambda x: not (str.isdigit(x)), region.text)),
                "Region ID": "".join(filter(str.isdigit, region.text))
            }

            data.append(dataObject)
            print(dataObject)

with open("data.json", 'w', encoding='utf-8') as outfile:
    json.dump(data, outfile, ensure_ascii=False)
