import requests
import re
import json
import lxml
import bs4
from fake_headers import Headers

def get_fake_headers():
    return Headers(browser="chrome",os="mac",headers=True).generate()

response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2',headers=get_fake_headers())

result = []
if response.status_code == 200:
    soup = bs4.BeautifulSoup(response.text,features="lxml") 
    search_url = soup.findAll("div",class_="vacancy-serp-item__layout")
    for i in search_url:
        address = i.find("div",attrs = {"data-qa":"vacancy-serp__vacancy-address","class":"bloko-text"}).text
        if address.split(",")[0] == "Москва" or address.split(",")[0] == "Санкт-Петербург":
            title = i.find("span",attrs = {"class":"serp-item__title-link serp-item__title"}).text
            link = i.find("a",attrs = {"class":"bloko-link"})["href"]
            salary = i.find("span",attrs = {"data-qa":"vacancy-serp__vacancy-compensation", "class":"bloko-header-section-2"})
            if salary is not None: 
                salary = str(salary.text)
            else: 
                salary = "По договорённости"

            response_vacancy = requests.get(link,headers=get_fake_headers())
            soup_vacancy = bs4.BeautifulSoup(response_vacancy.text,features="lxml")
            data = soup_vacancy.find("div",attrs = {"class":"g-user-content","data-qa":"vacancy-description"})
            if data is not None:
                if "Django" in re.findall(r"\w+",data.text)  or "Flask" in re.findall(r"\w+",data.text):
                    
                    result.append({
                        "title": title,
                        "salary": str(salary),
                        "address": str(address),
                        "link": link
                        })

for i in result:
    with open("vacancy_hh.json", "a",encoding="utf-8")as file:
        json.dump(i, file,ensure_ascii=False)
        file.write("\n")