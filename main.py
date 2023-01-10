import requests
from bs4 import BeautifulSoup
from fake_headers import Headers


HOST = 'https://spb.hh.ru/search/vacancy?text=Python+%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%87%D0%B8%D0%BA&from=suggest_post&salary=&area=2&ored_clusters=true&enable_snippets=true'
def get_headers():
    return Headers(browser='firefox', os='win').generate()

html = requests.get(HOST, headers=get_headers()).text

soup = BeautifulSoup(html, features='lxml')
job_div = soup.find(class_='vacancy-serp-content')
job_art = job_div.find_all('a')
link_tag = job_div.find('a', class_='serp-item__title')
job_link = link_tag['href']


print(job_link)