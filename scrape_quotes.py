import requests
from bs4 import BeautifulSoup
import json

url = 'https://quotes.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Функція для отримання даних про авторів
def get_authors_data(soup):
    authors_data = []
    # Знаходимо посилання на сторінки авторів
    author_links = [a['href'] for a in soup.select('.quote > span > a')]
    for link in author_links:
        response = requests.get(url + link)
        soup_author = BeautifulSoup(response.text, 'html.parser')
        # Отримуємо дані про автора
        fullname = soup_author.find('h3').get_text()
        born_date = soup_author.find('span', class_='author-born-date').get_text()
        born_location = soup_author.find('span', class_='author-born-location').get_text()
        description = soup_author.find('div', class_='author-description').get_text().strip()
        # Перевірка на дублікати
        if not any(author['fullname'] == fullname for author in authors_data):
            authors_data.append({
                'fullname': fullname,
                'born_date': born_date,
                'born_location': born_location,
                'description': description
            })
    return authors_data

# Отримання даних про авторів
authors_data = get_authors_data(soup)

# Збереження даних про авторів у файл JSON
with open('authors.json', 'w', encoding='utf-8') as f:
    json.dump(authors_data, f, indent=2, ensure_ascii=False)

# Знаходимо всі цитати
quotes_data = []
for quote in soup.find_all('div', class_='quote'):
    text = quote.find('span', class_='text').text.strip()
    author = quote.find('small', class_='author').text
    tags = [tag.text for tag in quote.find_all('a', class_='tag')]
    quotes_data.append({
        'quote': text,
        'author': author,
        'tags': tags
    })

# Збереження даних про цитати у файл JSON
with open('quotes.json', 'w', encoding='utf-8') as f:
    json.dump(quotes_data, f, indent=2, ensure_ascii=False)

print("Дані збережено у файлах 'authors.json' та 'quotes.json'.")