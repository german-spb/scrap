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
for job in job_div:
    job_art = job.find('a').text # название должности
    link_tag = job.find('a', class_='serp-item__title')
    job_link = link_tag['href'] # сылка
    job_adress = job.find(class_='vacancy-serp-item__info')
    job_comp = job_adress.find(class_='bloko-text').text # компания
    job_company = job_comp.replace(u'\xa0', u' ')
    job_city = job_adress.find(attrs={'class':'bloko-text', 'data-qa':'vacancy-serp__vacancy-address'}).text # город
    job_many = str(job.find('span', class_ = 'bloko-header-section-3')) # вилка ЗП
    cleanr = re.compile('<.*?>')
    job_salary = re.sub(cleanr, '', job_many)
    salary = job_salary.replace(u'\u202f', u' ')

    jobs.append({
        'должность' : job_art,
        'ссылка' : job_link,
        'компания' : job_company,
        'город' : job_city,
        'вилка ЗП' : salary
        })
pprint(jobs)
# -------------------------------------------------------------------------------
# HOST = 'https://habr.com/ru/all/'

# def get_headers():
#     Headers(browser='firefox', os='win').generate()

# habr_main_html = requests.get(HOST, headers=get_headers()).text
# soup = BeautifulSoup(habr_main_html, features='lxml')

# article_list_tag = soup.find(class_='tm-articles-list')
# 'id="post-content-body"'
# articles_tags = article_list_tag.find_all('article')

# articles = []

# for article in articles_tags:
#     article_time = article.find('time')['title']
#     link_tag = article.find('a', class_='tm-article-snippet__title-link')
#     link_relative = link_tag['href']
#     link = f'https://habr.com{link_relative}'
#     span_tag = link_tag.find('span')
#     title = span_tag.text
#     article_html = requests.get(link, headers=get_headers()).text
#     article_body = BeautifulSoup(article_html, features='lxml').find(id='post-content-body').text

#     articles.append({

#         'time': article_time,
#         'title': title,
#         'body': article_body,
#         'link': link
#     })

# pprint.pprint(articles)
    
