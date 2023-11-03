import requests
from bs4 import BeautifulSoup

URL = "https://www.bbc.com/news/world-us-canada-67268201"
URL = "https://www.bbc.com/news/world-us-canada-67293355"
URL = "https://www.bbc.com/news/world-australia-67293752"

page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
divs = soup.find_all('div', attrs={'data-component': ['text-block', 'subheadline-block']})

extracted_elements = [soup.find('h1', id='main-heading')]
for div in divs:
    extracted_elements += div.find_all(['p', 'h2'])

text = [paragraph.text for paragraph in extracted_elements]

for elem in text:
    print(elem, end='\n\n')
