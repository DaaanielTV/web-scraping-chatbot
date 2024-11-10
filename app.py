from flask import Flask, render_template, request, jsonify
import httpx
from bs4 import BeautifulSoup
import asyncio

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
async def scrape():
    data = request.json
    url = data.get('url')
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            title = soup.find('title').text if soup.find('title') else "Kein Titel gefunden"
            description = soup.find('meta', {'name': 'description'})
            description = description['content'] if description else "Keine Beschreibung gefunden"
            headlines = [h.text for h in soup.find_all(['h1', 'h2', 'h3'])][:5]
            
            return jsonify({
                "title": title,
                "description": description,
                "headlines": headlines
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 