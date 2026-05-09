#!/usr/bin/env python3
"""
生成Clash Meta配置文件
"""
import yaml
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database import ProxyDatabase

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

    parser = argparse.ArgumentParser(description='生成Clash Meta配置文件')
    parser.add_argument('--count', type=int, help='代理数量限制')
    parser.add_argument('--output', '-o', help='输出文件路径')

    args = parser.parse_args()

    db = ProxyDatabase('proxies.db')
    proxies = db.get_valid_proxies(args.count)

    print(f"生成 {len(proxies)} 个代理的Clash配置")
    generate_clash_config(proxies, args.output)