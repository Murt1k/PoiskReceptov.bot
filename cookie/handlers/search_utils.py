import requests
"""
https://www.povarenok.ru/recipes/search/?ing=%CC%EE%F0%EA%EE%E2%FC%2C+%D1%FB%F0+%F2%E2%E5%F0%E4%FB%E9&ing_exc=%D7%E5%F1%ED%EE%EA&kitchen=&type=12&cat=&subcat=&orderby=#searchformtop
https://www.povarenok.ru/recipes/search/?ing=%CC%EE%F0%EA%EE%E2%FC+%D1%FB%F0%20%F2%E2%E5%F0%E4%FB%E9&ing_exc=%D7%E5%F1%ED%EE%EA%09&kitchen=&type=12&cat=&subcat=&orderby=#searchformtop"""

from urllib.parse import quote

def get_true_name(words):
    url = 'https://www.povarenok.ru/ajax/recipes/autocomplete/ingredients/'
  
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://www.povarenok.ru',
        'Referer': 'https://www.povarenok.ru/recipes/search/?ing=1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36',
        'X-CSRF-TOKEN': '1e316466d2e872356b03ceb0bf97e093f55cb2503406fd5ceeb81e717934334b',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"'
    }

    cookies = {
        'PHPSESSID': '7bb02094b1f45eceab4edf931ab83065',
        'drs': '2'
    }

    result = []
    for name in words:
        data = {'q': name}
        response = requests.post(url, headers=headers, cookies=cookies, data=data)
        try:
            result.append(response.json()[0][:-2]+",")
        except:
            result.append(404)
            print("Error 404: serach_utils.get_true_name (Not results)")
            return result
    else:
        result[-1] = response.json()[0][:-2]

    return result

def _get_html(url: str):
    r = requests.get(url)

    r.encoding = 'windows-1251'  # указать правильную кодировку

    return r.text

def _encoding_to_cp1251(words: list[str]):
    result = ""

    for i in words:
        encoded = quote(i.encode("cp1251")) + "+"
        result += encoded

    return result[:-1]


def _get_url_keys_products(words, type_dish, exclude, page):
    words = _encoding_to_cp1251(words)
    exclude = _encoding_to_cp1251(exclude)

    url = (
        f"https://www.povarenok.ru/recipes/search/~"
        f"{page}"
        f"/?ing="
        f"{words}"
        f"&ing_exc="
        f"{exclude}"
        f'&kitchen=&type={type_dish}&cat=&subcat=&orderby=#searchformtop'
    )

    print(url)

    return _get_html(url)

def _get_url_search(words):
    words = _encoding_to_cp1251(words)

    url = (
        f"https://www.povarenok.ru/recipes/search/?name="
        f"{words}"
        f"&orderby=#searchformtop"
    )

    return _get_html(url)

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

def search_worker(words=[], type_dish="", exclude=[""], function="keys_products", page=1):
    """
    search_worker(words=["то что ты ищешь прям вот так пиши сюда"], function="search")
    """

    if function == "keys_products":
        words = get_true_name(words)
        if words[0] == 404:
            return words[0]
        
        if len(exclude) > 0:
            print(f"После get_true_name: {exclude}")
            exclude = get_true_name(exclude)
            print(f"После get_true_name: {exclude}")
            if exclude[0] == 404:
                return exclude[0]
        else:
            exclude = [""]

        html = _get_url_keys_products(words, type_dish, exclude, page)
    elif function == "search":
        html = _get_url_search(words)

    return _html_process(html)


