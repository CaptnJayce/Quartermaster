import requests
from bs4 import BeautifulSoup
import ollama
import qt

conversation_history = []

def query_llama(query):
    try:
        prompt = qt.p
        
        for message in conversation_history:
            prompt += f"\n{message['role']}: {message['content']}"
        
        prompt += f"\nUser: {query}\nQT:"
        
        result = ollama.chat(model="llama3.2:3b", messages=[{"role": "user", "content": prompt}])
        
        return result['message']['content'] if 'message' in result and 'content' in result['message'] else "No content in response"

    except Exception as e:
        print(f"Error querying Ollama: {e}")
        return None

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

def qt_assistant(query):
    qt_reply = query_llama(query)
    
    if qt_reply:
        conversation_history.append({"role": "user", "content": query})
        conversation_history.append({"role": "assistant", "content": qt_reply})

        if "search" not in query.lower():
            print("\nQT:", qt_reply)
        
        if "search" in query.lower() or "search the web" in qt_reply.lower():
            search_results = search_web(query)
            
            if search_results:
                relevant_info = ""
                for idx, result in enumerate(search_results[:3], 1):
                    relevant_info += f"Title: {result['title']}\nLink: {result['link']}\nSnippet: {result['snippet']}\n\n"
                
                formatted_query = f"Please summarize the following search results into a concise, human-readable summary:\n\n{relevant_info}"
                summary = query_llama(formatted_query)
                
                if summary:
                    print(summary + "\n")
                else:
                    print("No summary returned from Ollama.")
    else:
        print("No response from AI. Exiting.")

if __name__ == "__main__":
    while True:
        query = input("Enter your query: ")
        qt_assistant(query)
