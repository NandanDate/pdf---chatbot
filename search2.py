import requests
from bs4 import BeautifulSoup
import sqlite3

def fetch_wikipedia_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', href=True)
    wikipedia_links = []
    for link in links:
        href = link.get('href')
        if is_valid_link(href):
            wikipedia_links.append(href)
    return wikipedia_links

def is_valid_link(href):
    if href and href.startswith('/wiki/') and ':' not in href and '#' not in href:  
        full_url = 'https://en.wikipedia.org' + href
        try:
            response = requests.head(full_url)
            return response.status_code == 200  # Link is valid if status code is 200 (OK)
        except requests.exceptions.RequestException:
            return False
    return False

def create_db():
    conn = sqlite3.connect('wiki_links_search2.db')
    c = conn.cursor()
    c.execute('''CREATE VIRTUAL TABLE IF NOT EXISTS links_fts
                 USING fts5(link)''')  # Removed TEXT from column definition
    conn.commit()
    conn.close()

def index_links(links):
    conn = sqlite3.connect('wiki_links_search2.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS links
                 (id INTEGER PRIMARY KEY, link TEXT UNIQUE)''')  # Add UNIQUE constraint to ensure uniqueness
    for link in links:
        full_url = 'https://en.wikipedia.org' + link
        c.execute("INSERT OR IGNORE INTO links (link) VALUES (?)", (full_url,))  # Use INSERT OR IGNORE to skip duplicates
    conn.commit()
    conn.close()


def main():
    create_db()
    seed_url = 'https://en.wikipedia.org/wiki/Main_Page'
    links = fetch_wikipedia_links(seed_url)
    index_links(links)

if __name__ == "__main__":
    main()
