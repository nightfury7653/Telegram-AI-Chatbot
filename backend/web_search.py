import aiohttp
from bs4 import BeautifulSoup
import re
import gemini_service as gemini

async def search_web(query):
    async with aiohttp.ClientSession() as session:
        search_url = f"https://lite.duckduckgo.com/lite?q={query}"
        async with session.get(search_url) as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            results = []
            
            # DuckDuckGo lite uses tables for results
            for row in soup.find_all('tr', class_='result-link')[:5]:
                try:
                    link = row.find('a')
                    title = link.text
                    url = link['href']
                    # Get snippet from next row
                    snippet = row.find_next('tr', class_='result-snippet').text
                    
                    results.append({
                        'title': title,
                        'link': url,
                        'snippet': snippet
                    })
                except:
                    continue
    
        # Generate AI summary
        summary_prompt = f"Summarize these search results about '{query}':\n" + \
                        "\n".join([f"- {r['title']}: {r['snippet']}" for r in results])
        summary = await gemini.get_chat_response(summary_prompt)
        
        return {
            'summary': summary,
            'results': results
        }