import json
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from pprint import pprint
import re

HOST = 'https://spb.hh.ru/search/vacancy?text=Python&from=suggest_post&area=2'
def get_headers():
    return Headers(browser='firefox', os='win').generate()

html = requests.get(HOST, headers=get_headers()).text

soup = BeautifulSoup(html, features='lxml')
job_div = soup.find_all(class_='vacancy-serp-item__layout')

jobs = []

job_worlds = ['Django', 'Flask']
for job in job_div:
    job_text = str(job.find(class_='g-user-content'))
    cleanr = re.compile('<.*?>')
    text = re.sub(cleanr, '', job_text)
    for item in job_worlds:
        if item in text:
            job_art = job.find('a').text # название должности
            link_tag = job.find('a', class_='serp-item__title')
            job_link = link_tag['href'] # сылка
            job_adress = job.find(class_='vacancy-serp-item__info')
            job_comp = job_adress.find(class_='bloko-text').text # компания
            job_company = job_comp.replace(u'\xa0', u' ')
            job_city = str(job_adress.find(attrs={'class':'bloko-text', 'data-qa':'vacancy-serp__vacancy-address'}).text) # город
            city = re.split("[,?]", job_city)
            job_many = str(job.find('span', class_ = 'bloko-header-section-3')) # вилка ЗП
            cleanr = re.compile('<.*?>')
            job_salary = re.sub(cleanr, '', job_many)
            salary = job_salary.replace(u'\u202f', u' ')

            jobs.append({
            'должность' : job_art,
            'ссылка' : job_link,
            'компания' : job_company,
            'город' : city[0],
            'вилка ЗП' : salary
                    })
with open('jobs.json', 'w', encoding='utf-8') as f:
    json.dump(jobs,f, ensure_ascii=False, indent=4)
# pprint(jobs)
