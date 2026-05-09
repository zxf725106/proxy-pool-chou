#!/usr/bin/env python3
"""
代理节点导出工具 - 支持多种格式
"""
import yaml
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database import ProxyDatabase


def export_clash(proxies, output_file=None):
    """导出为 Clash Meta 配置格式"""
    proxy_list = []
    for i, proxy in enumerate(proxies, 1):
        proxy_config = {
            'name': f'proxy-{i}',
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

    content = yaml.dump(clash_config, default_flow_style=False, allow_unicode=True)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ 已导出到 Clash 配置: {output_file} ({len(proxies)} 个节点)")
    else:
        print(content)


def export_json(proxies, output_file=None):
    """导出为 JSON 格式"""
    data = {
        'total': len(proxies),
        'proxies': proxies
    }
    
    content = json.dumps(data, indent=2, ensure_ascii=False)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ 已导出到 JSON: {output_file} ({len(proxies)} 个节点)")
    else:
        print(content)


def export_txt(proxies, output_file=None):
    """导出为文本格式 (IP:PORT)"""
    lines = [f"{p['ip']}:{p['port']}" for p in proxies]
    content = '\n'.join(lines)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ 已导出到文本: {output_file} ({len(proxies)} 个节点)")
    else:
        print(content)


def export_m3u(proxies, output_file=None):
    """导出为 ShadowRocket/Surge 格式"""
    lines = ['#EXTM3U']
    for i, proxy in enumerate(proxies, 1):
        lines.append(f"#EXTINF:-1,proxy-{i}")
        lines.append(f"http://{proxy['ip']}:{proxy['port']}")
    
    content = '\n'.join(lines)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ 已导出到 M3U: {output_file} ({len(proxies)} 个节点)")
    else:
        print(content)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='代理节点导出工具')
    parser.add_argument('--format', '-f', choices=['clash', 'json', 'txt', 'm3u'], 
                       default='clash', help='导出格式（默认: clash）')
    parser.add_argument('--count', type=int, help='导出数量限制（不指定则导出全部）')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--db', default='proxies.db', help='数据库文件路径')

    args = parser.parse_args()

    # 获取代理
    db = ProxyDatabase(args.db)
    if args.count:
        proxies = db.get_valid_proxies(args.count)
    else:
        proxies = db.get_valid_proxies(100000)  # 获取足够多的代理
    
    print(f"从数据库获取 {len(proxies)} 个代理\n")

    # 导出
    if args.format == 'clash':
        export_clash(proxies, args.output)
    elif args.format == 'json':
        export_json(proxies, args.output)
    elif args.format == 'txt':
        export_txt(proxies, args.output)
    elif args.format == 'm3u':
        export_m3u(proxies, args.output)
