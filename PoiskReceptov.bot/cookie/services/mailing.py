import requests

from urllib.parse import quote


def _get_html():
    url = "https://www.povarenok.ru/recipes-of-the-day/"
    
    r = requests.get(url)

    r.encoding = 'windows-1251'  # указать правильную кодировку

    return r.text

def _html_process(html):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, 'html.parser')

    articles = soup.find_all('article', class_='item-bl')

    results = []
    for article in articles:
        # Название
        title_tag = article.find('h2')
        title = title_tag.get_text(strip=True) if title_tag else 'Нет названия'

        # Ссылка на рецепт
        url_tag = article.find("a")
        url_src = url_tag["href"] if url_tag else "Нет ссылки"

        # Ссылка на картинку
        img_tag = article.find('div', class_='m-img').find('img') if article.find('div', class_='m-img') else None
        img_src = img_tag['src'] if img_tag else 'Нет картинки'

        # Описание (первый <p>)
        desc_tag = article.find('p')
        description = desc_tag.get_text(strip=True) if desc_tag else 'Нет описания'

        # Основные продукты в списке
        ingr_spans = article.find('div', class_='ingr_fast')
        if ingr_spans:
            ingredients = [span.get_text(strip=True) for span in ingr_spans.find_all('span')]
        else:
            ingredients = []

        results.append((url_src, title, img_src, description, ingredients))
    return results

def search_worker():

    html = _get_html()

    return _html_process(html)