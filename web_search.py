import requests
from bs4 import BeautifulSoup

def search_web(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0'
    }
    search_url = f"https://duckduckgo.com/html/?q={query}"
    response = requests.get(search_url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = []

    for result in soup.find_all('div', class_='result'):
        title_elem = result.find('a', class_='result__a')
        snippet_elem = result.find('a', class_='result__snippet')

        if title_elem and snippet_elem:
            title = title_elem.text
            link = title_elem['href']
            snippet = snippet_elem.text
            search_results.append({"title": title, "link": link, "snippet": snippet})

    return search_results
