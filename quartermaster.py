import requests
from bs4 import BeautifulSoup
import json
import ollama

def query_llama(query):
    try:
        result = ollama.chat(model="llama3.2:1b", messages=[{"role": "user", "content": query}])
        return result['message']['content'] if 'message' in result and 'content' in result['message'] else "No content in response"
    except Exception as e:
        print(f"Error querying Ollama: {e}")
        return None

def search_web(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
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

def qt_assistant(query):
    #print("Sent to QT", query)
    
    qt_reply = query_llama(query)
    
    if qt_reply:
        if "search" not in query.lower():
            print("\nQT:", qt_reply)
        
        if "search" in query.lower() or "search the web" in qt_reply.lower():
            #print("AI suggests or user wants to search the web. Proceeding with web scraping.")
            search_results = search_web(query)
            
            if search_results:
                print("Found the following search results:")
                relevant_info = ""
                for idx, result in enumerate(search_results[:3], 1):
                    relevant_info += f"Title: {result['title']}\nLink: {result['link']}\nSnippet: {result['snippet']}\n\n"
                
                formatted_query = f"Please summarize the following search results into a concise, human-readable summary:\n\n{relevant_info}"
                summary = query_llama(formatted_query)
                
                if summary:
                    print("\nSummary:", summary)
                else:
                    print("No summary returned from Ollama.")
    else:
        print("No response from AI. Exiting.")

if __name__ == "__main__":
    query = input("Enter your query: ")
    qt_assistant(query)
