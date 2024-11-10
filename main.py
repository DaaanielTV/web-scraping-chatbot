import tkinter as tk
from tkinter import messagebox
import httpx
from bs4 import BeautifulSoup
import threading
import asyncio
from datetime import datetime
from tkinter import ttk
import json

async def get_web_data(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extrahiere wichtige Informationen
        title = soup.find('title').text if soup.find('title') else "Kein Titel gefunden"
        description = soup.find('meta', {'name': 'description'})
        description = description['content'] if description else "Keine Beschreibung gefunden"
        
        # Finde alle Überschriften
        headlines = [h.text for h in soup.find_all(['h1', 'h2', 'h3'])]
        
        return {
            "title": title,
            "description": description,
            "headlines": headlines[:5]  # Erste 5 Überschriften
        }

def chatbot_response():
    user_input = entry.get()
    if user_input.startswith("http"):
        threading.Thread(target=asyncio.run, args=(process_request(user_input),)).start()
    else:
        messagebox.showinfo("Chatbot Antwort", "Das sieht nicht nach einem Link aus. Kannst du es nochmal versuchen?")

async def process_request(user_input):
    try:
        web_data = await get_web_data(user_input)
        messagebox.showinfo("Chatbot Antwort", f"Hier sind die Informationen, die ich gefunden habe: {web_data}")
    except Exception as e:
        messagebox.showwarning("Fehler", f"Etwas ist schief gelaufen: {e}")

class WebChatbot:
    def __init__(self):
        self.history = []

    def add_to_history(self, url, result):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append({
            "timestamp": timestamp,
            "url": url,
            "result": str(result)[:100] + "..."  # Gekürzte Version
        })

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("Web-Chatbot")
        
        # Erstelle Tabs
        tab_control = ttk.Notebook(self.root)
        
        # Tab 1: Web Scraping
        tab1 = ttk.Frame(tab_control)
        tab_control.add(tab1, text='Web Scraping')
        
        # Tab 2: Verlauf
        tab2 = ttk.Frame(tab_control)
        tab_control.add(tab2, text='Verlauf')
        
        tab_control.pack(expand=1, fill='both')

    def save_result(self, data):
        with open('saved_results.json', 'a', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "data": data
            }, f, ensure_ascii=False)
            f.write('\n')

    def show_progress(self):
        progress = ttk.Progressbar(
            self.root, 
            orient='horizontal', 
            length=300, 
            mode='indeterminate'
        )
        progress.pack(pady=10)
        progress.start()
        return progress

    def export_results(self, format='txt'):
        filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
        
        if format == 'txt':
            with open(filename, 'w', encoding='utf-8') as f:
                for entry in self.history:
                    f.write(f"Zeit: {entry['timestamp']}\n")
                    f.write(f"URL: {entry['url']}\n")
                    f.write(f"Ergebnis: {entry['result']}\n\n")

root = tk.Tk()
root.title("Web-Chatbot")

# Chatbot UI
label = tk.Label(root, text="Gib einen Link ein oder stelle eine Frage:")
label.pack(pady=10)

entry = tk.Entry(root, width=40)
entry.pack(pady=10)

button = tk.Button(root, text="Anfrage senden", command=chatbot_response)
button.pack(pady=10)

root.mainloop()
