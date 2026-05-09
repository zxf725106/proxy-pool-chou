import requests
from bs4 import BeautifulSoup
import time
import random

class ProxyCrawler:
    def __init__(self):
        self.sources = [
            'https://free-proxy-list.net/',
            'https://www.us-proxy.org/',
            'https://free-proxy-list.net/uk-proxy.html',
            'https://free-proxy-list.net/anonymous-proxy.html'
        ]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def crawl_proxies(self):
        proxies = []
        for url in self.sources:
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'lxml')
                table = soup.find('table', {'class': 'table table-striped table-bordered'})
                if table:
                    rows = table.find_all('tr')[1:]  # Skip header
                    for row in rows:
                        cols = row.find_all('td')
                        if len(cols) >= 2:
                            ip = cols[0].text.strip()
                            port = cols[1].text.strip()
                            if ip and port.isdigit():
                                protocol = 'https' if len(cols) > 6 and cols[6].text.strip().lower() == 'yes' else 'http'
                                country = cols[2].text.strip() if len(cols) > 2 else None
                                proxies.append({
                                    'ip': ip,
                                    'port': int(port),
                                    'protocol': protocol,
                                    'country': country
                                })
                time.sleep(random.uniform(1, 3))  # Respectful delay
            except Exception as e:
                print(f"Error crawling {url}: {e}")
        return proxies