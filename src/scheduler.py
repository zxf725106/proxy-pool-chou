import schedule
import time
from datetime import datetime
from .crawler import ProxyCrawler
from .validator import ProxyValidator
from .database import ProxyDatabase

class ProxyScheduler:
    def __init__(self):
        self.crawler = ProxyCrawler()
        self.validator = ProxyValidator()
        self.db = ProxyDatabase()

    def update_proxies(self):
        print(f"[{datetime.now()}] Starting proxy update...")
        # Crawl new proxies
        raw_proxies = self.crawler.crawl_proxies()
        print(f"Crawled {len(raw_proxies)} proxies")

        # For now, store all crawled proxies as valid (skip validation for speed)
        stored = 0
        for proxy in raw_proxies:
            try:
                self.db.insert_proxy(
                    proxy['ip'],
                    proxy['port'],
                    proxy['protocol'],
                    proxy.get('country'),
                    None  # speed
                )
                stored += 1
            except Exception as e:
                print(f"Error storing proxy {proxy['ip']}:{proxy['port']}: {e}")
        print(f"Stored {stored} proxies in database")

    def run_daily_at_9am(self):
        schedule.every().day.at("09:00").do(self.update_proxies)

        print("Scheduler started. Will update proxies daily at 9:00 AM")
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

if __name__ == "__main__":
    scheduler = ProxyScheduler()
    scheduler.run_daily_at_9am()