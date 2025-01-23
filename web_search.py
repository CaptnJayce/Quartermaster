import requests
from bs4 import BeautifulSoup

def search_web(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0 '
    }
    search_url = f"https://www.google.com/search?q={query}"
    response = requests.get(search_url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = []

    for g in soup.find_all(class_='tF2Cxc'):
        title = g.find('h3').text
        link = g.find('a')['href']
        snippet = g.find('div', class_='VwiC3b').text if g.find('div', class_='VwiC3b') else 'No snippet available'
        search_results.append({"title": title, "link": link, "snippet": snippet})

    return search_results
