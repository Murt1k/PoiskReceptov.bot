import requests
from bs4 import BeautifulSoup

 

def get_recept(url):
    R = requests.get(url)
    R.encoding = 'windows-1251'

    soup = BeautifulSoup(R.text, 'html.parser') 
    

    def ingridiens():
        articles = soup.find_all('div', class_='ingredients-bl')
        Ingridiens = articles[0].find_all('span')
        result = []
        for i in Ingridiens:
            title = i.get_text(strip=True) 
            result.append(title)
        return result

    def picture():
        articles = soup.find_all('li', class_='cooking-bl')
        results = []
        for i in articles:
            img = i.find("a").find("img")["src"]
            recept = i.find("p").get_text(strip = True)
            results.append((img,recept))
        return results
    return ingridiens(),picture()

print(get_recept('https://www.povarenok.ru/recipes/show/132620/'))
