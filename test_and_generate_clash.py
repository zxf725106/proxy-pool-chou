#!/usr/bin/env python3
"""
生成Clash Meta配置文件 - 带测速和过滤功能
"""
import yaml
import sys
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database import ProxyDatabase
import requests

class ProxyTester:
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.test_url = 'http://httpbin.org/get'
    
    def test_proxy(self, proxy):
        """
        测试单个代理的延迟
        返回 (proxy, latency_ms) 或 (proxy, None)
        """
        proxy_url = f"{proxy['protocol']}://{proxy['ip']}:{proxy['port']}"
        proxies = {
            'http': proxy_url,
            'https': proxy_url
        }
        try:
            start = time.time()
            response = requests.get(self.test_url, proxies=proxies, timeout=self.timeout)
            latency = (time.time() - start) * 1000
            if response.status_code == 200:
                return proxy, latency
        except:
            pass
        return proxy, None

def generate_clash_config(proxies, output_file=None):
    """生成Clash Meta格式的配置"""
    proxy_list = []
    for i, proxy in enumerate(proxies):
        proxy_config = {
            'name': f'proxy-{i+1}',
            'type': 'http',
            'server': proxy['ip'],
            'port': proxy['port'],
            'udp': True
        }
        proxy_list.append(proxy_config)

    clash_config = {
        'proxies': proxy_list,
        'proxy-groups': [
            {
                'name': 'auto',
                'type': 'url-test',
                'proxies': [p['name'] for p in proxy_list],
                'url': 'http://www.gstatic.com/generate_204',
                'interval': 300
            }
        ]
    }

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(clash_config, f, default_flow_style=False, allow_unicode=True)
        print(f"Clash配置文件已保存到: {output_file}")
    else:
        print(yaml.dump(clash_config, default_flow_style=False, allow_unicode=True))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='生成并测速Clash Meta配置文件')
    parser.add_argument('--count', type=int, default=100, help='代理数量（默认100）')
    parser.add_argument('--output', '-o', default='clash_config.yaml', help='输出文件路径')
    parser.add_argument('--max-latency', type=int, default=300, help='最大延迟阈值(ms, 默认300)')
    parser.add_argument('--workers', type=int, default=10, help='并发测速线程数（默认10）')
    parser.add_argument('--skip-test', action='store_true', help='跳过测速')

    args = parser.parse_args()

    db = ProxyDatabase('proxies.db')
    raw_proxies = db.get_valid_proxies(args.count)
    print(f"从数据库获取 {len(raw_proxies)} 个代理")

    if args.skip_test:
        print("跳过测速，直接保存")
        generate_clash_config(raw_proxies, args.output)
    else:
        # 进行测速
        print(f"开始测速 ({args.workers} 线程并发)...")
        tester = ProxyTester()
        valid_proxies = []
        good_proxies = []

        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {executor.submit(tester.test_proxy, p): p for p in raw_proxies}
            completed = 0
            for future in as_completed(futures):
                completed += 1
                proxy, latency = future.result()
                if latency is not None:
                    if latency <= args.max_latency:
                        good_proxies.append((proxy, latency))
                        print(f"✓ [{completed}/{len(raw_proxies)}] {proxy['ip']}:{proxy['port']} - {latency:.0f}ms (保留)")
                    else:
                        print(f"✗ [{completed}/{len(raw_proxies)}] {proxy['ip']}:{proxy['port']} - {latency:.0f}ms (删除)")
                else:
                    print(f"✗ [{completed}/{len(raw_proxies)}] {proxy['ip']}:{proxy['port']} - 无响应 (删除)")

        # 按延迟排序（从低到高）
        good_proxies.sort(key=lambda x: x[1])
        valid_proxies = [p[0] for p in good_proxies]

        print(f"\n测速完成: 保留 {len(valid_proxies)}/{len(raw_proxies)} 个代理")
        if valid_proxies:
            print(f"延迟范围: {good_proxies[0][1]:.0f}ms ~ {good_proxies[-1][1]:.0f}ms")
        
        generate_clash_config(valid_proxies, args.output)
