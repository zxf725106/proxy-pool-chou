from flask import Flask, jsonify, Response, request
from database import ProxyDatabase
import yaml

app = Flask(__name__)
db = ProxyDatabase('../proxies.db')

@app.route('/proxies', methods=['GET'])
def get_proxies():
    proxies = db.get_valid_proxies()
    return jsonify(proxies)

@app.route('/proxies/<int:count>', methods=['GET'])
def get_proxies_count(count):
    proxies = db.get_valid_proxies(count)
    return jsonify(proxies)

@app.route('/clash', methods=['GET'])
def get_clash_config():
    count = request.args.get('count', type=int)
    if count:
        proxies = db.get_valid_proxies(count)
    else:
        proxies = db.get_valid_proxies()
    clash_config = generate_clash_config(proxies)
    return Response(yaml.dump(clash_config, default_flow_style=False), mimetype='text/yaml')

def generate_clash_config(proxies):
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
    return clash_config

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)