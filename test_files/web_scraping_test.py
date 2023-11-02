import requests
from bs4 import BeautifulSoup

URL = "https://www.bbc.com/news/world-us-canada-67268201"
page = requests.get(URL)

print(page.text)


soup = BeautifulSoup(page.content, "html.parser")
divs = soup.find_all('div', {'data-component': 'text-block'})

extracted_elements = []
for div in divs:
    h2_sibling = div.find_previous_sibling('h2', {'data-component': 'subheadline-block'})
    if h2_sibling:
        extracted_elements += (('h2', h2_sibling.text))

    extracted_elements += div.find_all('p')


text = [paragraph.text for paragraph in extracted_elements]

for elem in text:
    print(elem, end='\n\n')

