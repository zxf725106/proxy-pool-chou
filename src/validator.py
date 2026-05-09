import requests
import time

class ProxyValidator:
    def __init__(self, timeout=30):
        self.timeout = timeout
        self.test_url = 'http://httpbin.org/get'

    def validate_proxy(self, proxy):
        """
        Validate a single proxy
        proxy: dict with 'ip', 'port', 'protocol'
        Returns: (is_valid, speed)
        """
        proxy_url = f"{proxy['protocol']}://{proxy['ip']}:{proxy['port']}"
        proxies = {
            'http': proxy_url,
            'https': proxy_url
        }
        try:
            start_time = time.time()
            response = requests.get(self.test_url, proxies=proxies, timeout=self.timeout)
            end_time = time.time()
            if response.status_code == 200:
                speed = end_time - start_time
                return True, speed
            else:
                return False, None
        except:
            return False, None

    def validate_proxies(self, proxies):
        """
        Validate a list of proxies
        Returns list of valid proxies with speed
        """
        valid_proxies = []
        for proxy in proxies:
            is_valid, speed = self.validate_proxy(proxy)
            if is_valid:
                proxy['speed'] = speed
                valid_proxies.append(proxy)
            time.sleep(0.1)  # Small delay to avoid overwhelming
        return valid_proxies